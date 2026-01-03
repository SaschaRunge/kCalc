from data import Data
from math_m import Math_m

def main():
    data = Data()

    #data.add(data.generated_data["weight"][:5], "weight_too")
    #print(data.generated_data["date"])
    #moving_avg_kcal = Math_m.calculate_moving_average(data.generated_data["date"], 7)
    #print(list(map(lambda x: round(x, 2), moving_avg_kcal)))

    #print(data.get_by_date("weight", "2025-04-14", "2025-04-17"))

    #data._normalize_input("hey", "PENIS")

if __name__ == '__main__':
    main()