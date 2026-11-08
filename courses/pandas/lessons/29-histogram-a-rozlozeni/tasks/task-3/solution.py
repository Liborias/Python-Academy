# %% Knihovny
from matplotlib.figure import Figure
import pandas as pd


# %% Funkce pro úkol
def vycisti_hodnoty(serie):
    return serie.dropna()


# %% Vlastní ověření; při načtení kontrolou se nespustí.
if __name__ == "__main__":
    s = pd.Series([None, 0.0, 1.0, 2.0, 4.0], name="doba", dtype="float64")
    values = vycisti_hodnoty(s)
    print(values)
    if values is not None:
        fig = Figure(layout="constrained")
        ax = fig.subplots()
        ax.hist(values, bins=[0, 2, 4])
        ax.set(title="Jen známé doby", xlabel="Doba (min)", ylabel="Četnost")
        fig.savefig("graf.png", dpi=120)
        print("Uloženo: graf.png")
