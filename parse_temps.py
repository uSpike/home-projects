import csv
import datetime
from collections import defaultdict

f = open("StnData.csv")
r = csv.reader(f)

cold = {}  # date: low temp

for row in r:
    if len(row) < 3:
        continue
    date, high, avg, low = row
    if low == "M":
        continue
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    low = int(low)
    # Jan, Feb, Mar, Apr
    if date.month in [1, 2, 3, 4, 5]:
        cold[date] = low

inside_temp = 60
greenhouse_area = 1760
greenhouse_heat_loss = 0.7  # inflated poly
heater_efficiency = 0.8
hours_per_night = 12
cost_per_gallon = 2.5  # LP
btu_per_gallon = 91000  # LP

years = defaultdict(int)  # year: total BTU

for date, low in cold.items():
    # assume 10 hour nights
    btu = greenhouse_area * greenhouse_heat_loss * (inside_temp - low) * hours_per_night
    years[date.year] += btu / heater_efficiency

for year, btu in years.items():
    print(f"{year}: {btu:0.0f} BTU {btu // btu_per_gallon:0.0f} gallons {btu // btu_per_gallon * cost_per_gallon:0.0f} dollars")