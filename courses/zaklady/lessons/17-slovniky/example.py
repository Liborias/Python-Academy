auto = {"znacka": "Škoda", "rok": 2019}      # slovník: dvojice klíč: hodnota
print(auto["znacka"])                         # čtení podle klíče: Škoda

auto["barva"] = "modrá"                       # klíč "barva" ještě neexistuje, tak vznikne
auto["rok"] = 2020                            # klíč "rok" existuje, hodnota se přepíše
print(auto)                                   # {'znacka': 'Škoda', 'rok': 2020, 'barva': 'modrá'}
print(len(auto))                              # počet dvojic: 3
