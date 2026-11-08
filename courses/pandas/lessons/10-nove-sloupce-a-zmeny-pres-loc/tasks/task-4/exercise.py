# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def uprav_vybrane(tabulka, sloupec, minimum, bonus):
    # TODO: vraťte výsledek podle zadání; původní vstupy zachovejte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"cena": [45.0, 60.0, 25.0], "kusy": [5, 3, 2]}, index=["caj", "kava", "voda"])
    print(uprav_vybrane(df, "cena", 45, -5))
