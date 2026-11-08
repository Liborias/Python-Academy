# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def pocty_hodnot(serie):
    # TODO: vraťte výsledek podle zadání; původní vstupy neměňte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    s = pd.Series(["Brno", "Praha", "Brno", None, None], name="misto", dtype="str")
    print(pocty_hodnot(s))
