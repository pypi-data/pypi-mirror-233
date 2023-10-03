import re
import tqdm
import aiohttp
import asyncio
import pandas as pd
from logging import Logger
from types import TracebackType
from xml.etree import ElementTree
from typing import Type, Union, Literal
from xml.etree.ElementTree import Element
from tqdm.contrib.logging import logging_redirect_tqdm
from aiohttp.client_exceptions import ServerDisconnectedError

from geocollector.records import Record


class NCBI:
    eutils_session: aiohttp.ClientSession = None
    sra_session: aiohttp.ClientSession = None
    eutils_search_path: str = f"/entrez/eutils/esearch.fcgi?db=gds&term=[accession]&idtype=acc"
    eutils_fetch_path: str = f"/entrez/eutils/efetch.fcgi?db=gds&id=[ids]"
    
    def __init__(self, input_df: pd.DataFrame, logger: Logger, key: str = ""):
        self._ncbi_key: str = key
        self.input_df: pd.DataFrame = input_df
        self.logger: Logger = logger
        self.request_per_second: int = 3
        self.delay: float = 0.37
        self.previous_time = 0
        
        if self._ncbi_key != "":
            self.logger.info("API key provided - setting request rate to 10 per second")
            self.eutils_search_path += f"&api_key={self._ncbi_key}"
            self.eutils_fetch_path += f"&api_key={self._ncbi_key}"
            self.request_per_second = 10
            self.delay = 0.12
        else:
            self.logger.warning(
                "No API key provided - limiting to request rate to 3 per second. "
                "Create one at https://account.ncbi.nlm.nih.gov/settings/"
            )
        
        # Add columns to input dataframe then set column order
        self.main_columns: list[str] = [
            "GSE", "GSM", "SRR",
            "Rename", "Strand", "Prep Method",
            "Platform Code", "Platform Name", "Source",
            "Cell Characteristics", "Replicate Name",
            "Strategy", "Publication", "Extra Notes"
        ]
        self.internal_columns: list[str] = ["search_id", "cell_type", "srx"]
        self.input_df = pd.concat([
            self.input_df,
            pd.DataFrame(columns=self.main_columns + self.internal_columns)
        ])
        self.input_df = self.input_df[self.main_columns + self.internal_columns]
    
    @property
    def ncbi_key(self) -> str:
        return self._ncbi_key
    
    @property
    def dataframe(self) -> pd.DataFrame:
        return self.input_df
    
    async def execute(self) -> None:
        num_records = len(self.input_df)
        if num_records == 1:
            self.logger.info("Starting work on 1 record")
        else:
            self.logger.info(f"Starting work on {num_records} records")
        
        await self.search()
        await self.update_data()
        await self.srx_to_srr()
        await self.collect_gsm_related_data()
        await self.collect_gse_related_data()
        self.set_rename_column()
        self.create_csv()
    
    async def __init_sessions__(self, force_reconnect: bool = False) -> None:
        if force_reconnect:
            self.logger.debug("Forcing reconnect to NCBI")
            await NCBI.eutils_session.close()
            await NCBI.sra_session.close()
        
        if NCBI.eutils_session is None or force_reconnect:
            NCBI.eutils_session = aiohttp.ClientSession("https://eutils.ncbi.nlm.nih.gov")
            self.eutils_session: aiohttp.ClientSession = NCBI.eutils_session
        if NCBI.sra_session is None or force_reconnect:
            NCBI.sra_session = aiohttp.ClientSession("https://www.ncbi.nlm.nih.gov")
            self.sra_session: aiohttp.ClientSession = NCBI.sra_session
    
    def create_csv(self) -> None:
        write_df: pd.DataFrame = self.input_df[self.main_columns].copy()
        write_df.to_csv("output_data.csv", sep=",", index=False)
    
    async def __aenter__(self) -> "NCBI":
        await self.__init_sessions__()
        return self
    
    async def __aexit__(self, exc_type: Type[BaseException], exc_val: BaseException, exc_tb: TracebackType) -> None:
        await self.eutils_session.close()
        await self.sra_session.close()
    
    async def get(
        self,
        session: Literal["eutils", "sra"],
        path: str,
    ) -> aiohttp.ClientResponse:
        self.logger.debug(f"Making request to path: {path}")
        connection: aiohttp.ClientSession
        if session == "eutils":
            connection = self.eutils_session
        elif session == "sra":
            connection = self.sra_session
        
        await asyncio.sleep(self.delay)
        response: aiohttp.ClientResponse
        try:
            response = await connection.get(path)
        except ServerDisconnectedError:
            self.logger.debug("Server disconnected, retrying request")
            await self.__init_sessions__(force_reconnect=True)
            response = await connection.get(path)
        
        tries = 0
        while not response.ok and tries < 3:
            tries += 1
            code_family = str(response.status)[0]
            
            if code_family == "4":
                self.logger.debug(f"Received status code {response.status}, retrying request")
                await asyncio.sleep(5)
                response = await connection.get(path)
            else:
                raise aiohttp.ClientResponseError(
                    status=response.status,
                    message=f"Request failed, status code: {response.status}",
                    history=response.history,
                    request_info=response.request_info,
                )
        return response
    
    async def search(self) -> None:
        """
        This function will perform a search on the NCBI API for each GSE accession number in the input file.
        It will return a list of IDs, which will be used to fetch the records.
        :return:
        """
        ids = []
        with logging_redirect_tqdm([self.logger]):
            for gsm in tqdm.tqdm(self.input_df["GSM"], leave=False, desc="Searching for GSMs"):
                # for gsm in self.input_df["GSM"]:
                self.logger.debug(f"Searching for {gsm}")
                response = await self.get(
                    "eutils",
                    self.eutils_search_path.replace("[accession]", gsm),
                )
                xml_root: Element = ElementTree.fromstring(await response.text())
                ids.append([element.text for element in xml_root.findall('.//Id')])
        
        self.input_df["search_id"] = ids
        self.input_df = self.input_df.explode("search_id", ignore_index=True)
        self.logger.info(f"Search complete")
    
    async def update_data(self) -> None:
        """
        This function will perform a "fetch" for each of the IDs returned by the search function
        It will provide the `parse_fetch` function with the response, which will be used to parse the plain text into structured data
        :return:
        """
        with logging_redirect_tqdm([self.logger]):
            for gsm in tqdm.tqdm(self.input_df["GSM"].unique(), leave=False, desc="Fetching GSMs"):
                ids_list = self.input_df[self.input_df["GSM"] == gsm]["search_id"].tolist()
                cell_type = self.input_df[self.input_df["GSM"] == gsm]["cell_type"].tolist()[0]
                response = await self.get(
                    "eutils",
                    self.eutils_fetch_path.replace("[ids]", ",".join(ids_list))
                )
                
                record = self.parse_fetch(await response.text(), gsm, cell_type)
                self.input_df.loc[self.input_df["search_id"] == record.SEARCH_ID, "GSE"] = record.GSE
                self.input_df.loc[self.input_df["search_id"] == record.SEARCH_ID, "srx"] = record.SRX_ACCESSION
                self.input_df.loc[self.input_df["search_id"] == record.SEARCH_ID, "Rename"] = record.TITLE
        
        self.input_df = self.input_df.dropna(subset=["GSE"])
        self.logger.info(f"Fetch complete")
    
    def parse_fetch(self, response: str, gsm: str, cell_type: str) -> Record:
        """
        This function will parse the plain text provided by the NCBI api into structured data
        :param response: The plain text response returned from NCBI
        :param gsm: The GSM that was used to fetch the record
        :param cell_type: The GSM's cell type
        :return: A Record object
        """
        records = re.split(r"\n(?=\d+\.)", response.strip())
        
        for record in records:
            gse_accession_match = re.search(r'Series\s+Accession:\s+(.*?)\s+', record)
            platform_id_match = re.search(r"Platform\s+Accession:\s+(.*?)\s+", record)
            gsm_accession_match = re.search(r'Sample\s+Accession:\s+(.*?)\s+', record)
            
            if gse_accession_match:
                gse_accession = gse_accession_match.group(1)
                self.logger.debug(f"Found GSE Accession: {gse_accession}")
            elif platform_id_match:
                platform_id = platform_id_match.group(1)
                
                platform_name_match: Union[re.Match[str], None] = re.match(r'^\d+\.\s+(.*?)\n', record)
                platform_name: str = platform_name_match.group(1) if platform_name_match else ""
                self.logger.debug(f"Found Platform {platform_name} with ID {platform_id}")
            elif gsm_accession_match and gsm_accession_match.group(1) == gsm:
                gsm_accession = gsm_accession_match.group(1)
                title_match = re.match(r'\d+\.\s+(.*?)\n', record)
                title = title_match.group(1) if title_match else ""
                
                organism_match = re.search(r'Organism:\s+(.*?)\n', record)
                organism = organism_match.group(1) if organism_match else ""
                
                source_name_match = re.search(r'Source name:\s+(.*?)\n', record)
                source_name = source_name_match.group(1) if source_name_match else ""
                
                platform_match = re.search(r'Platform:\s+(.*?)\s+', record)
                platform_id = platform_match.group(1) if platform_match else ""
                
                srx_link_match = re.search(r'SRA Run Selector:\s+(.*?)\n', record)
                srx_link = srx_link_match.group(1) if srx_link_match else ""
                
                search_id_match = re.search(r"\s+ID:\s+(\d+)", record)
                search_id = search_id_match.group(1) if search_id_match else ""
                
                self.logger.debug(f"Found GSM accession {gsm_accession} with SRX link {srx_link}")
                
                new_record = Record(
                    TITLE=title,
                    GSE=gse_accession,
                    ORGANISM=organism,
                    SOURCE=source_name,
                    PLATFORM_ID=platform_id,
                    PLATFORM_NAME=platform_name,
                    CELL_TYPE=cell_type,
                    SRX_LINK=srx_link,
                    GSM=gsm_accession,
                    SEARCH_ID=search_id
                )
        
        return new_record
    
    async def srx_to_srr(self) -> None:
        """
        This function will parse the SRX link from the NCBI API and return the SRR value
        :return:
        """
        for srx in tqdm.tqdm(self.input_df["srx"], leave=False, desc="Converting SRX -> SRR"):
            response: aiohttp.ClientResponse = await self.get("sra", f"/sra/?term={srx}")
            text: str = await response.text()
            
            srr_match: Union[re.Match[str], None] = re.search(r"trace\.ncbi\.nlm\.nih\.gov/Traces\?run=(SRR\d+)", text)
            srr: str = srr_match.group(1) if srr_match else ""
            
            # Search for <div>:Layout: <span>PAIRED</span></div>
            strand_match: Union[re.Match[str], None] = re.search(r"<div>Layout: <span>(.*?)</span></div>", text)
            strand: str = strand_match.group(1) if strand_match else ""
            if strand.lower() == "single":
                strand = "SE"
            elif strand.lower() == "paired":
                strand = "PE"
            
            self.input_df.loc[self.input_df["srx"] == srx, "SRR"] = srr
            self.input_df.loc[self.input_df["srx"] == srx, "Strand"] = strand
        
        self.logger.info(f"Conversion complete")
    
    async def collect_gsm_related_data(self) -> None:
        for gsm in tqdm.tqdm(self.input_df["GSM"].unique(), leave=False, desc="Getting GSM data"):
            response = await self.get("sra", f"/geo/query/acc.cgi?acc={gsm}")
            text = await response.text()
            
            split_text = text.split("\n")
            
            replicate_title = self.get_replicate_title(split_text)
            prep_method = self.get_prep_method(text)
            platform_id = self.get_platform_id(split_text)
            platform_name = await self.get_platform_name(platform_id)
            library_strategy = self.get_library_strategy(split_text)
            source = self.get_source_name(split_text)
            characteristics = self.get_cell_characteristics(split_text)
            
            self.input_df.loc[self.input_df["GSM"] == gsm, "Replicate Name"] = replicate_title.replace(",", ";")
            self.input_df.loc[self.input_df["GSM"] == gsm, "Prep Method"] = prep_method.replace(",", ";")
            self.input_df.loc[self.input_df["GSM"] == gsm, "Platform Name"] = platform_name.replace(",", ";")
            self.input_df.loc[self.input_df["GSM"] == gsm, "Platform Code"] = platform_id.replace(",", ";")
            self.input_df.loc[self.input_df["GSM"] == gsm, "Strategy"] = library_strategy.replace(",", ";")
            self.input_df.loc[self.input_df["GSM"] == gsm, "Source"] = source.replace(",", ";")
            self.input_df.loc[self.input_df["GSM"] == gsm, "Cell Characteristics"] = characteristics.replace(",", ";")
        
        self.logger.info(f"GSM collection complete")
    
    def get_replicate_title(self, split_text: list[str]) -> str:
        replicate_title: str
        for i, line in enumerate(split_text):
            if line.lower() == '<tr valign="top"><td nowrap>title</td>':
                replicate_title = split_text[i + 1].strip()
                break
        
        replicate_title = replicate_title.replace('<td style="text-align: justify">', "").replace("</td>", "")
        return replicate_title
    
    def get_cell_characteristics(self, split_text: list[str]) -> str:
        characteristics: str
        for i, line in enumerate(split_text):
            if line.lower() == '<tr valign="top"><td nowrap>characteristics</td>':
                characteristics = split_text[i + 1].strip()
                break
        
        characteristics = characteristics.replace('<td style="text-align: justify">', "").replace("</td>", "")
        characteristics = characteristics.replace("<br>", ";")
        return characteristics
    
    def get_source_name(self, split_text: list[str]) -> str:
        source: str
        for i, line in enumerate(split_text):
            if line.lower() == '<tr valign="top"><td nowrap>source name</td>':
                source = split_text[i + 1].strip()
                break
        
        source = source.replace('<td style="text-align: justify">', "").replace("</td>", "")
        source = source.replace("<br>", "")
        return source
    
    def get_prep_method(self, text: str) -> str:
        
        # Search for "total RNA" in response
        prep_method: str = ""
        if "total rna" in text.lower():
            prep_method = "total"
        elif "polya rna" in text.lower():
            prep_method = "mrna"
        
        return prep_method
    
    def get_platform_id(self, split_text: list[str]) -> str:
        platform_html: str
        for i, line in enumerate(split_text):
            if line.lower() == '<tr valign="top"><td>platform id</td>':
                platform_html = split_text[i + 1].strip()
        
        platform_id_match = re.search(r"/geo/query/acc.cgi\?acc=(.+)\">", platform_html)
        platform_id = platform_id_match.group(1) if platform_id_match else ""
        
        return platform_id
    
    async def get_platform_name(self, platform_id: str) -> str:
        response = await self.get("sra", f"/geo/query/acc.cgi?acc={platform_id}")
        text = await response.text()
        
        platform_name: str = ""
        split_text = text.split("\n")
        for i, line in enumerate(split_text):
            if line.lower() == '<tr valign="top"><td nowrap>title</td>':
                platform_name = split_text[i + 1].strip()
                break
        
        platform_name = platform_name.replace('<td style="text-align: justify">', "").replace("</td>", "")
        return platform_name
    
    def get_library_strategy(self, split_text: list[str]) -> str:
        library_strategy: str = ""
        for i, line in enumerate(split_text):
            if line.lower() == '<tr valign="top"><td nowrap>library strategy</td>':
                library_strategy = split_text[i + 1].strip()
                break
        
        library_strategy = library_strategy.replace("<td>", "").replace("</td>", "")
        return library_strategy
    
    async def collect_gse_related_data(self) -> None:
        unique_gse = len(self.input_df["GSE"].unique())
        for gse in tqdm.tqdm(self.input_df["GSE"].unique(), leave=False, desc=f"Getting {unique_gse} unique GSE data"):
            response = await self.get("sra", f"/geo/query/acc.cgi?acc={gse}")
            text = await response.text()
            
            publication = self.get_publication(text).replace(",", ";")
            self.input_df.loc[self.input_df["GSE"] == gse, "Publication"] = publication
        
        self.logger.info(f"GSE collection complete")
    
    def get_publication(self, text: str) -> str:
        # Search for "PMID: \d+" in response
        # Regex: class="pubmed_id" id="34508131"
        publication_match = re.search(r"class=\"pubmed_id\" id=\"(\d+)\"", text)
        publication = publication_match.group(1) if publication_match else ""
        return publication
    
    def set_rename_column(self) -> None:
        study_number = 0
        for gse in self.input_df["GSE"].unique():
            cell_type = self.input_df[self.input_df["GSE"] == gse]["cell_type"].tolist()[0]
            study_number += 1
            run_number = 0
            for gsm in self.input_df[self.input_df["GSE"] == gse]["GSM"].unique():
                run_number += 1
                replicates = self.input_df[(self.input_df["GSE"] == gse) & (self.input_df["GSM"] == gsm)][
                    "SRR"].tolist()
                replicate_number = 0
                for replicate in replicates:
                    replicate_number += 1
                    name = f"{cell_type}_S{study_number}R{run_number}"
                    if len(replicates) > 1:
                        name += f"r{replicate_number}"
                    self.input_df.loc[self.input_df["SRR"] == replicate, "Rename"] = name
