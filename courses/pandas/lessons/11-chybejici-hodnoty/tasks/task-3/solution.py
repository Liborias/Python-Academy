# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def odstran_neuplne(tabulka, sloupce):
    return tabulka.dropna(subset=sloupce)


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"misto": ["Brno", None, ""], "teplota": [0.0, None, 18.5]}, index=["C", "A", "B"])
    print(odstran_neuplne(df, ["misto"]))
