# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def seskup_do_tabulky(tabulka, klic, hodnota):
    # TODO: vraťte výsledek podle zadání; původní vstupy neměňte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"produkt": ["caj", "kava", "caj", None], "trzba": [90.0, 180.0, 48.0, 25.0]}, index=["C", "A", "D", "B"])
    print(seskup_do_tabulky(df, "produkt", "trzba"))
