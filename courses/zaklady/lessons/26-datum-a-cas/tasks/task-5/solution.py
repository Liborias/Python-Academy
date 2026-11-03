from datetime import date, timedelta

def ceske_datum(rok, mesic, den):
    return date(rok, mesic, den).strftime("%d. %m. %Y")

print(ceske_datum(2026, 1, 2))
