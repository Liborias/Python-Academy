# %% Knihovny
from matplotlib.figure import Figure


# %% Funkce pro úkol
def priprav_graf(titulek, x_popisek, y_popisek):
    fig = Figure(figsize=(6, 4), layout="constrained")
    ax = fig.subplots()
    ax.set_title(titulek)
    ax.set_xlabel(x_popisek)
    ax.set_ylabel(y_popisek)
    return fig


# %% Vlastní ověření; při načtení kontrolou se nespustí.
if __name__ == "__main__":
    fig = priprav_graf("Cvičné ranní teploty", "Den", "Teplota (°C)")
    if fig is not None:
        fig.axes[0].plot([1, 2, 3], [8, 11, 9], marker="o", label="Ráno")
        fig.axes[0].legend()
        fig.savefig("graf.png", dpi=120)
        print("Uloženo: graf.png")
