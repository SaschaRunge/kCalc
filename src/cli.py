import sys
from csv_writer import CSVWriter
from dataset import DataSet

PATH_TO_FILE = "./data/generated/output.csv"

class CLI():
    def __init__(self, dataset):
        self.dataset = dataset

        self.valid_input = {"quit": ["quit", "q"],
                            "show": ["show", "s"],
                            "write": ["write", "w"],
                            "add": ["add", "a"],
                            "remove": ["remove", "r"]}

        print("")
        print(f"{' kCalc ':=^50}")
        print("")
        
    def run(self):
        while True:
            cmd = input("> ")
            args = cmd.split()
            if args:
                cmd = args[0]
            if cmd in self.valid_input["quit"]:
                sys.exit(0)
            if cmd in self.valid_input["show"]:
                self._show()
            if cmd in self.valid_input["write"]:
                self._write(PATH_TO_FILE)
            #TODO: wrap try/except for invalid input
            if cmd in self.valid_input["add"]:
                if len(args) == 4:
                    date = args[1]
                    kcal = args[2]
                    weight = args[3]

                    try:
                        self._add(date, kcal, weight, True)
                    except ValueError as e:
                        print(f"Invalid arguments '{args}'. Could not add data.")
                else:
                    print(f"Invalid arguments '{args}'. Could not add data.")
            if cmd in self.valid_input["remove"]:
                try:
                    #TODO: check false
                    self._remove(args[1])
                except ValueError as e:
                    print(f"Could not remove at '{args[1]}', argument 1 is no valid date: {e}")

    def _show(self):
        width = {"date": 14,
                "weight": 8,
                "kcal": 10,
                "default": 10}
        data = self.dataset.get()

        line = "|"
        for key in data:
            if key in width:
                line += f"{key:^{width[key]}}|"
            else:
                line += f"{key:^{width["default"]}}|"
        print(line)
        print(f"{'':=^{len(line)}}")

        for i in range(len(data["date"])):
            line = "|"
            for key, values in data.items():
                if key in width:
                    line += f"{str(values[i]):^{width[key]}}|"
                else:
                    line += f"{str(values[i]):^{width["default"]}}|"
            print(line)
        print("")
    
    def _write(self, file):
        data = self.dataset.get()

        print(f"Writing to file '{file}... .")
        try:
            writer = CSVWriter(file)
            writer.write(data)
            print(f"Successful.")
        #TODO: evaluate type of error
        except Exception as e:
            print(f"Could not write to file: {e}")

    def _add(self, date, kcal, weight, overwrite=False):
        self.dataset.add_row(overwrite, date=date, kcal=kcal, weight=weight)
        
    def _remove(self, date):
        self.dataset.delete_row(date)




            
            


