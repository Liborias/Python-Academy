# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def vyber_od_limitu(tabulka, sloupec, minimum):
    maska = tabulka[sloupec] >= minimum
    return tabulka.loc[maska].copy()


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"teplota": [10.0, 20.0, 30.0], "vlhkost": [80.0, 60.0, 45.0], "misto": ["Brno", "Praha", "Zlín"]}, index=["C", "A", "B"])
    print(vyber_od_limitu(df, "teplota", 20))
