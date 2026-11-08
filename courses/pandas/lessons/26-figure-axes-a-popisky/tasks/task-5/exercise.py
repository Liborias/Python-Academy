# %% Knihovny
from matplotlib.figure import Figure


# %% Funkce pro úkol
def dva_panely(titulek):
    # TODO: Doplňte podle zadání, jiných správných postupů může být více.
    pass


# %% Vlastní ověření; při načtení kontrolou se nespustí.
if __name__ == "__main__":
    fig = dva_panely("Dva pohledy na cvičná data")
    if fig is not None:
        fig.axes[0].plot([1, 2, 3], [8, 11, 9], marker="o")
        fig.axes[0].set_title("Vývoj")
        fig.axes[1].bar(["Čaj", "Káva"], [4, 7])
        fig.axes[1].set_title("Porovnání")
        fig.savefig("graf.png", dpi=120)
        print("Uloženo: graf.png")
