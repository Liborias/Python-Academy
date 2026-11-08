# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def pojmenovany_prehled(tabulka, klic, hodnota):
    return tabulka.groupby(klic, as_index=False, dropna=False, sort=True).agg(radky=(hodnota, "size"), dostupne=(hodnota, "count"), prumer=(hodnota, "mean"))


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"produkt": ["caj", "kava", "caj", None], "trzba": [90.0, 180.0, 48.0, 25.0]}, index=["C", "A", "D", "B"])
    print(pojmenovany_prehled(df, "produkt", "trzba"))
