# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def pravidelna_mrizka(serie, zacatek, konec):
    # TODO: vraťte výsledek podle zadání; vstupy neměňte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    s = pd.Series([18.0, 19.0], index=pd.DatetimeIndex(["2026-02-01", "2026-02-03"], name="den").as_unit("us"), name="teplota", dtype="float64")
    print(pravidelna_mrizka(s, "2026-02-01", "2026-02-03"))
