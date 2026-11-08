# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def pricti_bonus(serie, bonus):
    return serie + bonus


# %% Vlastní ověření: tento blok se při importu neprovede.
if __name__ == "__main__":
    s = pd.Series([10, 20], index=["A", "B"], name="body", dtype="float64")
    print(pricti_bonus(s, 3))
