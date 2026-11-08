# %% Knihovny a ověřené předchozí kroky
from pathlib import Path
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from predchozi import over_schema, vycisti_mereni, spoj_a_shrn, napis_zpravu, vytvor_vystupy
from test_dilna import spust_testy


# %% Aktuální krok projektu
def over_prehled(prehled, ocekavane):
    if prehled.keys() != ocekavane.keys():
        return False
    try:
        for jmeno in ocekavane:
            pd.testing.assert_frame_equal(prehled[jmeno], ocekavane[jmeno], check_exact=False, rtol=1e-12, atol=1e-12)
    except (AssertionError, TypeError, ValueError):
        return False
    return True


# %% Vlastní ověření nad přiloženými zdroji.
if __name__ == "__main__":
    raw = pd.read_csv("mereni.csv", sep=";", encoding="utf-8", dtype="str", keep_default_na=False)
    mista = pd.read_csv("mista.csv", sep=";", encoding="utf-8", dtype="str", keep_default_na=False)
    cisteni = vycisti_mereni(raw)
    prehled = spoj_a_shrn(cisteni["cista"], mista)
    print("Shodný přehled:", over_prehled(prehled, prehled))
    print("Veřejné testy prošly:", spust_testy(over_prehled))
