from datetime import date, timedelta

def den_tydne(rok, mesic, den):
    return date(rok, mesic, den).weekday()

print(den_tydne(2026, 11, 2))
