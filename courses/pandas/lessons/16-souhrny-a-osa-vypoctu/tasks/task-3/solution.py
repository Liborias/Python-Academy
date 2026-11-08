# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def pocet_dostupnych(tabulka, sloupce):
    return tabulka[sloupce].count().astype("int64")


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"rano": [10.0, None, None], "vecer": [14.0, 12.0, None], "misto": ["Brno", "Praha", "Zlín"]}, index=["B", "A", "C"])
    print(pocet_dostupnych(df, ["vecer", "rano"]))
