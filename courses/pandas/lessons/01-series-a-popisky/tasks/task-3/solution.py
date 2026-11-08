# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def prejmenuj_mereni(serie, nazev):
    return serie.rename(nazev)


# %% Vlastní ověření: tento blok se při importu neprovede.
if __name__ == "__main__":
    s = pd.Series([3, 5], index=["A", "B"], name="puvodni", dtype="float64")
    print(prejmenuj_mereni(s, "navstevy"))
