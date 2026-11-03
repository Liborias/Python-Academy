from datetime import date, timedelta         # z modulu datetime potřebujeme date a timedelta

narozeniny = date(2026, 12, 31)
dnes = date(2026, 10, 25)
print((narozeniny - dnes).days)               # 67: rozdíl dvou dat je timedelta, .days jsou dny

print(dnes + timedelta(days=10))              # 2026-11-04: posun o deset dní
print(dnes.strftime("%d. %m. %Y"))            # 25. 10. 2026: text podle předpisu
print(dnes.weekday())                         # 6: neděle (pondělí je 0)
