# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def preved_cisla(serie):
    return pd.to_numeric(serie, errors="coerce").astype("float64")


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    s = pd.Series(["12.5", "chyba", None, "0", "-3"], index=["E", "B", "A", "D", "C"], name="cena", dtype="str")
    print(preved_cisla(s))
