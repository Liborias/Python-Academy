# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def hodnota_bunky(tabulka, radek, sloupec):
    return tabulka.loc[radek, sloupec]


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"misto": ["Brno", "Praha", "Zlín"], "teplota": [18.5, 21.0, 16.5]}, index=["B", "A", "C"])
    print(hodnota_bunky(df, "C", "teplota"))
