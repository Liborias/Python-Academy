# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def preved_na_eura(ceny_kc, kurz):
    # TODO: doplňte výsledek podle zadání; None je zatím nedokončený návrat.
    return None


# %% Vlastní ověření: tento blok se při importu neprovede.
if __name__ == "__main__":
    ceny = pd.Series([50, 75, 125], index=["caj", "kava", "dezert"], name="cena", dtype="float64")
    print(preved_na_eura(ceny, 25))
