# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def prehled_dvou_hodnot(tabulka, klic, prvni, druha):
    return tabulka.groupby(klic, as_index=False, dropna=False, sort=True).agg(prumer=(prvni, "mean"), maximum=(druha, "max"))


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"produkt": ["caj", "kava", "caj"], "cena": [45.0, 60.0, 48.0], "kusy": [2.0, 3.0, 1.0]})
    print(prehled_dvou_hodnot(df, "produkt", "cena", "kusy"))
