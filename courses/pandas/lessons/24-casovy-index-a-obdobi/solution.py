# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def nastav_casovy_index(tabulka, sloupec):
    return tabulka.set_index(sloupec).sort_index(kind="stable")


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"cas": pd.to_datetime(["2026-02-02 08:00", "2026-02-01 08:00", "2026-02-01 12:00"]), "teplota": [19.0, 18.0, 20.0]})
    print(nastav_casovy_index(df, "cas"))
