# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def spoj_stejna_jmena(leva, prava, klic):
    return leva.merge(prava, on=klic, how="left", sort=False, suffixes=("_objednavka", "_sklad"))


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    a = pd.DataFrame({"kod": ["B", "A"], "stav": ["nová", "zaplacená"]})
    b = pd.DataFrame({"kod": ["A"], "stav": ["skladem"]})
    print(spoj_stejna_jmena(a, b, "kod"))
