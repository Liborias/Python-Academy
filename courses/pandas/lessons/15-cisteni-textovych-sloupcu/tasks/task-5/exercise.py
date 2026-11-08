# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def vycisti_sloupec(tabulka, sloupec):
    # TODO: vraťte výsledek podle zadání; původní vstupy neměňte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"misto": [" PRAHA ", "Brno", None], "poznamka": [" Zachovat ", "Text", "X"], "kusy": [1, 2, 3]})
    print(vycisti_sloupec(df, "misto"))
