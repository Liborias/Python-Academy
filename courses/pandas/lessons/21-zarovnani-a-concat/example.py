# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def zarovnej_mereni(serie, popisky):
    return serie.reindex(popisky)


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    s = pd.Series([18.0, 21.0], index=["Brno", "Praha"], name="teplota", dtype="float64")
    print(zarovnej_mereni(s, ["Praha", "Zlín", "Brno"]))
