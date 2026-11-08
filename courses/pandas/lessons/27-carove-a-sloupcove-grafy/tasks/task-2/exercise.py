# %% Knihovny
from matplotlib.figure import Figure


# %% Funkce pro úkol
def porovnani(nazvy, pocty):
    # TODO: Doplňte podle zadání, jiných správných postupů může být více.
    pass


# %% Vlastní ověření; při načtení kontrolou se nespustí.
if __name__ == "__main__":
    fig = porovnani(["Čaj", "Káva", "Voda"], [4, 7, 0])
    if fig is not None:
        fig.savefig("graf.png", dpi=120)
        print("Uloženo: graf.png")
