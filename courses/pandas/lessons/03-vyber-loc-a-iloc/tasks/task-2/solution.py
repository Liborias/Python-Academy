# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def vyber_usek(serie, zacatek, konec):
    return serie.iloc[zacatek:konec].copy()


# %% Vlastní ověření: tento blok se při importu neprovede.
if __name__ == "__main__":
    s = pd.Series([8, 6, 9, 4], index=["A", "B", "C", "D"], dtype="float64")
    print(vyber_usek(s, 1, 3))
