# %% Knihovny
from matplotlib.figure import Figure
from pathlib import Path


# %% Funkce pro úkol
def priprav_tisk(fig, sirka, vyska):
    fig.set_size_inches(sirka, vyska)
    return fig


# %% Vlastní ověření; při načtení kontrolou se nespustí.
if __name__ == "__main__":
    fig = Figure(layout="constrained")
    ax = fig.subplots()
    ax.plot([1, 2, 3], [8, 11, 9], marker="o")
    ax.set(title="Rozměr 8 × 4 palce", xlabel="Den", ylabel="Teplota (°C)")
    priprav_tisk(fig, 8, 4)
    fig.savefig("graf.png", dpi=100)
    print("Uloženo: graf.png, 800 × 400 pixelů")
