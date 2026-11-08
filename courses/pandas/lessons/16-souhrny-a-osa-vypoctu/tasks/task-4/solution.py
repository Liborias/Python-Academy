# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def rozsah_tabulky(tabulka):
    return {"radky": len(tabulka), "bunky": tabulka.size}


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"rano": [10.0, None, None], "vecer": [14.0, 12.0, None], "misto": ["Brno", "Praha", "Zlín"]}, index=["B", "A", "C"])
    print(rozsah_tabulky(df))
