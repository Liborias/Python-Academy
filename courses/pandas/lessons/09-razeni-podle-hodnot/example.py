# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def serad_tabulku(tabulka, sloupec, vzestupne):
    return tabulka.sort_values(by=sloupec, ascending=vzestupne, kind="stable", na_position="last")


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"produkt": ["Káva", "Čaj", "Voda", "Džus"], "cena": [60.0, 45.0, 25.0, 45.0], "kusy": [3, 5, 2, 8]}, index=["K", "C", "V", "D"])
    print(serad_tabulku(df, "cena", True))
