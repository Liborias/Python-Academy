# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def nesparovane_radky(prodeje, cenik):
    # TODO: vraťte výsledek podle zadání; vstupy neměňte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    a = pd.DataFrame({"produkt": ["caj", "voda", "novinka"], "kusy": [2, 1, 3]})
    b = pd.DataFrame({"produkt": ["caj", "voda"], "cena": [45.0, None]})
    print(nesparovane_radky(a, b))
