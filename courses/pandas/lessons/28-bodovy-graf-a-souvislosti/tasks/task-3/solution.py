# %% Knihovny
from matplotlib.figure import Figure
import pandas as pd


# %% Funkce pro úkol
def porovnej_skupiny(prvni, druha):
    fig = Figure(layout="constrained")
    ax = fig.subplots()
    ax.scatter(prvni["x"], prvni["y"], marker="o", label="Skupina A")
    ax.scatter(druha["x"], druha["y"], marker="^", label="Skupina B")
    ax.set(title="Dvě skupiny", xlabel="x", ylabel="y")
    ax.legend()
    return fig


# %% Vlastní ověření; při načtení kontrolou se nespustí.
if __name__ == "__main__":
    a = pd.DataFrame({"x": [1.0, 2.0, 3.0], "y": [3.0, 4.0, 5.0]})
    b = pd.DataFrame({"x": [1.0, 2.0, 3.0], "y": [5.0, 3.0, 2.0]})
    fig = porovnej_skupiny(a, b)
    if fig is not None:
        fig.savefig("graf.png", dpi=120)
        print("Uloženo: graf.png")
