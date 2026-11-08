# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def serie_ze_slovniku(data, nazev):
    return pd.Series(data, name=nazev, dtype="float64")


# %% Vlastní ověření: tento blok se při importu neprovede.
if __name__ == "__main__":
    print(serie_ze_slovniku({"caj": 45, "kava": 60}, "cena"))
