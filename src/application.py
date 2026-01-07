import copy
import os

from csv_writer import CSVWriter
from dataset import DataSet, InvalidInputException

SAVE_PATH = "./data/generated/saved.csv"
INPUT_PATH = "./data/input/input.csv"

class Application():
    def __init__(self):
        self.save_path = SAVE_PATH
        self.input_path = INPUT_PATH

        if os.path.isfile(self.save_path):
            self.dataset = DataSet(self.save_path)
        else:
            self.dataset = DataSet.empty()

        self_dataset_current = self.dataset
    
    def read(self, file=INPUT_PATH):
        try:
            self.dataset.read(file)
            return True
        #TODO: evaluate type of error
        except Exception as e:
            print(f"Could not read from file: {e}")
        return False

    def write(self, file=None):
        if file is None:
            file = self.save_path
        data = self.get_data()

        try:
            writer = CSVWriter(file)
            writer.write(data)
            return True
        #TODO: evaluate type of error
        except Exception as e:
            print(f"Could not write to file: {e}")
        return False

    def add(self, date, kcal, weight, overwrite=False):
        try:
            self.dataset.add_row(overwrite, date=date, kcal=kcal, weight=weight)
            return True
        except InvalidInputException:
            return False
    
    def remove(self, date):
        try:
            self.dataset.delete_row(date)
            return True
        except InvalidInputException:
            return False
    
    def get_data(self):
        return copy.deepcopy(self.dataset.get())
    
    def exit(self):
        pass
         


