# %% Knihovny
from matplotlib.figure import Figure


# %% Funkce pro úkol
def histogram(hodnoty, hranice):
    fig = Figure(layout="constrained")
    ax = fig.subplots()
    ax.hist(hodnoty, bins=hranice)
    ax.set(title="Rozložení dob", xlabel="Doba (min)", ylabel="Četnost")
    return fig


# %% Vlastní ověření; při načtení kontrolou se nespustí.
if __name__ == "__main__":
    fig = histogram([0, 1, 2, 2, 3, 4, 6], [0, 2, 4, 6])
    if fig is not None:
        fig.savefig("graf.png", dpi=120)
        print("Uloženo: graf.png")
