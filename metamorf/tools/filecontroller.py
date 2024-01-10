from abc import ABC, abstractmethod
import yaml
from metamorf.constants import *
import csv
import json
import os


class FileController(ABC):
    @abstractmethod
    def __init__(self):
        pass

    def set_file_location(self, path: str, file_name: str):
        self.path = str(path)
        self.file_name = str(file_name)
        if self.path is None or self.path == "":
            self.final_path = self.file_name + "." + self.extension
        else:
            if self.file_name[-4:] != "." + self.extension:
                self.file_name += "." + self.extension
            self.final_path = self.path + "/" + self.file_name

    @abstractmethod
    def read_file(self):
        pass

    def setup_writer(self, append: str):
        self.file = open(self.final_path, append)

    def write_file(self, content: str):
        self.file.write(content)
        self.file.flush()

    def close(self):
        self.file.close()


class FileControllerYML(FileController):
    def __init__(self):
        self.extension = FILE_TYPE_YML
        self.file = None

    def read_file(self):
        if len(self.file_name) == 0 or self.file_name is None: raise ValueError("FileController_YML: Trying to read a file with null name")
        final_path = os.path.join(self.path, self.file_name)
        if final_path[-4:] != "." + self.extension:
            final_path += "." + self.extension
        try:
            with open(final_path) as file:
                file = yaml.full_load(file)
            return file
        except:
            return None
        return None

    def write_file(self, content: dict):
        self.file.write(yaml.dump(content, sort_keys=False))


class FileControllerJSON(FileController):
    def __init__(self):
        self.extension = FILE_TYPE_JSON
        self.file = None

    def read_file(self):
        if len(self.file_name) == 0 or self.file_name is None: raise ValueError("FileController_JSON: Trying to read a file with null name")
        final_path = os.path.join(self.path, self.file_name)
        if final_path[-4:] != "." + self.extension:
            final_path += "." + self.extension
        try:
            with open(final_path) as file:
                file = json.load(file)
            return file
        except:
            return None

    def write_file(self, content: dict):
        self.file.write(json.dumps(content , indent = 4))


class FileControllerSQL(FileController):
    def __init__(self):
        self.extension = FILE_TYPE_SQL
        self.file = None

    def read_file(self):
        if len(self.file_name)==0 or self.file_name==None: raise ValueError("FileController_SQL: Trying to read a file with None null")
        final_path = os.path.join(self.path, self.file_name)
        if str(final_path[-4:]) != "." + self.extension:
            final_path += "." + self.extension
        try:
            with open(final_path, encoding='utf-8') as file:
                result = file.read()
            return result
        except:
            return None
        return None


class FileControllerLOG(FileController):
    def __init__(self):
        self.extension = FILE_TYPE_LOG
        self.file = None

    def read_file(self):
        if len(self.file_name)==0 or self.file_name==None: raise ValueError("FileController_SQL: Trying to read a file with None null")
        final_path = os.path.join(self.path, self.file_name)
        if final_path[-4:] != "." + self.extension:
            final_path += "." + self.extension
        try:
            with open(final_path, encoding='utf-8') as file:
                result = file.read()
            return result
        except:
            return None
        return None


class FileControllerTXT(FileController):
    def __init__(self):
        self.extension = FILE_TYPE_TXT
        self.file = None

    def read_file(self):
        if len(self.file_name) == 0 or self.file_name is None: raise ValueError("FileController_SQL: Trying to read a file with None null")
        final_path = os.path.join(self.path, self.file_name)
        if final_path[-4:] != "." + self.extension:
            final_path += "." + self.extension
        try:
            with open(final_path, encoding='utf-8') as file:
                result = file.read()
            return result
        except:
            return None
        return


class FileControllerCSV(FileController):
    def __init__(self):
        self.extension = FILE_TYPE_CSV
        self.file = None
        self.delimiter = ','

    def set_delimiter(self, delimiter_character):
        self.delimiter = delimiter_character

    def read_file(self):
        if len(self.file_name) == 0 or self.file_name is None: raise ValueError("FileController_SQL: Trying to read a file with None null")
        if self.path is None or self.path == '': final_path = self.file_name
        else: final_path = os.path.join(self.path, self.file_name)
        if final_path[-4:] != "." + self.extension:
            final_path += "." + self.extension
        try:
            with open(final_path, encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=self.delimiter, quotechar = '"')
                result = []
                for row in reader:
                    result.append(row)
            return result
        except:
            return None
        return None

    def write_file(self, content: list):
        for row in content:
            final_row = ""
            for col in row:
                if col is None: col=''
                if ',' in str(col): col = '"'+str(col)+'"'
                final_row += str(col) + ','
            final_row = str(final_row[:-1])+"\n"
            self.file.write(final_row)

#####################################################################################


class FileControllerFactory:

    def get_file_reader(self, fileType: str):
        if fileType.upper() == FILE_TYPE_YML.upper():
            return FileControllerYML()
        elif fileType.upper() == FILE_TYPE_LOG.upper():
            return FileControllerLOG()
        elif fileType.upper() == FILE_TYPE_SQL.upper():
            return FileControllerSQL()
        elif fileType.upper() == FILE_TYPE_TXT.upper():
            return FileControllerTXT()
        elif fileType.upper() == FILE_TYPE_CSV.upper():
            return FileControllerCSV()
        elif fileType.upper() == FILE_TYPE_JSON.upper():
            return FileControllerJSON()
        return None