# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def vyber_obdelnik(tabulka, radky, sloupce):
    return tabulka.loc[radky, sloupce].copy()


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"misto": ["Brno", "Praha", "Zlín"], "teplota": [18.5, 21.0, 16.5]}, index=["B", "A", "C"])
    print(vyber_obdelnik(df, ["C", "B"], ["teplota", "misto"]))
