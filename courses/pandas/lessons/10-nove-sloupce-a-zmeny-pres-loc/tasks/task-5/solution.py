# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def prepocitej_podle_popisku(tabulka, sloupec, hodnoty):
    vysledek = tabulka.copy()
    vysledek[sloupec] = hodnoty
    return vysledek


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"cena": [45.0, 60.0, 25.0], "kusy": [5, 3, 2]}, index=["caj", "kava", "voda"])
    hodnoty = pd.Series([26.0, 47.0, 62.0], index=["voda", "caj", "kava"], dtype="float64")
    print(prepocitej_podle_popisku(df, "cena", hodnoty))
