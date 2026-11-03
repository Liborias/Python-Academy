text = "kocka pes kocka ptak kocka pes"
pocty = {}                                    # prázdný slovník na počty
for slovo in text.split():                    # split() rozdělí větu na seznam slov
    pocty[slovo] = pocty.get(slovo, 0) + 1    # chybějící slovo se bere jako 0, pak se přičte 1
print(pocty)                                  # {'kocka': 3, 'pes': 2, 'ptak': 1}

nejvic = max(pocty, key=pocty.get)            # klíč s největší hodnotou
print(nejvic, pocty[nejvic])                  # kocka 3
