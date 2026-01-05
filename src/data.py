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

class DataSet():
    def __init__(self, filename = PATH_TO_FILE):
        self._source_data = {}       # raw input
        self._data = {}              # complete, normalized dataset

        self._import_from_csv(filename)
        self._normalize_data()

    def __len__(self):
        if not self._data:
            return 0
        first_value = next(iter(self._data.values()))
        return len(first_value)
    
    def _import_from_csv(self, filename):
        csv_loader = CSVLoader(filename)
        self._source_data = csv_loader.load_as_dict()
        
        if(DataSet._has_duplicates(self._source_data["date"])):
            raise InvalidInputException(f"Error: Duplicate entries in column 'date' in '{filename}' are invalid.")

        #TODO: maybe handle missing values differently. This might make it a bit annoying to add single values to a dataset, might need to remove lines with empty values for calculation instead
        if (DataSet._has_empty_values(self._source_data["date"]) or
            DataSet._has_empty_values(self._source_data["kcal"]) or
            DataSet._has_empty_values(self._source_data["weight"])):
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
    
    @staticmethod
    def _to_date(date) -> datetime.date:
        if isinstance(date, datetime.date):
            return date
        return Parser.parse_date(date)

    def _normalize(self, string, datatype):
            try:
                match(datatype):
                    case DataType.INTEGER:
                        value = Parser.parse_int(string)
                    case DataType.FLOAT:
                        value = Parser.parse_float(string)
                    case DataType.DATE:
                        value = Parser.parse_date(string)
                    case _:
                        raise InvalidTypeException(f"Invalid datatype {datatype!r}.")
            except ValueError as e:
                raise InvalidInputException(f"Could not convert string to datatype {datatype!r} (likely due to invalid formatting of your .csv): {e}") 
            return value

    def _normalize_list(self, strings, datatype):
        values = []
        for string in strings:
            values.append(self._normalize(string, datatype))
        return values

    def _normalize_data(self):
        self._data["date"] = self._normalize_list(self._source_data["date"], DataType.DATE)
        self._data["kcal"] = self._normalize_list(self._source_data["kcal"], DataType.FLOAT)
        self._data["weight"] = self._normalize_list(self._source_data["weight"], DataType.FLOAT)

    #TODO: implement tests
    def _has_constant_length(self):
        last_length = 0
        for key in self._data:
            if last_length != 0 and len(self._data[key]) != last_length:
                return False
            last_length = len(self._data[key])
        return True
    
    def _delete_point(self, key, date):
        """
        Don't use, just for testing.
        """

        if (key not in self._data):
            raise InvalidInputException(f"Key '{key}' does not exist. Do not call _delete_point.")
        date = DataSet._to_date(date)

        for i, value in enumerate(self._data["date"]):
            if value == date:
                del self._data[key][i]
                return True
        return False 
            
    def add_column(self, key, data):
        if len(self) != len(data):
            raise InvalidInputException("Failed to add data to DataSet; Provided data must match the length of the currently present data in DataSet.")
        self._data[key] = data #self._normalize_list(data, DataType.FLOAT)

    def add_row(self, overwrite=False, **kwargs):
        for key in kwargs:
            if key not in self._data:
                raise InvalidInputException(f"No such key '{key}' exists.")
        for key in self._data:
            if key not in kwargs:
                raise InvalidInputException(f"Input is missing values for key '{key}'.")
            
        #TODO: append to last row if no date (maybe)       
        if "date" not in kwargs:
            raise NotImplementedError()
        
        date = DataSet._to_date(kwargs["date"])
        dates = self._data["date"]
        for i in range(len(dates)):
            #TODO: normalize each element, not just date
            if date == dates[i]:
                for key in kwargs:
                    if key != "date":
                        self._data[key][i] = kwargs[key]
                    else:
                        self._data[key][i] = self._to_date(kwargs[key])
                break
            elif date > dates[i]: # first entry in chronological order if date is not present
                for key in kwargs:
                    if key != "date":
                        self._data[key].insert(i, kwargs[key])
                    else:
                        self._data[key].insert(i, self._to_date(kwargs[key]))
                break

    def get_copy(self, key):
        return self._data[key].copy()

    #TODO: migrate parsing responsibilty to higher level
    def get_by_date(self, key, start_date, end_date=None):
        """
        Returns the specified data in column key between two dates. 
        
        If the end date is earlier than the start date, end date is set to start date.
        """

        dates = self._data["date"]

        if (key not in self._data or
            not dates):
            return []
        
        start_date = DataSet._to_date(start_date)
        if end_date is None:
            end_date = start_date
        else:
            end_date = DataSet._to_date(end_date)

        if end_date < start_date:
            end_date = start_date

        return_values = []
        for i in range(len(dates)):
            if dates[i] >= start_date and dates[i] <= end_date:
                return_values.append(self._data[key][i])
            if dates[i] > end_date:
                break
        return return_values
    
    def get_window(self, key, start_date, days):
        """
        Returns data from start_date for the specified amount of days, start_date-inclusive.
        """

        dates = self._data["date"]

        if (days == 0 or 
            key not in self._data or 
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
    DataSet()