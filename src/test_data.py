import unittest
import datetime

from data import Data

FILEPATH = "./test_data/test_input.csv"

class TestData(unittest.TestCase):
    def test_get_data_by_date_empty_before(self):
        data = Data(FILEPATH)
        data_is = data.get_by_date("weight", "2024-04-11", "2024-04-22")
        data_should_be =  []
        self.assertEqual(data_is, data_should_be)

    def test_get_data_by_date_empty_after(self):
        data = Data(FILEPATH)
        data_is = data.get_by_date("weight", "2028-04-11", "2028-04-22")
        data_should_be =  []
        self.assertEqual(data_is, data_should_be)

    def test_get_data_by_date_empty_inbetween(self):
        data = Data(FILEPATH)
        data_is = data.get_by_date("weight", "2025-05-15", "2025-05-25")
        data_should_be =  []
        self.assertEqual(data_is, data_should_be)

    def test_get_data_by_date(self):
        data = Data(FILEPATH)
        data_is = data.get_by_date("weight", "2025-04-11", "2025-04-22")
        data_should_be =  [96.4, 96.4, 96.4, 96.8, 96.3, 95.8, 95.1, 95.5, 96.7, 96.7, 96.7, 96]
        self.assertEqual(data_is, data_should_be)

    def test_get_data_by_date_enclosing_missing_values(self):
        data = Data(FILEPATH)
        data_is = data.get_by_date("date", "2025-05-08", "2025-06-01")
        data_should_be = [datetime.date.fromisoformat("2025-05-08"), datetime.date.fromisoformat("2025-05-09"), datetime.date.fromisoformat("2025-05-10"), 
                          datetime.date.fromisoformat("2025-05-29"), datetime.date.fromisoformat("2025-05-30"), datetime.date.fromisoformat("2025-05-31"), 
                          datetime.date.fromisoformat("2025-06-01")]
        self.assertEqual(data_is, data_should_be)

    def test_get_data_by_date_into_missing_values(self):
        data = Data(FILEPATH)
        data_is = data.get_by_date("kcal", "2025-05-08", "2025-05-22")
        data_should_be = [2861, 2325, 2537]
        self.assertEqual(data_is, data_should_be)

    def test_get_data_by_date_single_front(self):
        data = Data(FILEPATH)
        data_is = data.get_by_date("date", "2025-04-09")
        data_should_be = [datetime.date.fromisoformat("2025-04-09")]
        self.assertEqual(data_is, data_should_be)

    def test_get_data_by_date_single_back(self):
        data = Data(FILEPATH)
        data_is = data.get_by_date("date", "2025-06-11")
        data_should_be = [datetime.date.fromisoformat("2025-06-11")]
        self.assertEqual(data_is, data_should_be)

    def test_get_data_by_date_single_somewhere(self):
        data = Data(FILEPATH)
        data_is = data.get_by_date("kcal", "2025-05-05")
        data_should_be = [2286]
        self.assertEqual(data_is, data_should_be)

    def test_get_window_single(self):
        data = Data(FILEPATH)
        data_is = data.get_window("kcal", "2025-05-05", 1)
        data_should_be = [2286]
        self.assertEqual(data_is, data_should_be)

    def test_get_window_forward(self):
        data = Data(FILEPATH)
        data_is = data.get_window("kcal", "2025-05-05", 5)
        data_should_be = [2286, 2572, 2258, 2861, 2325]
        self.assertEqual(data_is, data_should_be)

    def test_get_window_backward(self):
        data = Data(FILEPATH)
        data_is = data.get_window("kcal", "2025-05-05", -5)
        data_should_be = [2256, 2196, 2493, 2510, 2286] # going backward still orders chronologically, which is intended
        self.assertEqual(data_is, data_should_be)
    
    def test_get_window_into_missing_values(self):
        data = Data(FILEPATH)
        data_is = data.get_window("kcal", "2025-05-08", 15)
        data_should_be = [2861, 2325, 2537]
        self.assertEqual(data_is, data_should_be)

    def test_get_window_into_key_missing(self):
        data = Data(FILEPATH)
        data_is = data.get_window("thisdoesnotexist", "2025-05-08", 15)
        data_should_be = []
        self.assertEqual(data_is, data_should_be)

    def test_data_has_duplicates(self):
        data = ["2025-05-06","2025-05-07", "2025-05-08", "2025-05-08", "2025-05-12"]
        self.assertTrue(Data._has_duplicates(data))

    def test_data_has_no_duplicates(self):
        data = ["2025-05-06","2025-05-07", "2025-05-08", "2025-05-010", "2025-05-12"]
        self.assertFalse(Data._has_duplicates(data))


