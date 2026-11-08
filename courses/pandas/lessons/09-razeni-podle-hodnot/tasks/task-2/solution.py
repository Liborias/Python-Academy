# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def serad_podle_dvou(tabulka, prvni, druhy):
    return tabulka.sort_values(by=[prvni, druhy], ascending=[True, False], na_position="last")


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"produkt": ["Káva", "Čaj", "Voda", "Džus"], "cena": [60.0, 45.0, 25.0, 45.0], "kusy": [3, 5, 2, 8]}, index=["K", "C", "V", "D"])
    print(serad_podle_dvou(df, "cena", "kusy"))
