"""
Calculate total daily photosynthetic photon flux (PPF) for a given location and date
"""

from datetime import datetime, timedelta
from pysolar.solar import get_altitude, radiation
from astral.sun import sun
from astral import LocationInfo

location_lat = 43.0731  # Latitude of Madison, WI
location_lon = -89.4012  # Longitude of Madison, WI

location = LocationInfo("Madison", "Wisconsin", "America/Chicago", location_lat, location_lon)
time_interval = 30 * 60  # Time interval in seconds (30 minutes)
irradiance_to_ppf = 2.1  # Conversion factor from solar irradiance (W/m2) to PPF (umol/m2/s)

def calculate_total_ppf(lat: float, lon: float, date: datetime) -> float:
    s = sun(location.observer, date, tzinfo=location.timezone)
    total_ppf = 0.0
    
    current_time = s['sunrise']
    while current_time <= s['sunset']:
        altitude = get_altitude(lat, lon, current_time)
        if altitude > 0:  # Only calculate if the sun is above the horizon
            solar_irradiance = radiation.get_radiation_direct(current_time, altitude)
            # Convert solar irradiance (W/m²) to PPFD (µmol/m²/s)
            ppf = solar_irradiance * irradiance_to_ppf
            total_ppf += ppf * (time_interval)

        current_time += timedelta(seconds=time_interval)

    return total_ppf / 1e6  # Convert from µmol to mol

def daterange(start_date: datetime, end_date: datetime):
    days = int((end_date - start_date).days)
    for n in range(days):
        yield start_date + timedelta(n)

for d in daterange(datetime(2024, 1, 1), datetime(2024, 7, 30)):
    total_ppf = calculate_total_ppf(location_lat, location_lon, d)
    print(f"Total PPF on {d}: {total_ppf:.2f} mol/m²")
