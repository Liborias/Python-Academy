# %% Knihovny a ověřené předchozí kroky
from pathlib import Path
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from predchozi import over_schema, vycisti_mereni, spoj_a_shrn



# %% napis_zpravu
def napis_zpravu(cisteni, prehled):
    # TODO: Doplňte navazující část projektu.
    return None


# %% vytvor_vystupy
def vytvor_vystupy(cisteni, prehled, slozka):
    # TODO: Doplňte navazující část projektu.
    return None


# %% Vlastní ověření nad přiloženými zdroji.
if __name__ == "__main__":
    raw = pd.read_csv("mereni.csv", sep=";", encoding="utf-8", dtype="str", keep_default_na=False)
    mista = pd.read_csv("mista.csv", sep=";", encoding="utf-8", dtype="str", keep_default_na=False)
    cisteni = vycisti_mereni(raw)
    prehled = spoj_a_shrn(cisteni["cista"], mista)
    print(napis_zpravu(cisteni, prehled))
    print("Uloženo:", vytvor_vystupy(cisteni, prehled, "vystupy"))
