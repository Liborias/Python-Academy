# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def chybi_na_radku(tabulka, sloupce):
    return tabulka[sloupce].isna().any(axis=1)


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"misto": ["Brno", None, ""], "teplota": [0.0, None, 18.5]}, index=["C", "A", "B"])
    print(chybi_na_radku(df, ["misto", "teplota"]))
