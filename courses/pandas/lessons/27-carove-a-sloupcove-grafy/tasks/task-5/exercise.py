# %% Knihovny
from matplotlib.figure import Figure
import pandas as pd


# %% Funkce pro úkol
def serazeny_vyvoj(tabulka):
    # TODO: Doplňte podle zadání, jiných správných postupů může být více.
    pass


# %% Vlastní ověření; při načtení kontrolou se nespustí.
if __name__ == "__main__":
    data = pd.DataFrame({"den": [3.0, 1.0, 2.0], "hodnota": [9.0, 8.0, 11.0]})
    fig = serazeny_vyvoj(data)
    if fig is not None:
        fig.savefig("graf.png", dpi=120)
        print("Uloženo: graf.png")
