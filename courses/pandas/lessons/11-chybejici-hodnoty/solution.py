# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def chybejici_pocty(tabulka):
    return tabulka.isna().sum().astype("int64")


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"misto": ["Brno", None, ""], "teplota": [0.0, None, 18.5]}, index=["C", "A", "B"])
    print(chybejici_pocty(df))
