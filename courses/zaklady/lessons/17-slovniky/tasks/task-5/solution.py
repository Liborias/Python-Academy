def zmen_cenu(zbozi, nova_cena):
    zbozi["cena"] = nova_cena
    return zbozi

print(zmen_cenu({'cena': 10}, 25))
