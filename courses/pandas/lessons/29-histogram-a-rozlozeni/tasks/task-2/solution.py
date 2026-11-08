# %% Knihovny
from matplotlib.figure import Figure
import numpy as np


# %% Funkce pro úkol
def cetnosti(hodnoty, hranice):
    pocty, _ = np.histogram(hodnoty, bins=hranice)
    return pocty.tolist()


# %% Vlastní ověření; při načtení kontrolou se nespustí.
if __name__ == "__main__":
    hodnoty = [0, 1, 2, 2, 3, 4, 6]
    hranice = [0, 2, 4, 6]
    print("Četnosti:", cetnosti(hodnoty, hranice))
    fig = Figure(layout="constrained")
    ax = fig.subplots()
    ax.hist(hodnoty, bins=hranice)
    ax.set(title="Kontrola četností", xlabel="Doba (min)", ylabel="Četnost")
    fig.savefig("graf.png", dpi=120)
    print("Uloženo: graf.png")
