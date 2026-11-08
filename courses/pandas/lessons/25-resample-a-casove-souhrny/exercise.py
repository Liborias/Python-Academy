# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def denni_soucty(serie):
    # TODO: vraťte výsledek podle zadání; vstupy neměňte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    idx = pd.DatetimeIndex(["2026-02-01 08:00", "2026-02-01 12:00", "2026-02-03 00:00", "2026-02-04 08:00"], name="cas").as_unit("us")
    s = pd.Series([1.0, 2.0, 0.0, None], index=idx, name="mereni", dtype="float64")
    print(denni_soucty(s))
