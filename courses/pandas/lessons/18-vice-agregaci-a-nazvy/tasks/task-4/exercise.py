# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def prehled_dvou_klicu(tabulka, prvni_klic, druhy_klic, hodnota):
    # TODO: vraťte výsledek podle zadání; původní vstupy neměňte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    df = pd.DataFrame({"den": ["2026-11-01", "2026-11-01", "2026-11-02"], "produkt": ["caj", "kava", "caj"], "trzba": [90.0, 180.0, 48.0]})
    print(prehled_dvou_klicu(df, "den", "produkt", "trzba"))
