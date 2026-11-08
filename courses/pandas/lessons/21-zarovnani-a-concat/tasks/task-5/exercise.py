# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def spoj_serie(prvni, druha):
    # TODO: vraťte výsledek podle zadání; vstupy neměňte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    a = pd.Series([18.0, 21.0], index=["Brno", "Praha"], name="teplota", dtype="float64")
    b = pd.Series([19.0], index=["Brno"], name="teplota", dtype="float64")
    print(spoj_serie(a, b))
