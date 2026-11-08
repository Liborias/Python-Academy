# %% Knihovny
from matplotlib.figure import Figure
from pathlib import Path


# %% Funkce pro úkol
def uloz_tesne(fig, cesta):
    cesta = Path(cesta)
    fig.savefig(cesta, format="png", dpi=100, bbox_inches="tight", pad_inches=0.1)
    return cesta


# %% Vlastní ověření; při načtení kontrolou se nespustí.
if __name__ == "__main__":
    fig = Figure(figsize=(6, 4))
    ax = fig.subplots()
    ax.plot([1, 2, 3], [8, 11, 9], marker="o")
    ax.set(title="Celý popisek zůstane vidět", xlabel="Pořadí dne měření", ylabel="Cvičná teplota (°C)")
    print("Uloženo:", uloz_tesne(fig, "graf.png"))
