# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def spoj_jine_nazvy(objednavky, produkty):
    return objednavky.merge(produkty, left_on="kod", right_on="id", how="left", sort=False)


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    a = pd.DataFrame({"kod": ["B", "A"], "kusy": [1, 2]})
    b = pd.DataFrame({"id": ["A"], "nazev": ["Čaj"]})
    print(spoj_jine_nazvy(a, b))
