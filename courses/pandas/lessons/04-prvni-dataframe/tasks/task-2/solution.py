# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def tabulka_ze_zaznamu(zaznamy, sloupce):
    return pd.DataFrame(zaznamy, columns=sloupce)


# %% Vlastní ověření: tento blok se při importu neprovede.
if __name__ == "__main__":
    radky = [{"misto": "Brno", "teplota": 18.5}, {"misto": "Praha", "teplota": 21.0}]
    print(tabulka_ze_zaznamu(radky, ["teplota", "misto"]))
