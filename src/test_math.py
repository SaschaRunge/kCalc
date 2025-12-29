import unittest

from math_m import Math_m

class TestMath(unittest.TestCase):
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
