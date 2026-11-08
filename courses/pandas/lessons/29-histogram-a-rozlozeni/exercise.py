# %% Knihovny
from matplotlib.figure import Figure


# %% Funkce pro úkol
def histogram(hodnoty, hranice):
    # TODO: Doplňte podle zadání, jiných správných postupů může být více.
    pass


# %% Vlastní ověření; při načtení kontrolou se nespustí.
if __name__ == "__main__":
    fig = histogram([0, 1, 2, 2, 3, 4, 6], [0, 2, 4, 6])
    if fig is not None:
        fig.savefig("graf.png", dpi=120)
        print("Uloženo: graf.png")
