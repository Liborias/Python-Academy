# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def odstran_jednotku(serie, pripona):
    # TODO: vraťte výsledek podle zadání; původní vstupy neměňte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    s = pd.Series([" 12 kg ", "kg12", "12 kg navíc", None], name="hmotnost", dtype="str")
    print(odstran_jednotku(s, "kg"))
