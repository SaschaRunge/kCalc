import unittest

from dataset import DataSet, InvalidInputException
from application import Application

FILEPATH = "./test_data/test_input.csv"

class TestApplication(unittest.TestCase):
    def test_convert_to_timedelta_as_days(self):
        dataset = DataSet(FILEPATH)
        data_is = Application()._convert_to_timedelta_as_days(dataset.get_copy("date"))
        data_should_be = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                            11, 12, 13, 14, 15, 16, 17, 18, 19,
                            20, 21, 22, 23, 24, 25, 26, 27, 28,
                            29, 30, 31, 50, 51, 52, 53, 54, 55, 
                            56, 57, 58, 59, 60, 61, 62, 63]
        self.assertEqual(data_is, data_should_be)
    
    def test_convert_to_timedelta_as_days_from_windows(self):
        dataset = DataSet(FILEPATH)
        data_is = Application()._convert_to_timedelta_as_days(dataset.get_window("date", "2025-05-08", 25))
        print(data_is)
        print(dataset.get_window("date", "2025-05-08", 25))
        #data_should_be = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                          #  11, 12, 13, 14, 15, 16, 17, 18, 19,
                       #     20, 21, 22, 23, 24, 25, 26, 27, 28,
                     #       29, 30, 31, 50, 51, 52, 53, 54, 55, 
                    #        56, 57, 58, 59, 60, 61, 62, 63]
        #self.assertEqual(data_is, data_should_be)
    
    def test_convert_to_timedelta_as_days_empty(self):
        data_is = Application()._convert_to_timedelta_as_days([])
        data_should_be =  []
        self.assertEqual(data_is, data_should_be)
