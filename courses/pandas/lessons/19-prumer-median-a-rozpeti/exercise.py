# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def popis_hodnot(serie):
    # TODO: vraťte výsledek podle zadání; původní vstupy neměňte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    s = pd.Series([10.0, 10.0, 12.0, 1000.0, None], name="mereni", dtype="float64")
    print(popis_hodnot(s))
