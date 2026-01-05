import unittest
import datetime

from data import DataSet, InvalidInputException

FILEPATH = "./test_data/test_input.csv"

class TestDataSet(unittest.TestCase):
    def test_get_data_by_date_empty_before(self):
        data = DataSet(FILEPATH)
        data_is = data.get_by_date("weight", "2024-04-11", "2024-04-22")
        data_should_be =  []
        self.assertEqual(data_is, data_should_be)

    def test_get_data_by_date_empty_after(self):
        data = DataSet(FILEPATH)
        data_is = data.get_by_date("weight", "2028-04-11", "2028-04-22")
        data_should_be =  []
        self.assertEqual(data_is, data_should_be)

    def test_get_data_by_date_empty_inbetween(self):
        data = DataSet(FILEPATH)
        data_is = data.get_by_date("weight", "2025-05-15", "2025-05-25")
        data_should_be =  []
        self.assertEqual(data_is, data_should_be)

    def test_get_data_by_date(self):
        data = DataSet(FILEPATH)
        data_is = data.get_by_date("weight", "2025-04-11", "2025-04-22")
        data_should_be =  [96.4, 96.4, 96.4, 96.8, 96.3, 95.8, 95.1, 95.5, 96.7, 96.7, 96.7, 96]
        self.assertEqual(data_is, data_should_be)

    def test_get_data_by_date_enclosing_missing_values(self):
        data = DataSet(FILEPATH)
        data_is = data.get_by_date("date", "2025-05-08", "2025-06-01")
        data_should_be = [datetime.date.fromisoformat("2025-05-08"), datetime.date.fromisoformat("2025-05-09"), datetime.date.fromisoformat("2025-05-10"), 
                          datetime.date.fromisoformat("2025-05-29"), datetime.date.fromisoformat("2025-05-30"), datetime.date.fromisoformat("2025-05-31"), 
                          datetime.date.fromisoformat("2025-06-01")]
        self.assertEqual(data_is, data_should_be)

    def test_get_data_by_date_into_missing_values(self):
        data = DataSet(FILEPATH)
        data_is = data.get_by_date("kcal", "2025-05-08", "2025-05-22")
        data_should_be = [2861, 2325, 2537]
        self.assertEqual(data_is, data_should_be)

    def test_get_data_by_date_single_front(self):
        data = DataSet(FILEPATH)
        data_is = data.get_by_date("date", "2025-04-09")
        data_should_be = [datetime.date.fromisoformat("2025-04-09")]
        self.assertEqual(data_is, data_should_be)

    def test_get_data_by_date_single_back(self):
        data = DataSet(FILEPATH)
        data_is = data.get_by_date("date", "2025-06-11")
        data_should_be = [datetime.date.fromisoformat("2025-06-11")]
        self.assertEqual(data_is, data_should_be)

    def test_get_data_by_date_single_somewhere(self):
        data = DataSet(FILEPATH)
        data_is = data.get_by_date("kcal", "2025-05-05")
        data_should_be = [2286]
        self.assertEqual(data_is, data_should_be)

    def test_get_window_single(self):
        data = DataSet(FILEPATH)
        data_is = data.get_window("kcal", "2025-05-05", 1)
        data_should_be = [2286]
        self.assertEqual(data_is, data_should_be)

    def test_get_window_forward(self):
        data = DataSet(FILEPATH)
        data_is = data.get_window("kcal", "2025-05-05", 5)
        data_should_be = [2286, 2572, 2258, 2861, 2325]
        self.assertEqual(data_is, data_should_be)

    def test_get_window_backward(self):
        data = DataSet(FILEPATH)
        data_is = data.get_window("kcal", "2025-05-05", -5)
        data_should_be = [2256, 2196, 2493, 2510, 2286] # going backward still orders chronologically, which is intended
        self.assertEqual(data_is, data_should_be)
    
    def test_get_window_into_missing_values(self):
        data = DataSet(FILEPATH)
        data_is = data.get_window("kcal", "2025-05-08", 15)
        data_should_be = [2861, 2325, 2537]
        self.assertEqual(data_is, data_should_be)

    def test_get_window_into_key_missing(self):
        data = DataSet(FILEPATH)
        data_is = data.get_window("thisdoesnotexist", "2025-05-08", 15)
        data_should_be = []
        self.assertEqual(data_is, data_should_be)

    def test_data_has_duplicates_true(self):
        data = ["2025-05-06","2025-05-07", "2025-05-08", "2025-05-08", "2025-05-12"]
        self.assertTrue(DataSet._has_duplicates(data))

    def test_data_has_duplicates_false(self):
        data = ["2025-05-06","2025-05-07", "2025-05-08", "2025-05-010", "2025-05-12"]
        self.assertFalse(DataSet._has_duplicates(data))

    def test_data_delete_point(self):
        data = DataSet(FILEPATH)
        self.assertTrue(data._delete_point("kcal", "2025-04-19"))
        data_is = data.get_window("kcal", "2025-04-17", 10)
        data_should_be = [1967, 2200, 2119, 2149, 2752, 2252, 1730, 3779, 1612, 3916]
        self.assertEqual(data_is, data_should_be)

    def test_data_delete_point_multiple(self):
        data = DataSet(FILEPATH)
        self.assertTrue(data._delete_point("kcal", "2025-04-19"))
        self.assertTrue(data._delete_point("kcal", "2025-04-25"))
        data_is = data.get_window("kcal", "2025-04-17", 10)
        data_should_be = [1967, 2200, 2119, 2149, 2752, 2252, 1730, 3779, 3916, 1138] # weird things happening when multiple points get deleted, because lists are of uneven length
        self.assertEqual(data_is, data_should_be)
    
    def test_data_delete_point_None(self):
        data = DataSet(FILEPATH)
        self.assertFalse(data._delete_point("kcal", "1989-04-19"))
    
    def test_data_delete_point_twice(self):
        data = DataSet(FILEPATH)
        self.assertTrue(data._delete_point("date", "2025-04-19"))
        self.assertFalse(data._delete_point("date", "2025-04-19"))

    def test_data_has_constant_length_true(self):
        data = DataSet(FILEPATH)
        self.assertTrue(data._has_constant_length())

    def test_data_has_constant_length_true_additional_keys(self):
        data = DataSet(FILEPATH)
        data._data["copy_of_weight"] = data.get_copy("weight")
        data._data["copy_of_kcal"] = data.get_copy("kcal")
        self.assertTrue(data._has_constant_length())
    
    def test_data_has_constant_length_false(self):
        data = DataSet(FILEPATH)
        data._delete_point("kcal", "2025-04-19")
        self.assertFalse(data._has_constant_length())

    def test_data_has_constant_length_false_additional_keys(self):
        data = DataSet(FILEPATH)
        data._data["do_not_do_this"] = ["this", "is", "a", "test"]
        data._data["really"] = ["this", "is", "a", "test still"]
        data._data["really really"] = ["just", "adding data", "of", "length four"]
        self.assertFalse(data._has_constant_length())

    def test_data_get_copy_immutable(self):
        data = DataSet(FILEPATH)
        data._data["copy_of_kcal"] = data.get_copy("kcal")
        data._delete_point("kcal", "2025-04-19")
        self.assertNotEqual(len(data._data["kcal"]), len(data._data["copy_of_kcal"]))

    def test_data_add_column(self):
        data = DataSet(FILEPATH)
        new_column = [97.7, 96.4, 96.4, 96.4, 96.4, 96.8, 96.3, 
                      95.8, 95.1, 95.5, 96.7, 96.7, 96.7, 96.0, 
                      96.0, 94.6, 95.3, 95.8, 95.7, 96.2, 95.4, 
                      95.1, 94.6, 91.1, 94.2, 94.2, 95.5, 95.9, 
                      95.4, 95.4, 94.5, 94.2, 91.8, 92.6, 91.8, 
                      91.5, 105.0, 23.0, 91.1, 92.2, 91.5, 91.5, 
                      91.5, 91.5, 91.5, 1.0]
        data.add_column("made_up", new_column)
        self.assertTrue(data._has_constant_length())
        self.assertTrue(len(data._data.keys()) == 4)

    def test_data_add_column_multiple(self):
        data = DataSet(FILEPATH)
        new_column1 = [97.7, 96.4, 96.4, 96.4, 96.4, 96.8, 96.3, 
                      95.8, 95.1, 95.5, 96.7, 96.7, 96.7, 96.0, 
                      96.0, 94.6, 95.3, 95.8, 95.7, 96.2, 95.4, 
                      95.1, 94.6, 91.1, 94.2, 94.2, 95.5, 95.9, 
                      95.4, 95.4, 94.5, 94.2, 91.8, 92.6, 91.8, 
                      91.5, 105.0, 23.0, 91.1, 92.2, 91.5, 91.5, 
                      91.5, 91.5, 91.5, 1.0]
        new_column2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 
                      13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 
                      23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 
                      33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 
                      43, 44, 45]
        data.add_column("made_up", new_column1)
        data.add_column("once_again", new_column2)
        self.assertTrue(data._has_constant_length())
        self.assertTrue(len(data._data.keys()) == 5)
        self.assertEqual(new_column1, data.get_copy("made_up"))
        self.assertEqual(new_column2, data.get_copy("once_again"))

    def test_data_add_column_fails(self):
        data = DataSet(FILEPATH)
        new_column = [97.7, 96.4, 96.4, 96.4, 96.4, 96.8, 96.3, 
                      95.8, 95.1, 95.5, 96.7, 96.7, 96.7, 96.0]
        self.assertRaises(InvalidInputException, data.add_column, "this_should_fail", new_column)

    def test_data_add_row_kwargs_not_matching_data(self):
        data = DataSet(FILEPATH)
        self.assertRaises(InvalidInputException, data.add_row, date="2025-04-19", weight=97, kcal=2200, the_meaning_of_life_the_universe_and_everything=42)

    def test_data_add_row_data_not_matchin_kwargs(self):
        data = DataSet(FILEPATH)
        self.assertRaises(InvalidInputException, data.add_row, weight=97, kcal=2200)

    def test_data_add_row_append(self):
        data = DataSet(FILEPATH)
        data.add_row(date="2025-06-12", weight=100, kcal=2200)
        weight_is = data.get_window("weight", "2025-06-08", 10)
        weight_should_be = [91.5, 91.5, 91.5, 90.9, 100]
        kcal_is = data.get_window("kcal", "2025-06-08", 10)
        kcal_should_be = [2811, 2313, 1811, 2818, 2200]
        self.assertEqual(weight_is, weight_should_be)
        self.assertEqual(kcal_is, kcal_should_be)


