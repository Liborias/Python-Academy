def spustit():
    import sys
    from pathlib import Path
    import pandas as pd
    from predchozi import over_schema, vycisti_mereni, spoj_a_shrn, napis_zpravu, vytvor_vystupy, over_prehled
    print("Použitý Python:", sys.executable)
    raw = pd.read_csv("mereni.csv", sep=";", encoding="utf-8", dtype="str", keep_default_na=False)
    mista = pd.read_csv("mista.csv", sep=";", encoding="utf-8", dtype="str", keep_default_na=False)
    assert over_schema(raw, ["den", "kod", "teplota"])
    assert over_schema(mista, ["kod", "nazev", "oblast"])
    print("Vstupní záznamy:", len(raw))
    cisteni = vycisti_mereni(raw)
    prehled = spoj_a_shrn(cisteni["cista"], mista)
    print("Odmítnuté:")
    print(cisteni["odmitnuta"])
    print("Nespárované:")
    print(prehled["nesparovana"])
    print(prehled["podle_mist"])
    vystupy = vytvor_vystupy(cisteni, prehled, "vystupy")
    print(napis_zpravu(cisteni, prehled))
    print("Výstupy:", vystupy)
    from test_dilna import spust_testy
    assert spust_testy(over_prehled)
    print("Veřejné testy prošly.")
