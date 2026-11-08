# %% Knihovny
from matplotlib.figure import Figure


# %% Funkce pro úkol
def stejne_meritko(x, y, minimum, maximum):
    fig = Figure(layout="constrained")
    ax = fig.subplots()
    ax.scatter(x, y)
    ax.set_xlim(minimum, maximum)
    ax.set_ylim(minimum, maximum)
    ax.set_aspect("equal", adjustable="box")
    ax.set(title="Stejné měřítko", xlabel="Východ (m)", ylabel="Sever (m)")
    return fig


# %% Vlastní ověření; při načtení kontrolou se nespustí.
if __name__ == "__main__":
    fig = stejne_meritko([0, 2, 4], [1, 3, 1], -1, 5)
    if fig is not None:
        fig.savefig("graf.png", dpi=120)
        print("Uloženo: graf.png")
