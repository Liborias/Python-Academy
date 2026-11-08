# %% Knihovny
from matplotlib.figure import Figure
import pandas as pd


# %% Funkce pro úkol
def porovnej_skupiny(prvni, druha):
    # TODO: Doplňte podle zadání, jiných správných postupů může být více.
    pass


# %% Vlastní ověření; při načtení kontrolou se nespustí.
if __name__ == "__main__":
    a = pd.DataFrame({"x": [1.0, 2.0, 3.0], "y": [3.0, 4.0, 5.0]})
    b = pd.DataFrame({"x": [1.0, 2.0, 3.0], "y": [5.0, 3.0, 2.0]})
    fig = porovnej_skupiny(a, b)
    if fig is not None:
        fig.savefig("graf.png", dpi=120)
        print("Uloženo: graf.png")
