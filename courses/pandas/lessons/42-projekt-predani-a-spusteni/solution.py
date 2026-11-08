# %% Knihovny a ověřené předchozí kroky
from pathlib import Path
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
import json
from bunky import BUNKY, UVOD
import shutil
from predchozi import over_schema, vycisti_mereni, spoj_a_shrn, napis_zpravu, vytvor_vystupy, over_prehled, vytvor_notebook


# %% Aktuální krok projektu
def spust_dilnu(mereni_cesta, mista_cesta, slozka):
    raw = pd.read_csv(mereni_cesta, sep=";", encoding="utf-8", dtype="str", keep_default_na=False)
    mista = pd.read_csv(mista_cesta, sep=";", encoding="utf-8", dtype="str", keep_default_na=False)
    if not over_schema(raw, ["den", "kod", "teplota"]) or not over_schema(mista, ["kod", "nazev", "oblast"]):
        raise ValueError("Nesprávné zdrojové sloupce.")
    cisteni = vycisti_mereni(raw)
    prehled = spoj_a_shrn(cisteni["cista"], mista)
    slozka = Path(slozka)
    shutil.copytree("projekt", slozka, dirs_exist_ok=True)
    shutil.copy2(mereni_cesta, slozka / "mereni.csv")
    shutil.copy2(mista_cesta, slozka / "mista.csv")
    (slozka / "analyticka_dilna.ipynb").write_text(json.dumps(vytvor_notebook(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    vystupy = vytvor_vystupy(cisteni, prehled, slozka / "vysledky")
    return {"projekt": slozka, "vystupy": vystupy, "prijato": len(cisteni["cista"]), "odmitnuto": len(cisteni["odmitnuta"]), "nesparovano": len(prehled["nesparovana"])}


# %% Vlastní ověření nad přiloženými zdroji.
if __name__ == "__main__":
    print(spust_dilnu("mereni.csv", "mista.csv", Path("hotovy_projekt")))
