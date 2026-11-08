# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def dopln_predchozi(serie):
    # TODO: vraťte výsledek podle zadání; původní vstupy neměňte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    s = pd.Series([None, "otevřeno", None, "zavřeno", None], index=["E", "A", "D", "B", "C"], name="stav", dtype="str")
    print(dopln_predchozi(s))
