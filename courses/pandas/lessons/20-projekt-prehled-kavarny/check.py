import math
from copy import deepcopy
import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()

# Nezávislý očekávaný výsledek: součty v Python cyklu, bez groupby.
def ocekavany_report(data):
    dny, produkty = {}, {}
    celkem = {"radky": 0, "kusy": 0, "trzba": 0.0}
    for row in data.to_dict("records"):
        trzba = row["kusy"] * row["cena"]
        for skupiny, klic in ((dny, row["den"]), (produkty, row["produkt"])):
            if klic not in skupiny:
                skupiny[klic] = {"radky": 0, "kusy": 0, "trzba": 0.0}
            skupiny[klic]["radky"] += 1
            skupiny[klic]["kusy"] += row["kusy"]
            skupiny[klic]["trzba"] += trzba
        celkem["radky"] += 1
        celkem["kusy"] += row["kusy"]
        celkem["trzba"] += trzba
    def tabulka(skupiny, klic):
        zaznamy = [{klic: k, **skupiny[k]} for k in sorted(skupiny)]
        return pd.DataFrame(zaznamy, columns=[klic,"radky","kusy","trzba"]).astype(
            {klic:"str","radky":"int64","kusy":"int64","trzba":"float64"})
    return {"podle_dnu": tabulka(dny,"den"), "podle_produktu": tabulka(produkty,"produkt"), "celkem": celkem}

df = pd.DataFrame({"den":["2026-02-02","2026-02-01","2026-02-02","2026-02-01"],
                   "produkt":["B","A","B","A"], "kusy":[2,3,0,1], "cena":[1.25,2.0,8.0,2.75]}, index=["D","A","C","B"])
empty = df.head(0)
extra = pd.DataFrame({"den":["2025-12-31","2026-01-01","2026-01-01"],
                      "produkt":["X","Y","X"], "kusy":[3,1,2], "cena":[0.1,0.2,0.3]})
repeated = pd.concat([df, df.iloc[[0]]])
cases = [((data,), ocekavany_report(data)) for data in (df, empty, extra, df.iloc[::-1], repeated)]
check_cases(c, ns, "prehled_kavarny", cases)

report = ocekavany_report(df)
controls = [((report,),True), ((ocekavany_report(empty),),True), ((ocekavany_report(extra),),True)]
for name in ("podle_dnu", "podle_produktu"):
    for field in ("radky", "kusy", "trzba"):
        broken = deepcopy(report)
        broken[name].loc[0, field] += 1
        controls.append(((broken,),False))
for field in ("radky", "kusy", "trzba"):
    broken = deepcopy(report)
    broken["celkem"][field] += 1
    controls.append(((broken,),False))
near = deepcopy(report)
near["podle_dnu"].loc[0,"trzba"] += 1e-11
controls.append(((near,),True))
for name in ("podle_dnu", "podle_produktu"):
    broken = deepcopy(report)
    broken[name].loc[0,"trzba"] += 0.01
    controls.append(((broken,),False))
check_cases(c, ns, "over_soucty", controls)
c.done()
