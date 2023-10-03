import os
import argparse
import pandas as pd
from logging import INFO, DEBUG, ERROR


class Arguments(argparse.Namespace):
    """
    This class is meant to hold command line arguments
    It should not persist past the scope of the main function; the "Settings" class is meant for that
    """
    
    def __init__(self) -> None:
        super().__init__()
        self._api_key: str = ""
        self._input_file: str = ""
        self._verbosity: int = INFO
        self._dataframe: pd.DataFrame = pd.DataFrame()
    
    @property
    def api_key(self) -> str:
        return self._api_key
    
    @api_key.setter
    def api_key(self, value: str) -> None:
        self._api_key = value
    
    @property
    def input_file(self) -> str:
        return self._input_file
    
    @input_file.setter
    def input_file(self, value: str) -> None:
        self._input_file = value
    
    @property
    def verbosity(self) -> int:
        return self._verbosity
    
    @verbosity.setter
    def verbosity(self, value: str) -> None:
        if value == "DEBUG":
            self._verbosity = DEBUG
        elif value == "ERROR":
            self._verbosity = ERROR
        else:
            self._verbosity = INFO
    
    @property
    def dataframe(self) -> pd.DataFrame:
        if self._dataframe.empty:
            self._dataframe = pd.read_csv(self.input_file, comment="#")
        return self._dataframe


def parse_args(argv: list[str]) -> Arguments:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-k", "--api-key",
        type=str,
        required=False,
        dest="api_key",
        help="API key for NCBI API. Visit https://account.ncbi.nlm.nih.gov/settings/ to create one."
    )
    parser.add_argument(
        "-i", "--input-file",
        type=str,
        required=True,
        dest="input_file",
        help="Path to data file. This file should be a CSV with columns 'gse', and one (or both) of: 'gsm', 'name'."
    )
    
    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument(
        "-v", "--verbose",
        action="store_const",
        dest="verbosity",
        const="DEBUG",
        help="Print verbose output."
    )
    verbosity.add_argument(
        "-q", "--quiet",
        action="store_const",
        dest="verbosity",
        const="ERROR",
        help="Print only errors."
    )
    
    namespace = Arguments()
    args = parser.parse_args(argv, namespace=namespace)
    return args
