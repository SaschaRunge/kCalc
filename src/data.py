import os
import datetime

from csv_loader import CSVLoader

from enum import Enum
from parser import Parser

PATH_TO_FILE = "./data/input/input.csv"

class DataType(Enum):
    INTEGER = 0
    FLOAT = 1
    DATE = 2

class InvalidTypeException(Exception):
    pass
class InvalidInputException(Exception):
    pass

class Data():
    def __init__(self, filename = PATH_TO_FILE):
        self.source_data = {}       # raw input
        self.data = {}              # complete, normalized dataset

        self._import_from_csv(filename)
        self._normalize_data()
    
    def _import_from_csv(self, filename):
        csv_loader = CSVLoader(filename)
        self.source_data = csv_loader.load_as_dict()
        
        if(Data._has_duplicates(self.source_data["date"])):
            raise InvalidInputException(f"Error: Duplicate entries in column 'date' in '{filename}' are invalid.")

        #TODO: maybe handle missing values differently. This might make it a bit annoying to add single values to a dataset, might need to remove lines with empty values for calculation instead
        if (Data._has_empty_values(self.source_data["date"]) or
            Data._has_empty_values(self.source_data["kcal"]) or
            Data._has_empty_values(self.source_data["weight"])):
            raise InvalidInputException(f"Error: Dataset '{filename}' has missing values.")
    
    @staticmethod
    def _has_duplicates(data):
        """
        Do NOT use for floats.
        """
        return len(data) != len(set(data))

    @staticmethod
    def _has_empty_values(data):
        for value in data:
            if not value:
                return True
        return False

    def _normalize(self, strings, datatype):
        normalized_input = []
        try:
            for string in strings:
                match(datatype):
                    case DataType.INTEGER:
                        value = Parser.parse_int(string)
                    case DataType.FLOAT:
                        value = Parser.parse_float(string)
                    case DataType.DATE:
                        value = Parser.parse_date(string)
                    case _:
                        raise InvalidTypeException(f"Invalid datatype {datatype!r}.")
                normalized_input.append(value)
        except ValueError as e:
            raise InvalidInputException(f"Could not convert string to datatype {datatype!r} (likely due to invalid formatting of your .csv): {e}") 

        return normalized_input

    def _normalize_data(self):
        self.data["date"] = self._normalize(self.source_data["date"], DataType.DATE)
        self.data["kcal"] = self._normalize(self.source_data["kcal"], DataType.FLOAT)
        self.data["weight"] = self._normalize(self.source_data["weight"], DataType.FLOAT)

    def add(self, data, key):
        for _, v in self.data.items():
            if len(v) != len(data):
                raise NotImplementedError("TODO: Make sure to enforce consistent length for all lists stored in generated data (class Data).")
        self.data[key] = data

    def get_by_date(self, key, start_date, end_date=None):
        """
        Returns the specified data in column key between two dates. 
        
        If the end date is earlier than the start date, end date is set to start date.
        """

        dates = self.data["date"]

        if (key not in self.data or
            not dates):
            return []
        
        if not isinstance(start_date, datetime.date):
            start_date = Parser.parse_date(start_date)
        if end_date is None:
            end_date = start_date
        elif not isinstance(end_date, datetime.date):
            end_date = Parser.parse_date(end_date)

        if end_date < start_date:
            end_date = start_date

        return_values = []
        for i in range(len(dates)):
            if dates[i] >= start_date and dates[i] <= end_date:
                return_values.append(self.data[key][i])
            if dates[i] > end_date:
                break
        return return_values
    
    def get_window(self, key, start_date, days):
        """
        Returns data from date_start for the specified amount of days, date_start-inclusive.
        """

        dates = self.data["date"]

        if (days == 0 or 
            key not in self.data or 
            not dates):
            return []
        
        if not isinstance(start_date, datetime.date):
            start_date = Parser.parse_date(start_date)

        if days > 0:
            end_date = start_date + datetime.timedelta(days=(days - 1))
        elif days < 0:
            end_date = start_date + datetime.timedelta(days=(days + 1))
            start_date, end_date = end_date, start_date
      
        return self.get_by_date(key, start_date, end_date)

if __name__ == '__main__':
    Data()