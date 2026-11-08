# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def preved_casy(serie):
    return pd.to_datetime(serie, format="%Y-%m-%d %H:%M", errors="coerce").astype("datetime64[us]")


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    s = pd.Series(["2026-02-01 08:30", "2026-02-01 25:00", None], name="cas", dtype="str")
    print(preved_casy(s))
