# %% Knihovny a hotové souhrny z projektu kavárny.
import pandas as pd
from pathlib import Path
from matplotlib.figure import Figure
from kavarna import prehled_kavarny


# %% vyber_mesic
def vyber_mesic(tabulka, mesic):
    # TODO: Doplňte jednu navazující část projektu.
    return None


# %% prehled_mesice
def prehled_mesice(tabulka, mesic):
    # TODO: Doplňte jednu navazující část projektu.
    return None


# %% uloz_report
def uloz_report(prehled, slozka):
    # TODO: Doplňte jednu navazující část projektu.
    return None


# %% Spuštění měsíčního přehledu nad vlastními cvičnými daty.
if __name__ == "__main__":
    data = pd.read_csv("prodeje.csv", sep=";", decimal=",", encoding="utf-8", keep_default_na=False, dtype={"den":"str", "produkt":"str", "kusy":"int64", "cena":"float64"})
    data["den"] = pd.to_datetime(data["den"], format="%Y-%m-%d").astype("datetime64[us]")
    prehled = prehled_mesice(data, "2026-02")
    if prehled is None:
        print("Doplňte tři funkce projektu podle zadání.")
    else:
        print("Podle dnů:")
        print(prehled["podle_dnu"])
        print("Podle produktů:")
        print(prehled["podle_produktu"])
        print("Celkem:", prehled["celkem"])
        print("Uloženo:", uloz_report(prehled, "vystupy"))
