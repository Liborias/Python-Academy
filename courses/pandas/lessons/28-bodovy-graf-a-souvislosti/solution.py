# %% Knihovny
from matplotlib.figure import Figure


# %% Funkce pro úkol
def bodovy_graf(x, y):
    fig = Figure(layout="constrained")
    ax = fig.subplots()
    ax.scatter(x, y)
    ax.set(title="Cvičná měření", xlabel="Doba učení (h)", ylabel="Body v kvízu")
    return fig


# %% Vlastní ověření; při načtení kontrolou se nespustí.
if __name__ == "__main__":
    fig = bodovy_graf([1, 2, 3, 4], [5, 9, 7, 12])
    if fig is not None:
        fig.savefig("graf.png", dpi=120)
        print("Uloženo: graf.png")
