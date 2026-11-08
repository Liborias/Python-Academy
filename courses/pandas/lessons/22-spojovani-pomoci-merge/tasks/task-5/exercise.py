# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def spoj_dva_klice(prodeje, cenik):
    # TODO: vraťte výsledek podle zadání; vstupy neměňte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    a = pd.DataFrame({"den": ["2026-11-02", "2026-11-01"], "produkt": ["caj", "caj"], "kusy": [1, 3]})
    b = pd.DataFrame({"den": ["2026-11-01", "2026-11-02"], "produkt": ["caj", "caj"], "cena": [45.0, 48.0]})
    print(spoj_dva_klice(a, b))
