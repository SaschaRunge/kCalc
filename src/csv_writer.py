import csv

#TODO: safe implementation via tempfile
class CSVWriter():
    def __init__(self, file):
        self.file = file

    def write(self, data: dict, file=None):
        if file is None:
            file = self.file

        with open(file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            writer.writerow(list(data.keys()))
            for i in range(len(data["date"])):
                row = []
                for value in data.values():
                    row.append(value[i])
                writer.writerow(row)

            
            #for value in data["date"]
