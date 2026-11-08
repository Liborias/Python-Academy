# %% Knihovny
from matplotlib.figure import Figure


# %% Funkce pro úkol
def vyvoj(dny, hodnoty):
    fig = Figure(layout="constrained")
    ax = fig.subplots()
    ax.plot(dny, hodnoty, marker="o")
    ax.set(title="Vývoj měření", xlabel="Den", ylabel="Hodnota")
    return fig


# %% Vlastní ověření; při načtení kontrolou se nespustí.
if __name__ == "__main__":
    fig = vyvoj([1, 3, 7], [8.0, 11.0, 9.0])
    if fig is not None:
        fig.savefig("graf.png", dpi=120)
        print("Uloženo: graf.png")
