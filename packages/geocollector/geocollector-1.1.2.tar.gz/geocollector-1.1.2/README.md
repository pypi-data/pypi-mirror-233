# GEO Collector

![PyPI - Version](https://img.shields.io/pypi/v/GEOcollector?style=for-the-badge&logo=PyPy&logoColor=white&color=red&link=https%3A%2F%2Fpypi.org%2Fproject%2Fgeocollector%2F)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/JoshLoecker/GEOcollector/tests.yml?style=for-the-badge&logo=pytest&logoColor=white&label=Tests)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/GEOcollector?style=for-the-badge&logo=python&logoColor=white)
![Coveralls branch](https://img.shields.io/coverallsCoverage/github/JoshLoecker/GEOcollector?branch=master&style=for-the-badge&logo=coveralls&logoColor=white)

## Description

GEOcollector is a Python package for collecting metadata about gene expression datasets from the NCBI Gene Expression
Omnibus (GEO) database. It will convert a list of GSM accession numbers and cell types into the information required
for [FastqToGeneCounts](https://github.com/HelikarLab/FastqToGeneCounts) to process the raw RNA-seq data.

Long story short, given an input file like this:

```csv
GSM,cell_type
GSM3785334,baso
GSM3898581,baso

```

GEOcollector will output a file like this (without formatted columns):

```csv
GSE       ,GSM        ,SRR        ,Rename    ,Strand ,Prep Method ,Platform Code ,Platform Name                      ,Source           ,Cell Characteristics                                                                                                                                                                                                                        ,Replicate Name                                                        ,Strategy ,Publication ,Extra Notes
GSE131525 ,GSM3785334 ,SRR9097791 ,baso_S1R1 ,SE     ,total       ,GPL16791      ,Illumina HiSeq 2500 (Homo sapiens) ,B                ,subject - disease status: Screened Healthy Control;subject: HC3;age at draw: 55;Sex: Female;median cv coverage: 0.763618;fastq total reads: 6241803;unpaired reads examined: 5663490;unpaired read duplicates: 1597507;primary race: White; ,lib3945                                                               ,RNA-Seq  ,31671072    ,
GSE133028 ,GSM3898581 ,SRR9328889 ,baso_S2R1 ,PE     ,total       ,GPL20301      ,Illumina HiSeq 4000 (Homo sapiens) ,peripheral blood ,cell type: peripheral blood B cells;                                                                                                                                                                                                        ,Patient 2 IgD-CD27- double negative B cells from the peripheral blood ,RNA-Seq  ,32859762    ,
GSE133028 ,GSM3898591 ,SRR9328899 ,baso_S2R2 ,PE     ,total       ,GPL20301      ,Illumina HiSeq 4000 (Homo sapiens) ,peripheral blood ,cell type: peripheral blood B cells;                                                                                                                                                                                                        ,Patient 3 IgD-CD27- double negative B cells from the peripheral blood ,RNA-Seq  ,32859762    ,
```

## Installation

To install GEOcollector, you can use pip:

```bash
pip install GEOcollector
```

## Usage

The following sections are command line parameters associated with GEOcollector

### Command Line Interface

To execute GEOcollector, simply call it from the command line with the relevant parameters

```bash
geocollector --api-key APIKEY --input-file /home/user/input.csv --verbose
geocollector --input-file /home/user/input.csv --quiet
geocollector --api-key APIKEY --input-file /home/user/input.csv
```

To view help for GEOcollector, run the following command

```bash
geocollector --help
```

### API Key

Without an API key, NCBI limits the number of requests to 3 per second. With an API key, this value is increased to 10
requests per second. To obtain an API key, follow the below steps

1. Access [NCBI's website](https://www.ncbi.nlm.nih.gov/)
2. Click "Log In" in the top right corner
    1. If you do not have an account, create one now
3. Click your username in the top right corner
4. Click "Account settings" in the dropdown menu
5. Scroll down to the "API Key" section
6. Click "Create API Key"
7. Copy the API key that has been created

### Input file

The input file should be a CSV file in the following format. Multiple GSMs can be associated to a single cell type

```csv
GSM,cell_type
GSM_1,cell_type_1
GSM_2,cell_type_1
GSM_3,cell_type_1
GSM_4,cell_type_2
```

### Verbosity

If you would like to show debug information on the command line, pass the flag `--verbose`. If you would like to silence
all output (except warnings), pass the flag `--quiet`. If neither flag is passed, standard "info" messages will be shown

---

If you have problems, please [create a new issue](https://github.com/JoshLoecker/GEOcollector/issue)
