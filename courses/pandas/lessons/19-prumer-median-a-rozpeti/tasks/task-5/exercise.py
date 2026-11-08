# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def porovnej_skupiny(tabulka, klic, hodnota):
    # TODO: vraťte výsledek podle zadání; původní vstupy neměňte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"skupina": ["A", "A", "A", "B"], "hodnota": [10.0, 10.0, 1000.0, 20.0]})
    print(porovnej_skupiny(df, "skupina", "hodnota"))
