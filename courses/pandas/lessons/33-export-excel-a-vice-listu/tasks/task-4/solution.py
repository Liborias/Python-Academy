# %% Knihovny
import pandas as pd
from pathlib import Path


# %% Funkce pro úkol
def zachovej_kody(tabulka, cesta):
    cesta = Path(cesta)
    tabulka.to_excel(cesta, sheet_name="Data", engine="openpyxl", index=False)
    return cesta


# %% Vlastní ověření; při importu se neprovede.
if __name__ == "__main__":
    data = pd.DataFrame({"kod": ["001", "NA", "010"], "pocet": [2, 0, 3]})
    print("Uloženo:", zachovej_kody(data, "kody.xlsx"))
