class Math_m():
    ### Calculates the moving average at datapoint i for n values. The moving average at datapoint i is calculated with the datapoints between i - n + offset and i + offset. ###
    ### If there's not enough datapoints within the given range it will shorten the length of n to fit the data.                                                              ###
    @staticmethod
    def calculate_moving_average(data, n, offset=0):
        result = []
        for i in range(len(data)):
            lower_boundary = max(0, i - n + offset + 1)
            upper_boundary = min(len(data), i + offset + 1) 

            moving_average = sum(data[lower_boundary:upper_boundary])/(upper_boundary - lower_boundary)

            result.append(moving_average)  
        return result
    
    ### https://en.wikipedia.org/wiki/Simple_linear_regression ###
    ### fit data to y = m * x + b                              ###
    @staticmethod
    def linear_least_squares(x_values, y_values):
        if not x_values or not y_values:
            raise ValueError(f"Invalid call on Math_m.linear_least_squares. Arguments must not be empty or None.")
        if len(x_values) != len(y_values):
            raise ValueError(f"Uneven length of lists provided to Math_m.linear_least_squares: ({len(x_values)} != {len(y_values)})")
        if len(x_values) == 1:
            raise ValueError(f"Invalid call on Math_m.linear_least_squares. Linear regression is not possible on a single x-y-pair.")

        s_x = sum(x_values)
        s_y = sum(y_values)
        s_xx = sum(Math_m.mulitply_lists(x_values, x_values))
        s_yy = sum(Math_m.mulitply_lists(y_values, y_values))
        s_xy = sum(Math_m.mulitply_lists(x_values, y_values))

        n = len(x_values)

        m = (n * s_xy - s_x * s_y) / (n * s_xx - s_x ** 2)
        b =  1 / n * s_y - m / n * s_x
        
        return m, b
    
    @staticmethod
    def mulitply_lists(list1, list2):
        result = []

        if len(list1) != len(list2):
            raise ValueError(f"Uneven length of lists provided to Math_m.multiply_lists: ({len(list1)} != {len(list2)})")

        for value1, value2 in zip(list1, list2):
            result.append(value1 * value2)

        return result
    
    @staticmethod
    def add_lists(list1, list2):
        result = []

        if len(list1) != len(list2):
            raise ValueError(f"Uneven length of lists provided to Math_m.add_lists: ({len(list1)} != {len(list2)})")

        for value1, value2 in zip(list1, list2):
            result.append(value1 + value2)

        return result
    
    @staticmethod
    def subtract_lists(list1, list2):
        result = []

        if len(list1) != len(list2):
            raise ValueError(f"Uneven length of lists provided to Math_m.subtract_lists: ({len(list1)} != {len(list2)})")

        for value1, value2 in zip(list1, list2):
            result.append(value1 - value2)

        return result
