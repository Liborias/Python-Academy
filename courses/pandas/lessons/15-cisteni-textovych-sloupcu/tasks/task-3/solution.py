# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def odstran_jednotku(serie, pripona):
    return serie.str.strip().str.removesuffix(pripona).str.strip()


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    s = pd.Series([" 12 kg ", "kg12", "12 kg navíc", None], name="hmotnost", dtype="str")
    print(odstran_jednotku(s, "kg"))
