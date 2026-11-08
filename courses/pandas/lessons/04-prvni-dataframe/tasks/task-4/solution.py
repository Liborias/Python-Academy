# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def prvni_radky(tabulka, pocet):
    return tabulka.head(pocet).copy()


# %% Vlastní ověření: tento blok se při importu neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"misto": ["Brno", "Praha", "Zlin"], "teplota": [18.5, 21.0, 16.0]})
    print(prvni_radky(df, 2))
