import os
import sys
import csv
import datetime

from enum import Enum

PATH_TO_FILE = "./data/input/input.csv"

class DataType(Enum):
    INTEGER = 0
    FLOAT = 1
    DATE = 2

class Data():
    def __init__(self, filename = PATH_TO_FILE):
        self.source_data = {}
        self.generated_data = {}

        self._import_data_as_dict(filename)
        self._normalize_all_data()
    
    def _import_data_as_dict(self, filename):
        date = []
        kcal = []
        weight = []

        self.source_data = {}
        
        #TODO: abspath to csv
        
        try:
            with open(filename, newline='') as csvfile:
                csv_reader = csv.DictReader(csvfile)
                for row in csv_reader:
                    if("date" not in row.keys() or "weight" not in row.keys() or "kcal" not in row.keys()):
                        raise Exception(f"Missing or incomplete header in '{filename}'. Columns 'date', 'weight' and 'kcal' must exist.")
                    date.append(row["date"])
                    kcal.append(row["kcal"])
                    weight.append(row["weight"])
        except Exception as e:
            sys.exit(f"Error: Unable to read data from '{filename}':\n{e}")
                
        self.source_data["date"] = date
        self.source_data["kcal"] = kcal
        self.source_data["weight"] = weight   

    def _clean_string(self, string):
        if not string:
            return "0"
        string = string.translate(str.maketrans(',', '.', ' "!@#$'))
        return string
    
    def _try_convert_string_to_value(self, string, datatype):
        try:
            match(datatype):
                case DataType.INTEGER:
                    value = int(string)
                case DataType.FLOAT:
                    value = float(string)
                case DataType.DATE:
                    value = self._try_convert_string_to_date(string)
                case _:
                    raise Exception(f"Invalid datatype {datatype} in {os.path.abspath(__file__)} in {self._try_convert_string_to_value.__name__}.")
        except ValueError as e:
            sys.exit(f"ValueError: Could not convert string to datatype {datatype} (likely due to invalid formatting of your .csv): {e}")
        return value

    def _normalize_input(self, input, datatype):
        normalized_input = []
        for value in input:
            value = self._clean_string(value)
            normalized_input.append(self._try_convert_string_to_value(value, datatype))
        return normalized_input

    def _normalize_all_data(self):
        self.generated_data["date"] = self._normalize_input(self.source_data["date"], DataType.DATE)
        self.generated_data["kcal"] = self._normalize_input(self.source_data["kcal"], DataType.INTEGER)
        self.generated_data["weight"] = self._normalize_input(self.source_data["weight"], DataType.FLOAT)

    def add(self, data, key):
        for _, v in self.generated_data.items():
            if len(v) != len(data):
                raise NotImplementedError("TODO: Make sure to enforce consistent length for all lists stored in generated data (class Data).")
        self.generated_data[key] = data

    def get_by_date(self, key, date_from, date_to=None):
        if key not in self.generated_data.keys():
            return None
        if date_to is None:
            date_to = date_from
        if not isinstance(date_from, datetime.date):
            self._try_convert_string_to_date(date_from)
        if not isinstance(date_to, datetime.date):
            self._try_convert_string_to_date(date_to)


    def _try_convert_string_to_date(self, string):
        try:
            return datetime.date.fromisoformat(string)
        except ValueError as e:
            raise NotImplementedError(f"TODO: Handle failed string to date conversion in _try_convert_string_to_date: {e}")

if __name__ == '__main__':
    Data()