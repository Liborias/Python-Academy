# %% Knihovny a ověřené předchozí kroky
from pathlib import Path
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
import json
from bunky import BUNKY, UVOD
from predchozi import over_schema, vycisti_mereni, spoj_a_shrn, napis_zpravu, vytvor_vystupy, over_prehled
from bez_notebooku import spustit



# %% vytvor_notebook
def vytvor_notebook():
    # TODO: Doplňte navazující část projektu.
    return None


# %% Vlastní ověření nad přiloženými zdroji.
if __name__ == "__main__":
    notebook = vytvor_notebook()
    if notebook is None:
        print("Doplňte strukturu notebooku podle zadání.")
    else:
        Path("analyticka_dilna.ipynb").write_text(json.dumps(notebook, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        print("Uloženo: analyticka_dilna.ipynb")
        spustit()
