# %% Knihovny a ověřené předchozí kroky
from pathlib import Path
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
import json
from bunky import BUNKY, UVOD
import shutil
from predchozi import over_schema, vycisti_mereni, spoj_a_shrn, napis_zpravu, vytvor_vystupy, over_prehled, vytvor_notebook



# %% spust_dilnu
def spust_dilnu(mereni_cesta, mista_cesta, slozka):
    # TODO: Doplňte navazující část projektu.
    return None


# %% Vlastní ověření nad přiloženými zdroji.
if __name__ == "__main__":
    print(spust_dilnu("mereni.csv", "mista.csv", Path("hotovy_projekt")))
