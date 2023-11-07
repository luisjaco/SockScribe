import sys
import os
import csv

class CSVEditor:
    def __init__(self, path: str, delimiter: str):
        """
        Creates a CSVEditor instance, appends data to a csv file.\n
        Parameters: \n
            path-- File path of the csv file, will be checked if valid.\n
            delimiter-- Delimiter of data within csv.\n
        Returns: CSVEditor instance.
        """
        if os.path.exists(path):
            self.path = path
            self.delimiter = delimiter
        else:
            print("Error: path not found, exiting")
            sys.exit(1)


    def append_to_file(self, data: str):
        if os.path.exists(self.path):
            with open(self.path, 'a') as csvfile:
                split_data = data.split(sep=self.delimiter)
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(split_data)
        else:
            print("Error: Path not found when attempting to append data, exiting.")
            raise FileNotFoundError
        