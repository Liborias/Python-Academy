# %% Knihovny
from matplotlib.figure import Figure


# %% Funkce pro úkol
def velikost_bodu(x, y, velikosti):
    fig = Figure(layout="constrained")
    ax = fig.subplots()
    ax.scatter(x, y, s=velikosti)
    ax.set(title="Velikost značky jako údaj", xlabel="Čas (min)", ylabel="Výkon (body)")
    return fig


# %% Vlastní ověření; při načtení kontrolou se nespustí.
if __name__ == "__main__":
    fig = velikost_bodu([1, 2, 3], [3, 6, 5], [30, 100, 200])
    if fig is not None:
        fig.savefig("graf.png", dpi=120)
        print("Uloženo: graf.png")
