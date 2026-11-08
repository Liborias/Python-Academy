# %% Knihovny
from matplotlib.figure import Figure


# %% Funkce pro úkol
def hustota(hodnoty, hranice):
    fig = Figure(layout="constrained")
    ax = fig.subplots()
    ax.hist(hodnoty, bins=hranice, density=True)
    ax.set(title="Hustota dob", xlabel="Doba (min)", ylabel="Hustota (1/min)")
    return fig


# %% Vlastní ověření; při načtení kontrolou se nespustí.
if __name__ == "__main__":
    fig = hustota([0, 1, 2, 4], [0, 1, 4])
    if fig is not None:
        fig.savefig("graf.png", dpi=120)
        print("Uloženo: graf.png")
