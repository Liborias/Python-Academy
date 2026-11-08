# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def rozmery_tabulky(tabulka):
    return tabulka.shape


# %% Vlastní ověření: tento blok se při importu neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"misto": ["Brno", "Praha"], "hodnota": [1, 2]})
    print(rozmery_tabulky(df))
