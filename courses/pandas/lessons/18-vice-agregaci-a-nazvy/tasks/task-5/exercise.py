# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def serad_prehled(tabulka):
    # TODO: vraťte výsledek podle zadání; původní vstupy neměňte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"skupina": ["B", "A", "C"], "radky": [2, 3, 1], "prumer": [10.0, 10.0, None]}, index=[5, 2, 9])
    print(serad_prehled(df))
