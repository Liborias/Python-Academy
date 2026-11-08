# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def vytvor_mereni(hodnoty, mista, nazev):
    return pd.Series(hodnoty, index=mista, name=nazev, dtype="float64")


# %% Vlastní ověření: tento blok se při importu neprovede.
if __name__ == "__main__":
    print(vytvor_mereni([18, 21.5, 16], ["Brno", "Praha", "Zlin"], "teplota"))
