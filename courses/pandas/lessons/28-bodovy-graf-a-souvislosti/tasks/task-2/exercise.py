# %% Knihovny
from matplotlib.figure import Figure
import pandas as pd


# %% Funkce pro úkol
def vyber_dvojice(tabulka):
    # TODO: Doplňte podle zadání, jiných správných postupů může být více.
    pass


# %% Vlastní ověření; při načtení kontrolou se nespustí.
if __name__ == "__main__":
    data = pd.DataFrame({"x": [1.0, None, 3.0], "y": [5.0, 7.0, 8.0]})
    pary = vyber_dvojice(data)
    print(pary)
    if pary is not None:
        fig = Figure(layout="constrained")
        ax = fig.subplots()
        ax.scatter(pary["x"], pary["y"])
        ax.set(title="Úplné dvojice", xlabel="x", ylabel="y")
        fig.savefig("graf.png", dpi=120)
        print("Uloženo: graf.png")
