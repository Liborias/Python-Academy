# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def preved_sloupce(tabulka, typy):
    # TODO: vraťte výsledek podle zadání; původní vstupy neměňte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"kusy": ["2", None, "0"], "cena": ["12.5", "0", "3.0"], "kod": ["001", "007", "010"]})
    print(preved_sloupce(df, {"kusy": "Int64", "cena": "float64"}).dtypes)
