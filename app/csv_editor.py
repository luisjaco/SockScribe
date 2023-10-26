import sys
import os

class TextEditor:
    def __init__(self, path: str):
        self.path = path


    def append_to_file(self, data: str):
        try:
            with open(self.path, 'a') as fileobj:
                fileobj.write("\n" + data)
        except FileNotFoundError:
            print("Error: Path not found, exiting.")
            raise FileNotFoundError
    