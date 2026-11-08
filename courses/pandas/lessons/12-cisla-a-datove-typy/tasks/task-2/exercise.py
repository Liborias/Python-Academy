# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def preved_desetinnou_carku(serie):
    # TODO: vraťte výsledek podle zadání; původní vstupy neměňte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    s = pd.Series(["12,5", "-0,25", "3.0", None, "chyba"], name="cena", dtype="str")
    print(preved_desetinnou_carku(s))
