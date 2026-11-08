# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def vyber_pozice(serie, pozice):
    # TODO: doplňte výsledek podle zadání; None je zatím nedokončený návrat.
    return None


# %% Vlastní ověření: tento blok se při importu neprovede.
if __name__ == "__main__":
    s = pd.Series([8, 6, 9], index=[10, 20, 30], name="hodnota", dtype="float64")
    print(vyber_pozice(s, [2, 0]))
