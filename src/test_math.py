import unittest

from math_m import Math_m

class TestCalculateMovingAverage(unittest.TestCase):
    def test_calculate_moving_average_empty(self):
        data = []
        output_is = Math_m.calculate_moving_average(data, 5, 2)
        output_should_be = []
        self.assertEqual(output_is, output_should_be)
    
    def test_calculate_moving_average_single(self):
        data = [7]
        output_is = Math_m.calculate_moving_average(data, 5, 2)
        output_should_be = [7]
        self.assertEqual(output_is, output_should_be)

    def test_calculate_moving_average_no_offset(self):
        data = [10, 15, 12, 13, 15, 12, 21, 7, 10]
        output_is = Math_m.calculate_moving_average(data, 5)
        output_should_be = [10/1, 25/2, 37/3, 50/4, 65/5, 67/5, 73/5, 68/5, 65/5]
        self.assertEqual(output_is, output_should_be)

    def test_calculate_moving_average_no_offset_short(self):
        data = [10, 15, 12]
        output_is = Math_m.calculate_moving_average(data, 5)
        output_should_be = [10/1, 25/2, 37/3]
        self.assertEqual(output_is, output_should_be)

    def test_calculate_moving_average_offset_centered(self):
        data = [10, 15, 12, 13, 15, 12, 21, 7, 10]
        output_is = Math_m.calculate_moving_average(data, 5, 2)
        output_should_be = [37/3, 50/4, 65/5, 67/5, 73/5, 68/5, 65/5, 50/4, 38/3]
        self.assertEqual(output_is, output_should_be)
    
    def test_calculate_moving_average_offset_leading_only(self):
        data = [10, 15, 12, 13, 15, 12, 21, 7, 10]
        output_is = Math_m.calculate_moving_average(data, 5, 4)
        output_should_be = [sum(data[0:5])/5, sum(data[1:6])/5, sum(data[2:7])/5, 
                            sum(data[3:8])/5, sum(data[4:9])/5, sum(data[5:9])/4, 
                            sum(data[6:9])/3, sum(data[7:9])/2, data[8]]
        self.assertEqual(output_is, output_should_be)

    ''' Test does and probably should fail.
    def test_calculate_moving_average_missing_value(self):
        data = [10, 15, 12, '', 15, 12, 21, 7, 10]
        output_is = Math_m.calculate_moving_average(data, 5)
        output_should_be = [sum(data[0:1])/1, sum(data[0:2])/2, sum(data[0:3])/3,
                            sum(data[0:4])/4, sum(data[0:5])/5, sum(data[1:6])/5,
                            sum(data[2:7])/5, sum(data[3:8])/5, sum(data[4:9])/5]
        self.assertEqual(output_is, output_should_be) '''
    
class TestHelper(unittest.TestCase):
    def test_mulitply_lists(self):
        array1 = [1, 2, -3, 0]
        array2 = [4, 7, 2, 5]

        output_is = Math_m.mulitply_lists(array1, array2)
        output_should_be = [4, 14, -6, 0]
        self.assertEqual(output_is, output_should_be)

    def test_mulitply_lists_empty(self):
        array1 = []
        array2 = []

        output_is = Math_m.mulitply_lists(array1, array2)
        output_should_be = []
        self.assertEqual(output_is, output_should_be)

    def test_mulitply_lists_uneven(self):
        array1 = [1, 2, -3]
        array2 = [4, 7, 2, 5]

        self.assertRaises(ValueError, Math_m.mulitply_lists, array1, array2)

    def test_add_lists(self):
        array1 = [1, 2, -3, 0]
        array2 = [4, 7, 2, 5]

        output_is = Math_m.add_lists(array1, array2)
        output_should_be = [5, 9, -1, 5]
        self.assertEqual(output_is, output_should_be)

    def test_add_lists_empty(self):
        array1 = []
        array2 = []

        output_is = Math_m.add_lists(array1, array2)
        output_should_be = []
        self.assertEqual(output_is, output_should_be)

    def test_add_lists_uneven(self):
        array1 = [1, 2, -3]
        array2 = [4, 7, 2, 5]

        self.assertRaises(ValueError, Math_m.add_lists, array1, array2)

    def test_subtract_lists(self):
        array1 = [1, 9, -3, 0]
        array2 = [4, 7, 2, 5]

        output_is = Math_m.subtract_lists(array1, array2)
        output_should_be = [-3, 2, -5, -5]
        self.assertEqual(output_is, output_should_be)

    def test_subtract_lists_empty(self):
        array1 = []
        array2 = []

        output_is = Math_m.subtract_lists(array1, array2)
        output_should_be = []
        self.assertEqual(output_is, output_should_be)

    def test_subtract_lists_uneven(self):
        array1 = [1, 2, -3]
        array2 = [4, 7, 2, 5]

        self.assertRaises(ValueError, Math_m.subtract_lists, array1, array2)

class TestLinearLeastSquares(unittest.TestCase):
    def test_linear_least_squares_very_short(self):
        x_values = [1, 2]
        y_values = [2, 3]

        output_is = Math_m.linear_least_squares(x_values, y_values)
        output_should_be = (1, 1)
        self.assertEqual(output_is, output_should_be)

    def test_linear_least_squares_short(self):
        x_values = [1, 2, 3, 4]
        y_values = [6, 5, 7, 10]

        output_is = Math_m.linear_least_squares(x_values, y_values)
        output_should_be = (1.4, 3.5)
        self.assertEqual(output_is, output_should_be)

    def test_linear_least_squares_long(self):
        x_values = [1.47, 1.50, 1.52, 1.55, 1.57, 1.60, 1.63, 1.65, 1.68, 1.70, 1.73, 1.75, 1.78, 1.80, 1.83]
        y_values = [52.21, 53.12, 54.48, 55.84, 57.20, 58.57, 59.93, 61.29, 63.11, 64.47, 66.28, 68.10, 69.92, 72.19, 74.46]

        output_is = Math_m.linear_least_squares(x_values, y_values)
        output_should_be = (61.272, -39.062)
        self.assertAlmostEqual(output_is[0], output_should_be[0], 3)
        self.assertAlmostEqual(output_is[1], output_should_be[1], 3)

    def test_linear_least_squares_flat(self):
        x_values = [1, 2, 3, 4, 5, 6]
        y_values = [5, 5, 5, 5, 5, 5]

        output_is = Math_m.linear_least_squares(x_values, y_values)
        output_should_be = (0, 5)
        self.assertEqual(output_is, output_should_be)

    def test_linear_least_squares_empty(self):
        x_values = []
        y_values = []

        self.assertRaises(ValueError, Math_m.linear_least_squares, x_values, y_values)
    
    def test_linear_least_squares_lone_pair(self):
        x_values = [1]
        y_values = [5]

        self.assertRaises(ValueError, Math_m.linear_least_squares, x_values, y_values)

