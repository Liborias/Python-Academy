# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def nacti_bez_hlavicky(cesta):
    return pd.read_csv(cesta, sep=";", decimal=",", encoding="utf-8", header=None, names=["misto", "hodnota"])


# %% Vlastní ověření: tento blok se při importu neprovede.
if __name__ == "__main__":
    print(nacti_bez_hlavicky("bez-hlavicky.csv"))
