# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def prehled_dvou_hodnot(tabulka, klic, prvni, druha):
    # TODO: vraťte výsledek podle zadání; původní vstupy neměňte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"produkt": ["caj", "kava", "caj"], "cena": [45.0, 60.0, 48.0], "kusy": [2.0, 3.0, 1.0]})
    print(prehled_dvou_hodnot(df, "produkt", "cena", "kusy"))
