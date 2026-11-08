# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def sjednot_mezery(serie):
    # TODO: vraťte výsledek podle zadání; původní vstupy neměňte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    s = pd.Series(["  Nové   Město ", "Žďár\tnad\nSázavou", None], name="misto", dtype="str")
    print(sjednot_mezery(s))
