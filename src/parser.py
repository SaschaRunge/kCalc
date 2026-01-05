import datetime

class Parser():
    @staticmethod
    def _clean_string(string):
        if not string:
            return "0" #TODO probably should return None with subsequent clean up
        return string.translate(str.maketrans(',', '.', ' "!@#$'))
    
    '''    
    @staticmethod
    def _preprocess(value):
        if isinstance(int, value) or isinstance(float, value):
            return value
        if isinstance(str, value):
            Parser._clean_string(value)
            try:
                return datetime.date.fromisoformat(value)
            except ValueError:
                try:
                    return Parser.parse_float(value)
                except ValueError:
                    return value
    '''
    
    @staticmethod
    def parse_int(string):
        return int(Parser._clean_string(string))

    @staticmethod
    def parse_float(string):
        return float(Parser._clean_string(string))
    
    @staticmethod
    def parse_date(string):
        try:
            return datetime.date.fromisoformat(string)
        except ValueError as e:
            raise ValueError(f"{string} is not a valid date format. Use YYYY-MM-DD. {e}")


    