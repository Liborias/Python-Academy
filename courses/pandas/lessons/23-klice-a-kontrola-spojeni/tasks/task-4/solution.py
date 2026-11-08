# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def nesparovane_radky(prodeje, cenik):
    spojene = prodeje.merge(cenik, on="produkt", how="left", sort=False, indicator=True)
    return spojene.loc[spojene["_merge"] == "left_only", prodeje.columns].reset_index(drop=True)


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    a = pd.DataFrame({"produkt": ["caj", "voda", "novinka"], "kusy": [2, 1, 3]})
    b = pd.DataFrame({"produkt": ["caj", "voda"], "cena": [45.0, None]})
    print(nesparovane_radky(a, b))
