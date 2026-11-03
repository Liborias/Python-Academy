ukoly = [{"text": "uklidit", "hotovo": False}]
ukoly.append({"text": "uvařit", "hotovo": True})

for cislo, ukol in enumerate(ukoly, 1):          # enumerate(seznam, 1) číslování od 1
    znacka = "x" if ukol["hotovo"] else " "      # kratší zápis if/else do jedné řádky
    print(f"{cislo}. [{znacka}] {ukol['text']}")

casti = "pridej Koupit mléko".split(" ", 1)      # rozdělí jen na první mezeře
print(casti)                                     # ['pridej', 'Koupit mléko']
