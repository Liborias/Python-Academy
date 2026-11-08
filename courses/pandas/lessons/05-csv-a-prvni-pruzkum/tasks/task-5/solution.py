# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def pocet_zaznamu(cesta):
    return len(pd.read_csv(cesta, sep=";", decimal=",", encoding="utf-8"))


# %% Vlastní ověření: tento blok se při importu neprovede.
if __name__ == "__main__":
    print(pocet_zaznamu("mereni.csv"))
