# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def nahrad_bunku(tabulka, radek, sloupec, nova_hodnota):
    vysledek = tabulka.copy()
    vysledek.loc[radek, sloupec] = nova_hodnota
    return vysledek


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"cena": [45.0, 60.0, 25.0], "kusy": [5, 3, 2]}, index=["caj", "kava", "voda"])
    print(nahrad_bunku(df, "caj", "cena", 48.5))
