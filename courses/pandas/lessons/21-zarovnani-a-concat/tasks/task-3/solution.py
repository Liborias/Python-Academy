# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def spoj_sloupce(prvni, druha):
    return pd.concat([prvni, druha], axis=1, join="outer").sort_index()


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    a = pd.DataFrame({"rano": [18.0, 21.0]}, index=["Brno", "Praha"])
    b = pd.DataFrame({"vecer": [17.0, 20.0]}, index=["Zlín", "Brno"])
    print(spoj_sloupce(a, b))
