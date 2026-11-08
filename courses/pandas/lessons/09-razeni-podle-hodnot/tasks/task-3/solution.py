# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def nejlevnejsi(tabulka, pocet):
    return tabulka.sort_values(by="cena", kind="stable", na_position="last").head(pocet)


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"produkt": ["Káva", "Čaj", "Voda", "Džus"], "cena": [60.0, 45.0, 25.0, 45.0], "kusy": [3, 5, 2, 8]}, index=["K", "C", "V", "D"])
    print(nejlevnejsi(df, 2))
