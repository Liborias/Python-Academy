# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def overene_ceny(prodeje, cenik):
    return prodeje.merge(cenik, on="produkt", how="left", sort=False, validate="many_to_one")


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    prodeje = pd.DataFrame({"produkt": ["caj", "kava", "novinka"], "kusy": [2, 3, 1]})
    cenik = pd.DataFrame({"produkt": ["kava", "caj"], "cena": [60.0, 45.0]})
    print(overene_ceny(prodeje, cenik))
