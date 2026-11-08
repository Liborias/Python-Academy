# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def statistiky_skupin(tabulka, klic, hodnota):
    return tabulka.groupby(klic, dropna=False, sort=True)[hodnota].agg(["count", "mean", "min", "max"])


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"produkt": ["caj", "kava", "caj", None], "trzba": [90.0, 180.0, 48.0, 25.0]}, index=["C", "A", "D", "B"])
    print(statistiky_skupin(df, "produkt", "trzba"))
