# %% Knihovny
from matplotlib.figure import Figure


# %% Funkce pro úkol
def dve_rady(dny, prvni, druha):
    fig = Figure(layout="constrained")
    ax = fig.subplots()
    ax.plot(dny, prvni, marker="o", label="Ráno")
    ax.plot(dny, druha, marker="s", label="Večer")
    ax.set(title="Dvě měření", xlabel="Den", ylabel="Teplota (°C)")
    ax.legend()
    return fig


# %% Vlastní ověření; při načtení kontrolou se nespustí.
if __name__ == "__main__":
    fig = dve_rady([1, 2, 3], [8, 11, 9], [6, 8, 7])
    if fig is not None:
        fig.savefig("graf.png", dpi=120)
        print("Uloženo: graf.png")
