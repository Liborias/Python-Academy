# %% Knihovny
from matplotlib.figure import Figure


# %% Funkce pro úkol
def vodorovne(nazvy, hodnoty):
    fig = Figure(layout="constrained")
    ax = fig.subplots()
    ax.barh(nazvy, hodnoty)
    ax.invert_yaxis()
    ax.set_xlim(left=0)
    ax.set(title="Kategorie shora", xlabel="Počet", ylabel="Kategorie")
    return fig


# %% Vlastní ověření; při načtení kontrolou se nespustí.
if __name__ == "__main__":
    fig = vodorovne(["Čaj s medem", "Káva bez kofeinu", "Voda"], [4, 7, 0])
    if fig is not None:
        fig.savefig("graf.png", dpi=120)
        print("Uloženo: graf.png")
