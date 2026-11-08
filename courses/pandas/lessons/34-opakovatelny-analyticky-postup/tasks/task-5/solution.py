# %% Knihovny
import pandas as pd
from pathlib import Path
from cisteni import zpracuj_mereni, souhrn_mist


# %% Funkce pro úkol
def analyzuj_mereni(vstup, vystup):
    data = zpracuj_mereni(vstup)
    souhrn = souhrn_mist(data)
    souhrn.to_csv(vystup, sep=";", decimal=",", encoding="utf-8", index=False)
    return souhrn


# %% Vlastní ověření; při importu se neprovede.
if __name__ == "__main__":
    print(analyzuj_mereni("mereni.csv", "souhrn.csv"))
