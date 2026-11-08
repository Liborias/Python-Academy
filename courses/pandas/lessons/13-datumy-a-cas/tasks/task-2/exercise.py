# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def preved_casy(serie):
    # TODO: vraťte výsledek podle zadání; původní vstupy neměňte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    s = pd.Series(["2026-02-01 08:30", "2026-02-01 25:00", None], name="cas", dtype="str")
    print(preved_casy(s))
