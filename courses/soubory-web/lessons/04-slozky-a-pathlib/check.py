from pathlib import Path
from dilna_check import check
c = check()
c.imports("pathlib", "Použijte modul pathlib: from pathlib import Path.")
c.utf8()
for _jmeno in ("najdi_txt", "obsah_slozky"):
    _f = c.function(_jmeno)
    c.add(f"Funkce {_jmeno} řadí výsledek", _f is not None and bool(c.calls_in(_f, "sorted") or c.calls_in(_f, "sort")),
          f"Ve funkci {_jmeno} seřaďte výsledek pomocí sorted(...), pořadí z disku není zaručené.")
ns = c.load()
if ns is not None:
    c.returns(ns, "najdi_txt", ("poznamky",), ["pondeli.txt", "utery.txt"])
    c.returns(ns, "najdi_txt", ("poznamky/archiv",), ["stary.txt"])
    c.returns(ns, "najdi_txt", ("neexistuje",), [])
    c.returns(ns, "obsah_slozky", ("poznamky",), ["archiv", "pondeli.txt", "seznam.md", "stare.txt", "utery.txt"])
    c.returns(ns, "obsah_slozky", ("poznamky/archiv",), ["stary.txt"])
    ok, v = c.call(ns, "zapis_poznamku", ("nova/pod", "p.txt", "Příliš žluťoučký\n"))
    c.add("zapis_poznamku vrací Path k souboru", ok and isinstance(v, Path) and v.name == "p.txt", f"Vrátila {v!r}.")
    soubor = Path("nova/pod/p.txt")
    c.add("zapis_poznamku vytvoří složky a soubor", soubor.is_file() and soubor.read_text(encoding="utf-8") == "Příliš žluťoučký\n",
          "Složka i soubor mají po zavolání existovat (mkdir s parents=True zakládá i nadřazené složky).")
    ok, v = c.call(ns, "zapis_poznamku", ("nova", "q.txt", "x"))
    c.add("zapis_poznamku funguje i s už existující složkou", ok and Path("nova/q.txt").is_file(), f"Volání skončilo: {v!r}.")
c.done()
