# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def rok_z_data(serie):
    return serie.dt.year.astype("Int64")


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    s = pd.Series([pd.Timestamp("2026-02-01"), pd.NaT, pd.Timestamp("2024-02-29")], name="datum", dtype="datetime64[us]")
    print(rok_z_data(s))
