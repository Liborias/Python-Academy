# %% Knihovny a ověřené předchozí kroky
from pathlib import Path
import pandas as pd



# %% over_schema
def over_schema(tabulka, povinne):
    # TODO: Doplňte navazující část projektu.
    return None


# %% Vlastní ověření nad přiloženými zdroji.
if __name__ == "__main__":
    raw = pd.read_csv("mereni.csv", sep=";", encoding="utf-8", dtype="str", keep_default_na=False)
    mista = pd.read_csv("mista.csv", sep=";", encoding="utf-8", dtype="str", keep_default_na=False)
    print("Schéma měření:", over_schema(raw, ["den", "kod", "teplota"]))
    print("Schéma katalogu:", over_schema(mista, ["kod", "nazev", "oblast"]))
    print("Počet záznamů:", len(raw))
