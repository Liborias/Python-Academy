# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def preved_data(serie):
    return pd.to_datetime(serie, format="%d.%m.%Y", errors="coerce").astype("datetime64[us]")


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    s = pd.Series(["01.02.2026", "31.02.2026", None, "29.02.2024"], name="datum", dtype="str")
    print(preved_data(s))
