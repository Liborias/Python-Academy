# %% Knihovny
from matplotlib.figure import Figure


# %% Funkce pro úkol
def porovnani(nazvy, pocty):
    fig = Figure(layout="constrained")
    ax = fig.subplots()
    ax.bar(nazvy, pocty)
    ax.set(title="Porovnání kategorií", xlabel="Kategorie", ylabel="Počet")
    ax.set_ylim(bottom=0)
    return fig


# %% Vlastní ověření; při načtení kontrolou se nespustí.
if __name__ == "__main__":
    fig = porovnani(["Čaj", "Káva", "Voda"], [4, 7, 0])
    if fig is not None:
        fig.savefig("graf.png", dpi=120)
        print("Uloženo: graf.png")
