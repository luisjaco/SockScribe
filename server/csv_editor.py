import sys
import os
import csv

class CSVEditor:
    """
    The CSVEditor class handles appending csv data to a csv file.
    """
    def __init__(self, path: str, delimiter: str= ","):
        """
        Creates a CSVEditor instance.

        Args:
            path: file path to desired csv file.
            delimiter: delimiter to be used when writing csv data. default is ",".
        """
        if os.path.exists(path):
            self._path = path
            self._delimiter = delimiter
        else:
            print("Error: path not found, exiting")
            sys.exit(1)


    def append_to_file(self, data: str) -> None:
        """
        Appends csv data to the set csv file.
        
        Args:
            data: properly formatted csv data."""
        if os.path.exists(self._path):
            with open(self._path, 'a') as csvfile:
                split_data = data.split(sep=self._delimiter)
                csvwriter = csv.writer(csvfile, delimiter=self._delimiter)
                csvwriter.writerow(split_data)
        else:
            print("Error: Path not found when attempting to append data, exiting.")
            raise FileNotFoundError