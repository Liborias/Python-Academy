# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def vyber_podle_masky(tabulka, maska):
    return tabulka.loc[maska].copy()


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"teplota": [10.0, 20.0, 30.0], "vlhkost": [80.0, 60.0, 45.0], "misto": ["Brno", "Praha", "Zlín"]}, index=["C", "A", "B"])
    maska = pd.Series([True, False, True], index=["B", "C", "A"], dtype=bool)
    print(vyber_podle_masky(df, maska))
