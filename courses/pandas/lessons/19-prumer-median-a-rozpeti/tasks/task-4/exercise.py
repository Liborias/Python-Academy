# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def mediany_sloupcu(tabulka, sloupce):
    # TODO: vraťte výsledek podle zadání; původní vstupy neměňte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"rano": [10.0, None, None], "vecer": [14.0, 12.0, None], "misto": ["Brno", "Praha", "Zlín"]}, index=["B", "A", "C"])
    print(mediany_sloupcu(df, ["vecer", "rano"]))
