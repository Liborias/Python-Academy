# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def vyber_nekterou_podminku(tabulka, sloupec_a, limit_a, sloupec_b, limit_b):
    # TODO: vraťte výsledek podle zadání; původní vstupy zachovejte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"teplota": [10.0, 20.0, 30.0], "vlhkost": [80.0, 60.0, 45.0], "misto": ["Brno", "Praha", "Zlín"]}, index=["C", "A", "B"])
    print(vyber_nekterou_podminku(df, "teplota", 25, "vlhkost", 80))
