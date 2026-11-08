# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def obnov_index(tabulka):
    # TODO: vraťte výsledek podle zadání; původní vstupy zachovejte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"produkt": ["Káva", "Čaj", "Voda", "Džus"], "cena": [60.0, 45.0, 25.0, 45.0], "kusy": [3, 5, 2, 8]}, index=["K", "C", "V", "D"])
    print(obnov_index(df.sort_values("cena", kind="stable")))
