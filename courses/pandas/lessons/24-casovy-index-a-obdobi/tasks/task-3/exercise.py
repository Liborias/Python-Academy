# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def vyber_den(tabulka, den):
    # TODO: vraťte výsledek podle zadání; vstupy neměňte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    idx = pd.DatetimeIndex(["2026-02-01 08:00", "2026-02-01 12:00", "2026-02-02 00:00"], name="cas").as_unit("us")
    df = pd.DataFrame({"teplota": [18.0, 20.0, 19.0]}, index=idx)
    print(vyber_den(df, "2026-02-01"))
