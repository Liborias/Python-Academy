# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def seznam_sloupcu(tabulka):
    return tabulka.columns.tolist()


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"misto": ["Brno", "Praha", "Zlín"], "teplota": [18.5, 21.0, 16.5]}, index=["B", "A", "C"])
    print(seznam_sloupcu(df))
