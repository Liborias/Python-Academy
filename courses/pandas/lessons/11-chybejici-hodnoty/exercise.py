# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def chybejici_pocty(tabulka):
    # TODO: vraťte výsledek podle zadání; původní vstupy neměňte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"misto": ["Brno", None, ""], "teplota": [0.0, None, 18.5]}, index=["C", "A", "B"])
    print(chybejici_pocty(df))
