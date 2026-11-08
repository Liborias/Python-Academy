# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def jeden_sloupec_jako_tabulka(tabulka, sloupec):
    # TODO: vraťte výsledek podle zadání; původní vstupy zachovejte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"misto": ["Brno", "Praha", "Zlín"], "teplota": [18.5, 21.0, 16.5]}, index=["B", "A", "C"])
    print(jeden_sloupec_jako_tabulka(df, "teplota"))
