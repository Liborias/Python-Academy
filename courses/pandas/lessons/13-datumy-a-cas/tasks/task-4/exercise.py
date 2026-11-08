# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def vyber_obdobi(tabulka, sloupec, od, do):
    # TODO: vraťte výsledek podle zadání; původní vstupy neměňte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"datum": pd.to_datetime(["2026-02-01", "2026-02-02", None]), "kusy": [3, 5, 2]})
    print(vyber_obdobi(df, "datum", "2026-02-01", "2026-02-02"))
