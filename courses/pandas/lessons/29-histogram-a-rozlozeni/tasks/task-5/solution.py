# %% Knihovny
from matplotlib.figure import Figure


# %% Funkce pro úkol
def dve_rozlozeni(prvni, druha, hranice):
    fig = Figure(figsize=(8, 3), layout="constrained")
    osy = fig.subplots(1, 2, sharey=True)
    for ax, data, jmeno in zip(osy, [prvni, druha], ["Ráno", "Večer"]):
        ax.hist(data, bins=hranice)
        ax.set(title=jmeno, xlabel="Doba (min)", ylabel="Četnost")
    fig.suptitle("Dvě rozložení")
    return fig


# %% Vlastní ověření; při načtení kontrolou se nespustí.
if __name__ == "__main__":
    fig = dve_rozlozeni([0, 1, 2], [1, 1, 3, 4], [0, 2, 4])
    if fig is not None:
        fig.savefig("graf.png", dpi=120)
        print("Uloženo: graf.png")
