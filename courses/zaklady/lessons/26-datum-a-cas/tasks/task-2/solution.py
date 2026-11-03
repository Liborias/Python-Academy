from datetime import date, timedelta

def posun(rok, mesic, den, dny):
    return (date(rok, mesic, den) + timedelta(days=dny)).strftime("%Y-%m-%d")

print(posun(2026, 12, 31, 1))
