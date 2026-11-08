# %% Knihovny
import pandas as pd
from pathlib import Path
from cisteni import zpracuj_mereni


# %% Funkce pro úkol
def zpracuj_soubory(cesty):
    casti = [zpracuj_mereni(cesta) for cesta in cesty]
    if not casti:
        return pd.DataFrame({"misto": pd.Series(dtype="str"), "hodnota": pd.Series(dtype="float64")})
    return pd.concat(casti, ignore_index=True)


# %% Vlastní ověření; při importu se neprovede.
if __name__ == "__main__":
    print(zpracuj_soubory(["mereni.csv", "dalsi.csv"]))
