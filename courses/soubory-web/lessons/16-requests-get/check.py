import os, sys
sys.path.insert(0, os.getcwd())
from dilna_web import spust
from dilna_check import check
c = check()
c.imports("requests", "Použijte balíček requests: import requests.")
for _jmeno in ("stahni_text", "stavovy_kod", "nacti_json", "nadpis"):
    _f = c.function(_jmeno)
    c.add(f"Funkce {_jmeno} stahuje pomocí requests.get",
          _f is not None and bool(c.calls_in(_f, "get")), f"Ve funkci {_jmeno} zavolejte requests.get(url).")
ns = c.load()
if ns is not None:
    A = spust()
    S = __import__("pathlib").Path("web/index.html").read_bytes().decode("utf-8")
    c.returns(ns, "stahni_text", (A + "/index.html",), S)
    c.returns(ns, "stavovy_kod", (A + "/index.html",), 200)
    c.returns(ns, "stavovy_kod", (A + "/neexistuje.html",), 404)
    c.returns(ns, "stavovy_kod", (A + "/_status/500",), 500)
    c.returns(ns, "nacti_json", (A + "/data.json",), {"mesto": "Brno", "teplota": 21, "vitr": [3, 5, 4]})
    c.returns(ns, "nadpis", (A + "/index.html",), "Vítejte v Dílně")
    c.returns(ns, "nadpis", (A + "/knihy.html",), "Knihkupectví U Lampy")
    c.returns(ns, "nadpis", (A + "/_status/404",), None)
c.done()
