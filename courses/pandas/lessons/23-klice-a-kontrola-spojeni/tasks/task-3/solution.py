# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def pridej_stav_spojeni(leva, prava, klic):
    return leva.merge(prava, on=klic, how="outer", sort=True, indicator=True)


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    a = pd.DataFrame({"kod": ["B", "A"], "leva": [2.0, 1.0]})
    b = pd.DataFrame({"kod": ["A", "C"], "prava": [10.0, 30.0]})
    print(pridej_stav_spojeni(a, b, "kod"))
