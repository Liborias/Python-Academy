# %% Knihovny a ověřené předchozí kroky
from pathlib import Path
import pandas as pd
import numpy as np
from predchozi import over_schema, vycisti_mereni



# %% spoj_a_shrn
def spoj_a_shrn(cista, mista):
    # TODO: Doplňte navazující část projektu.
    return None


# %% Vlastní ověření nad přiloženými zdroji.
if __name__ == "__main__":
    raw = pd.read_csv("mereni.csv", sep=";", encoding="utf-8", dtype="str", keep_default_na=False)
    mista = pd.read_csv("mista.csv", sep=";", encoding="utf-8", dtype="str", keep_default_na=False)
    cisteni = vycisti_mereni(raw)
    print(spoj_a_shrn(cisteni["cista"], mista))
