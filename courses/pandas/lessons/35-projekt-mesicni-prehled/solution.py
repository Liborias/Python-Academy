# %% Knihovny a hotové souhrny z projektu kavárny.
import pandas as pd
from pathlib import Path
from matplotlib.figure import Figure
from kavarna import prehled_kavarny


# %% vyber_mesic
def vyber_mesic(tabulka, mesic):
    zacatek = pd.Timestamp(mesic + "-01")
    konec = zacatek + pd.offsets.MonthBegin(1)
    return tabulka.loc[(tabulka["den"] >= zacatek) & (tabulka["den"] < konec)].copy()


# %% prehled_mesice
def prehled_mesice(tabulka, mesic):
    data = vyber_mesic(tabulka, mesic)
    data["den"] = data["den"].dt.strftime("%Y-%m-%d").astype("str")
    return prehled_kavarny(data)


# %% uloz_report
def uloz_report(prehled, slozka):
    slozka = Path(slozka)
    slozka.mkdir(parents=True, exist_ok=True)
    csv = slozka / "podle_dnu.csv"
    excel = slozka / "prehled.xlsx"
    graf = slozka / "trzby.png"
    prehled["podle_dnu"].to_csv(csv, sep=";", decimal=",", encoding="utf-8", index=False)
    with pd.ExcelWriter(excel, engine="openpyxl") as zapis:
        prehled["podle_dnu"].to_excel(zapis, sheet_name="Dny", index=False)
        prehled["podle_produktu"].to_excel(zapis, sheet_name="Produkty", index=False)
        pd.DataFrame([prehled["celkem"]]).to_excel(zapis, sheet_name="Celkem", index=False)
    fig = Figure(figsize=(6, 4), layout="constrained")
    ax = fig.subplots()
    produkty = prehled["podle_produktu"]
    ax.bar(produkty["produkt"], produkty["trzba"])
    ax.set(title="Měsíční tržby podle produktů", xlabel="Produkt", ylabel="Tržba (Kč)")
    ax.set_ylim(bottom=0)
    fig.savefig(graf, dpi=120)
    return {"csv": csv, "excel": excel, "graf": graf}


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
