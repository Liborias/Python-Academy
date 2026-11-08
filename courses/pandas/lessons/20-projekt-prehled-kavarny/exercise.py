# %% Knihovny: tabulky a porovnání desetinných součtů.
import math
import pandas as pd


# %% Výpočet přehledů zachovává původní tabulku.
def prehled_kavarny(tabulka):
    # TODO: vytvořte dva přehledy a celkový souhrn.
    return None


# %% Kontrolní součty ověřují oba přehledy proti celkovému výsledku.
def over_soucty(prehled):
    # TODO: ověřte počty i desetinné tržby obou přehledů.
    return False


# %% Přiložená data jsou syntetická; relativní cesta používá pracovní složku.
if __name__ == "__main__":
    data = pd.read_csv("prodeje.csv", sep=";", decimal=",", encoding="utf-8",
                       dtype={"den": "str", "produkt": "str", "kusy": "int64", "cena": "float64"})
    prehled = prehled_kavarny(data)
    if prehled is None:
        print("Doplňte prehled_kavarny a over_soucty podle zadání.")
    else:
        print("Přehled podle dnů:")
        print(prehled["podle_dnu"])
        print("Přehled podle produktů:")
        print(prehled["podle_produktu"])
        print("Celkem:", prehled["celkem"])
        print("Kontrolní součty souhlasí:", over_soucty(prehled))
