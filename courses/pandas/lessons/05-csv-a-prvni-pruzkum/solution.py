# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def nacti_mereni(cesta):
    return pd.read_csv(cesta, sep=";", decimal=",", encoding="utf-8")


# %% Vlastní ověření: tento blok se při importu neprovede.
if __name__ == "__main__":
    print(nacti_mereni("mereni.csv"))
