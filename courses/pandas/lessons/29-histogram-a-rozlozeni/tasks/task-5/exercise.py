# %% Knihovny
from matplotlib.figure import Figure


# %% Funkce pro úkol
def dve_rozlozeni(prvni, druha, hranice):
    # TODO: Doplňte podle zadání, jiných správných postupů může být více.
    pass


# %% Vlastní ověření; při načtení kontrolou se nespustí.
if __name__ == "__main__":
    fig = dve_rozlozeni([0, 1, 2], [1, 1, 3, 4], [0, 2, 4])
    if fig is not None:
        fig.savefig("graf.png", dpi=120)
        print("Uloženo: graf.png")
