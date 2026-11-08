# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def soucty_sloupcu(tabulka, sloupce):
    return tabulka[sloupce].sum(axis=0, min_count=1).astype("float64")


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"rano": [10.0, None, None], "vecer": [14.0, 12.0, None], "misto": ["Brno", "Praha", "Zlín"]}, index=["B", "A", "C"])
    print(soucty_sloupcu(df, ["rano", "vecer"]))
