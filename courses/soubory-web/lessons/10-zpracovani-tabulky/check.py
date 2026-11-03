import csv
from dilna_check import check
c = check()
c.utf8()
ns = c.load()
if ns is not None:
    R = [{"mesic": "leden", "zbozi": "jablka", "kusy": 120, "cena": 25}, {"mesic": "leden", "zbozi": "hrušky", "kusy": 80, "cena": 30},
         {"mesic": "únor", "zbozi": "jablka", "kusy": 100, "cena": 26}, {"mesic": "únor", "zbozi": "hrušky", "kusy": 95, "cena": 30},
         {"mesic": "březen", "zbozi": "jablka", "kusy": 150, "cena": 24}, {"mesic": "březen", "zbozi": "švestky", "kusy": 60, "cena": 45}]
    c.returns(ns, "nacti_prodej", ("prodej.csv",), R)
    c.returns(ns, "trzby_podle_zbozi", (R,), {"jablka": 9200, "hrušky": 5250, "švestky": 2700})
    c.returns(ns, "trzby_podle_zbozi", ([],), {})
    c.returns(ns, "nejlepsi_mesic", (R,), "březen")
    c.returns(ns, "nejlepsi_mesic", (R[:4],), "únor")
    c.returns(ns, "nejlepsi_mesic", ([{"mesic": "x", "zbozi": "a", "kusy": 1, "cena": 1}],), "x")
    c.returns(ns, "nejvic_kusu", (R, 3), [R[4], R[0], R[2]])
    c.returns(ns, "nejvic_kusu", (R, 1), [R[4]])
    c.returns(ns, "nejvic_kusu", (R, 10), [R[4], R[0], R[2], R[3], R[1], R[5]])
    stejne = [{"mesic": "a", "zbozi": "x", "kusy": 5, "cena": 1}, {"mesic": "b", "zbozi": "y", "kusy": 5, "cena": 1},
              {"mesic": "c", "zbozi": "z", "kusy": 9, "cena": 1}]
    c.returns(ns, "nejvic_kusu", (stejne, 3), [stejne[2], stejne[0], stejne[1]])
    kopie = [dict(r) for r in R]
    c.call(ns, "nejvic_kusu", (kopie, 3))
    c.add("nejvic_kusu nemění původní seznam", kopie == R, "Použijte sorted(...), které vrací nový seznam, a původní nechte beze změny.")
c.done()
