# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def spolecne_sloupce(prvni, druha):
    # TODO: vraťte výsledek podle zadání; vstupy neměňte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    a = pd.DataFrame({"rano": [18.0], "vecer": [20.0]})
    b = pd.DataFrame({"vecer": [19.0], "vlhkost": [65.0]})
    print(spolecne_sloupce(a, b))
