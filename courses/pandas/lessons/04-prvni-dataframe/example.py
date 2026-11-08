# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def vytvor_tabulku(data):
    return pd.DataFrame(data)


# %% Vlastní ověření: tento blok se při importu neprovede.
if __name__ == "__main__":
    data = {"misto": ["Brno", "Praha"], "teplota": [18.5, 21.0]}
    print(vytvor_tabulku(data))
