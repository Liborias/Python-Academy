# %% Knihovny
from matplotlib.figure import Figure


# %% Funkce pro úkol
def popis_osu(ax, titulek, x_popisek, y_popisek):
    # TODO: Doplňte podle zadání, jiných správných postupů může být více.
    pass


# %% Vlastní ověření; při načtení kontrolou se nespustí.
if __name__ == "__main__":
    fig = Figure(figsize=(6, 4), layout="constrained")
    ax = fig.subplots()
    ax.plot([1, 2, 3], [8, 11, 9], label="Ráno")
    popis_osu(ax, "Cvičná teplota", "Den", "Teplota (°C)")
    fig.savefig("graf.png", dpi=120)
    print("Uloženo: graf.png")
