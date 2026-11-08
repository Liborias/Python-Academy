# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def spoj_jednoznacne(leva, prava, klic):
    # TODO: vraťte výsledek podle zadání; vstupy neměňte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    a = pd.DataFrame({"kod": ["B", "A"], "leva": [2.0, 1.0]})
    b = pd.DataFrame({"kod": ["A", "C"], "prava": [10.0, 30.0]})
    print(spoj_jednoznacne(a, b, "kod"))
