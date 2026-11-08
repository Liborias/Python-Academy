# %% Knihovny
from matplotlib.figure import Figure


# %% Funkce pro úkol
def stejne_meritko(x, y, minimum, maximum):
    # TODO: Doplňte podle zadání, jiných správných postupů může být více.
    pass


# %% Vlastní ověření; při načtení kontrolou se nespustí.
if __name__ == "__main__":
    fig = stejne_meritko([0, 2, 4], [1, 3, 1], -1, 5)
    if fig is not None:
        fig.savefig("graf.png", dpi=120)
        print("Uloženo: graf.png")
