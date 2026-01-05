import datetime

class Parser():
    @staticmethod
    def _clean_string(string):
        if not string:
            return "0" #TODO probably should return None with subsequent clean up
        return string.translate(str.maketrans(',', '.', ' "!@#$'))
    #def _filter_argument(value):
        #if isinstance(int, value)

    
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
            raise NotImplementedError(f"TODO: Handle failed string to date conversion in Parser.parse_date: {e}")


    