# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def odstran_duplicity(tabulka):
    # TODO: vraťte výsledek podle zadání; původní vstupy neměňte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"kod": ["A", "B", "A", "B"], "cena": [10.0, 20.0, 10.0, 25.0]}, index=["r3", "r1", "r2", "r0"])
    print(odstran_duplicity(df))
