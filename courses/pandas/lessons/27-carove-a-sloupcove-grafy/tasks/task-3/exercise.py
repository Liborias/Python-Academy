# %% Knihovny
from matplotlib.figure import Figure


# %% Funkce pro úkol
def dve_rady(dny, prvni, druha):
    # TODO: Doplňte podle zadání, jiných správných postupů může být více.
    pass


# %% Vlastní ověření; při načtení kontrolou se nespustí.
if __name__ == "__main__":
    fig = dve_rady([1, 2, 3], [8, 11, 9], [6, 8, 7])
    if fig is not None:
        fig.savefig("graf.png", dpi=120)
        print("Uloženo: graf.png")
