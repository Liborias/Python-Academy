# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def pojmenuj_radky(data, popisky):
    return pd.DataFrame(data, index=popisky)


# %% Vlastní ověření: tento blok se při importu neprovede.
if __name__ == "__main__":
    print(pojmenuj_radky({"teplota": [18.5, 21.0]}, ["Brno", "Praha"]))
