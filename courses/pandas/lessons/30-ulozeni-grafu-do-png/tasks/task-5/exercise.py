# %% Knihovny
from matplotlib.figure import Figure
from pathlib import Path


# %% Funkce pro úkol
def uloz_varianty(fig, slozka):
    # TODO: Doplňte podle zadání, jiných správných postupů může být více.
    pass


# %% Vlastní ověření; při načtení kontrolou se nespustí.
if __name__ == "__main__":
    fig = Figure(figsize=(6, 4), layout="constrained")
    ax = fig.subplots()
    ax.plot([1, 2, 3], [8, 11, 9], marker="o")
    ax.set(title="Stejný obsah, různé DPI", xlabel="Den", ylabel="Teplota (°C)")
    print("Uloženo:", uloz_varianty(fig, "vystupy"))
