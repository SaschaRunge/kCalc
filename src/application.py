import os
from dataset import DataSet

SAVE_PATH = "./data/generated/saved.csv"
PATH_TO_INPUT = "./data/input/input.csv"

class Application():
    def __init__(self):
        self.save_path = SAVE_PATH
        if os.path.isfile(self.save_path):
            self.dataset = DataSet(self.save_path)
        else:
            self.dataset = DataSet.empty()
    
    def load(self, file):
        self.dataset.load(file)
         


