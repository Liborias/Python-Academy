# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def vycisti_text(serie):
    # TODO: vraťte výsledek podle zadání; původní vstupy neměňte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    s = pd.Series(["  PRAHA ", " Brno", "ŽĎÁR  ", "", None], name="misto", dtype="str")
    print(vycisti_text(s))
