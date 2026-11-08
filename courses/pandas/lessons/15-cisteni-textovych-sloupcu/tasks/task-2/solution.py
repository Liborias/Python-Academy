# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def sjednot_mezery(serie):
    return serie.str.strip().str.replace(r"\s+", " ", regex=True)


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    s = pd.Series(["  Nové   Město ", "Žďár\tnad\nSázavou", None], name="misto", dtype="str")
    print(sjednot_mezery(s))
