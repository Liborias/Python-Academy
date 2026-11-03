from datetime import date, timedelta

def dny_od_zacatku(rok, mesic, den):
    return (date(rok, mesic, den) - date(rok, 1, 1)).days

print(dny_od_zacatku(2026, 1, 1))
