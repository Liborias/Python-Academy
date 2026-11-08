# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def pridej_trzbu(tabulka):
    vysledek = tabulka.copy()
    vysledek["trzba"] = vysledek["cena"] * vysledek["kusy"]
    return vysledek


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"cena": [45.0, 60.0, 25.0], "kusy": [5, 3, 2]}, index=["caj", "kava", "voda"])
    print(pridej_trzbu(df))
    print("Původní sloupce:", df.columns.tolist())
