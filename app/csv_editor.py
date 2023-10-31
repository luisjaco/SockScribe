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
        Returns: a CSVEditor instance.

        """
        if os.path.exists(path):
            self.path = path
            self.delimiter = delimiter
        else:
            print("Error: path not found, exiting")
            sys.exit(1)


    def append_to_file(self, data: str):
        try:
            with open(self.path, 'a') as csvfile:
                split_data = data.split(self.delimiter)
                csvwriter = csv.writer(csvfile, delimiter=self.delimiter)
                csvwriter.writerow(split_data)
        except FileNotFoundError:
            print("Error: Path not found when writing data.")
            raise FileNotFoundError
        