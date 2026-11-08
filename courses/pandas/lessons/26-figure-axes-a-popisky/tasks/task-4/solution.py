# %% Knihovny
from matplotlib.figure import Figure


# %% Funkce pro úkol
def nastav_rozsah(ax, minimum, maximum):
    ax.set_ylim(minimum, maximum)
    return ax


# %% Vlastní ověření; při načtení kontrolou se nespustí.
if __name__ == "__main__":
    fig = Figure(figsize=(6, 4), layout="constrained")
    ax = fig.subplots()
    ax.plot([1, 2, 3], [8, 11, 9], label="Ráno")
    nastav_rozsah(ax, -5, 20)
    fig.savefig("graf.png", dpi=120)
    print("Uloženo: graf.png")
