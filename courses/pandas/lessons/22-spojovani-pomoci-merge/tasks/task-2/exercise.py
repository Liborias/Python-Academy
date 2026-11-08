# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def jen_zname_produkty(prodeje, cenik):
    # TODO: vraťte výsledek podle zadání; vstupy neměňte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    prodeje = pd.DataFrame({"produkt": ["caj", "kava", "novinka"], "kusy": [2, 3, 1]})
    cenik = pd.DataFrame({"produkt": ["kava", "caj"], "cena": [60.0, 45.0]})
    print(jen_zname_produkty(prodeje, cenik))
