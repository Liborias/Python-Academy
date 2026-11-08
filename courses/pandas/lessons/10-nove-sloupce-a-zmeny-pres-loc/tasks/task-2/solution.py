# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def pridej_prevod(tabulka, zdroj, cil, kurz):
    vysledek = tabulka.copy()
    vysledek[cil] = vysledek[zdroj] / kurz
    return vysledek


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"cena": [45.0, 60.0, 25.0], "kusy": [5, 3, 2]}, index=["caj", "kava", "voda"])
    print(pridej_prevod(df, "cena", "cena_eur", 25))
