# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def mesicni_soucty(serie):
    return serie.resample("MS", closed="left", label="left").sum(min_count=1)


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    idx = pd.DatetimeIndex(["2026-01-31 23:59", "2026-02-01 00:00", "2026-04-01 00:00"], name="cas").as_unit("us")
    s = pd.Series([2.0, 3.0, None], index=idx, name="mereni", dtype="float64")
    print(mesicni_soucty(s))
