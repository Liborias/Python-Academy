# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def odchylky_od_prumeru(serie):
    return serie - serie.mean()


# %% Vlastní ověření: tento blok se při importu neprovede.
if __name__ == "__main__":
    s = pd.Series([10, 15, 20], index=["A", "B", "C"], name="mereni", dtype="float64")
    print(odchylky_od_prumeru(s))
