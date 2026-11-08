# %% Knihovny: tabulky a porovnání desetinných součtů.
import math
import pandas as pd


# %% Výpočet přehledů zachovává původní tabulku.
def prehled_kavarny(tabulka):
    data = tabulka.copy()
    data["trzba"] = data["kusy"] * data["cena"]
    podle_dnu = data.groupby("den", as_index=False, sort=True).agg(
        radky=("kusy", "size"), kusy=("kusy", "sum"), trzba=("trzba", "sum")
    )
    podle_produktu = data.groupby("produkt", as_index=False, sort=True).agg(
        radky=("kusy", "size"), kusy=("kusy", "sum"), trzba=("trzba", "sum")
    )
    celkem = {"radky": len(data), "kusy": int(data["kusy"].sum()), "trzba": float(data["trzba"].sum())}
    return {"podle_dnu": podle_dnu, "podle_produktu": podle_produktu, "celkem": celkem}


# %% Kontrolní součty ověřují oba přehledy proti celkovému výsledku.
def over_soucty(prehled):
    for nazev in ("podle_dnu", "podle_produktu"):
        tabulka = prehled[nazev]
        for pole in ("radky", "kusy"):
            if tabulka[pole].sum() != prehled["celkem"][pole]:
                return False
        if not math.isclose(float(tabulka["trzba"].sum()), prehled["celkem"]["trzba"], rel_tol=1e-12, abs_tol=1e-9):
            return False
    return True
