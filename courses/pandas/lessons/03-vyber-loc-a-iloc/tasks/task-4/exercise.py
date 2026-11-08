# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def prejmenuj_popisky(serie, zmeny):
    # TODO: doplňte výsledek podle zadání; None je zatím nedokončený návrat.
    return None


# %% Vlastní ověření: tento blok se při importu neprovede.
if __name__ == "__main__":
    s = pd.Series([10, 20], index=["A", "B"], name="hodnota", dtype="float64")
    print(prejmenuj_popisky(s, {"A": "Brno"}))
