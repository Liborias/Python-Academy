# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def jedinecne_hodnoty(serie):
    # TODO: vraťte výsledek podle zadání; původní vstupy neměňte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    s = pd.Series(["Brno", "Praha", "Brno", ""], name="misto", dtype="str")
    print(jedinecne_hodnoty(s))
