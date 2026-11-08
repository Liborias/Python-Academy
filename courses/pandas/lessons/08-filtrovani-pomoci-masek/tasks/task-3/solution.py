# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def vyber_nekterou_podminku(tabulka, sloupec_a, limit_a, sloupec_b, limit_b):
    maska = (tabulka[sloupec_a] >= limit_a) | (tabulka[sloupec_b] >= limit_b)
    return tabulka.loc[maska].copy()


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"teplota": [10.0, 20.0, 30.0], "vlhkost": [80.0, 60.0, 45.0], "misto": ["Brno", "Praha", "Zlín"]}, index=["C", "A", "B"])
    print(vyber_nekterou_podminku(df, "teplota", 25, "vlhkost", 80))
