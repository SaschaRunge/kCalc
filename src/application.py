import copy
import os


from config_handler import ConfigHandler
from csv_writer import CSVWriter
from dataset import DataSet, InvalidInputException
from datetime import datetime
from math_m import Math_m

SAVE_PATH = "./data/generated/saved.csv"
INPUT_PATH = "./data/input/input.csv"
CONFIG_PATH = "./config.yaml"
DEFAULT_PATH = "./defaults.yaml"

class Application():
    def __init__(self):
        self.save_path = SAVE_PATH
        self.input_path = INPUT_PATH

        if os.path.isfile(self.save_path):
            self.dataset = DataSet(self.save_path)
        else:
            self.dataset = DataSet.empty()

        self.defaults = Application._load_config(DEFAULT_PATH, True)
        self.config = Application._load_config(CONFIG_PATH, False)

        #self_dataset_current = self.dataset

    @staticmethod
    def _load_config(yaml_file, is_default):
        try:
            return ConfigHandler.load(yaml_file)
        except FileNotFoundError as e:
            #TODO: Use default values
            if not is_default:
                print(f"Warning: {yaml_file} not found. Using default values instead.")
            else:
                raise FileNotFoundError(f"{yaml_file} is missing. Please copy from source: {e}")
    
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
    
    def get_last_known(self, key):
        return self.dataset.get_last(key)

    def trend_weight(self, start_date, days):
        """
        Trend or best fit for weight, starting from start_date going back in time by days.

        Returns a tuple (m, b) with the linear_least_squares solution to y = m * x + b for weight over the specified timeframe.
        The slope m directly corresponds to estimated weightloss per day.
        """

        x_as_dates = self.x_axis(start_date, days)
        x = Application._convert_to_timedelta_as_days(x_as_dates)
        y = self.dataset.get_window("weight", start_date, -days)

        return Math_m.linear_least_squares(x, y)
    
    def x_axis(self, start_date, days):
        """
        Wrapper to self.dataset.get_window("date", start_date, -days) (ensures x-axis alignement for any timeseries calculations).
        """
        return self.dataset.get_window("date", start_date, -days)
    
    def weekly_weight_loss(self):
        """
        Returns weekly_weight_loss as estimated by linear_least_squares. Since this requires at least 2 datapoints, returns None if there are not enough points.
        """
        try:
            days = self.from_config_get("calculation_interval_days")
            trend_m, _ = self.trend_weight(self.dataset.get_last("date"), days)
            return trend_m * 7000 # 7 days per week, 1000 g per kg
        except ValueError:
            return None
    
    def tdee(self):
        weight_loss = self.weekly_weight_loss()
        #TODO: replace by global loading of config not each individually
        days = self.from_config_get("calculation_interval_days")
        kcal_per_kg_fat = self.from_config_get("kcal_per_kg_fat")
        kcal_consumed = self.dataset.get_window("kcal", self.dataset.get_last("date"), -days) # 
        if not kcal_consumed:
            return None
        avg_kcal_consumed = sum(kcal_consumed)/len(kcal_consumed) # average daily calorie intake
        daily_calorie_deficit = weight_loss * kcal_per_kg_fat / 7000
        return avg_kcal_consumed - daily_calorie_deficit
    
    def tdee_adjusted(self):
        weekly_weight_loss_goal = self.from_config_get("weekly_weight_loss_goal")
        kcal_per_kg_fat = self.from_config_get("kcal_per_kg_fat")
        return self.tdee() - weekly_weight_loss_goal * kcal_per_kg_fat / 7000
    
    def import_config(self):
        raise NotImplementedError()

    @staticmethod
    def _convert_to_timedelta_as_days(dates):
        if not dates:
            return [] 
        
        days = []
        for date in dates:
            days.append((date - dates[0]).days)
        return days
    
    def from_config_get(self, key):
        try:
            return self.config[key]
        except KeyError:
            print(f"Warning: '{key}' missing in config.yaml. Using default value.")
            try:
                return self.defaults[key]
            except KeyError as e:
                print(f"{self.defaults=}")
                raise KeyError(f"No default found for '{key}'. Please redownload defaults.yaml and place it in the root directory of kCalc.")


    def exit(self):
        pass
         


