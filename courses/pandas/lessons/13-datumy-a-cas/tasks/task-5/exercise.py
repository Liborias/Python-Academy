# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def chybne_datumy(serie):
    # TODO: vraťte výsledek podle zadání; původní vstupy neměňte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    s = pd.Series(["01.02.2026", "31.02.2026", None, "29.02.2024"], name="datum", dtype="str")
    print(chybne_datumy(s))
