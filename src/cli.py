import sys
from csv_writer import CSVWriter
from dataset import DataSet
from application import Application

class CLI():
    def __init__(self):
        self.valid_input = {"add": ["add", "a"],
                    "remove": ["remove", "r"],
                    "show": ["show", "s"],
                    "read": ["read", "re"],
                    "write": ["write", "w"],
                    "quit": ["quit", "q"],
}
        self.application = Application()
        
    def run(self):
        print("")
        print(f"{' kCalc ':=^50}")
        print("")

        while True:
            cmd = input("> ")

            args = cmd.split()
            if args:
                cmd = args[0]
            if cmd in self.valid_input["add"]:
                if len(args) == 4:
                    date = args[1]
                    kcal = args[2]
                    weight = args[3]

                    try:
                        self.application.add(date, kcal, weight, True)
                    except ValueError as e:
                        print(f"\nInvalid arguments '{args}'. Could not add data.\n")
                else:
                    print(f"\nInvalid arguments '{args}'. Could not add data.\n")
            elif cmd in self.valid_input["remove"]:
                try:
                    if len(args) > 1 and self.application.remove(args[1]):
                        print(f"\n Removed at '{args[1]}'.\n")
                    else:
                        print(f"\nInvalid argument(s) for command 'r'. Usage: r (DATE). Date is either missing or invalid.\n")
                except ValueError as e:
                    print(f"\nCould not remove at '{args[1]}', argument 1 is no valid date: {e}\n")
            elif cmd in self.valid_input["show"]:
                self._show()
            elif cmd in self.valid_input["read"]:
                print(f"\nReading from '{self.application.input_path}'... .")
                if self.application.read():
                    print(f"Successful.\n")
                else:
                    print("Could not read file.\n")
            elif cmd in self.valid_input["write"]:
                print(f"\nWriting to file '{self.application.save_path}'... .")
                if self.application.write():
                    print(f"Successful.\n")
                else:
                    print("Could not write file.\n")
            elif cmd in self.valid_input["quit"]:
            #TODO: wrap try/except for invalid input
                print("\nExit.")
                self.application.exit()
                sys.exit(0)
            else:
                print("\nInvalid input. Please try again (or don't).\n")

    def _show(self):
        width = {"date": 14,
                "weight": 8,
                "kcal": 10,
                "default": 10}
        data = self.application.get_data()

        line = "|"
        for key in data:
            if key in width:
                line += f"{key:^{width[key]}}|"
            else:
                line += f"{key:^{width["default"]}}|"

        print("")
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



            
            


