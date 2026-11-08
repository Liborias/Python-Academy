# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def spoj_radky(prvni, druha):
    return pd.concat([prvni, druha], ignore_index=True)


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    a = pd.DataFrame({"misto": ["Brno", "Praha"], "teplota": [18.0, 21.0]})
    b = pd.DataFrame({"misto": ["Brno"], "teplota": [19.0]})
    print(spoj_radky(a, b))
