import os, sys
sys.path.insert(0, os.getcwd())
from dilna_web import spust
from dilna_check import check
import ast
import threading
import time
from pathlib import Path
import requests
ZAZNAM = []
_skutecne = time.sleep


def _spanek(s):                      # čekání studenta jen zapíšeme, čekání serveru necháme skutečné
    if threading.current_thread() is threading.main_thread():
        ZAZNAM.append(s)
    else:
        _skutecne(s)


time.sleep = _spanek
def T(n):
    return Path(f"web/clanky/{n}.html").read_bytes().decode("utf-8")


c = check()
c.imports("requests", "Použijte balíček requests.")
f1 = c.function("stahni_bezpecne")
c.add("stahni_bezpecne používá timeout", f1 is not None and any(k.arg == "timeout" and isinstance(k.value, ast.Name) and k.value.id == "timeout" for call in c.calls_in(f1, "get") for k in call.keywords),
      "Do requests.get přidejte timeout=timeout.")
c.add("stahni_bezpecne zachytává výjimky", f1 is not None and any(isinstance(n, __import__("ast").Try) for n in __import__("ast").walk(f1)),
      "Použijte try a except requests.RequestException.")
f2 = c.function("stahni_s_opakovanim")
ns = c.load()
if ns is not None:
    A = spust()
    c.returns(ns, "stahni_bezpecne", (A + "/clanky/1.html",), T(1))
    c.returns(ns, "stahni_bezpecne", (A + "/neexistuje",), None)
    c.returns(ns, "stahni_bezpecne", (A + "/_status/500",), None)
    c.returns(ns, "stahni_bezpecne", ("http://127.0.0.1:1/",), None)
    t = time.time()
    ok, v = c.call(ns, "stahni_bezpecne", (A + "/_pomalu/3",), {"timeout": 0.5})
    c.add("Pomalý server: timeout se dodrží", ok and v is None and time.time() - t < 2.5,
          "Při timeout=0.5 musí funkce skončit dřív než za 2,5 s a vrátit None.")
    c.returns(ns, "stahni_bezpecne", (A + "/_pomalu/0.5",), None, {"timeout": 0.1})
    c.returns(ns, "stahni_bezpecne", (A + "/_pomalu/0.2",), "Hotovo po čekání", {"timeout": 2})
    ZAZNAM.clear()
    c.returns(ns, "stahni_s_opakovanim", (A + "/_nestabilni/p", 3, 0.3), "Povedlo se")
    c.add("Mezi pokusy se čeká `pauza` sekund (2 neúspěšné pokusy = 2 pauzy)", ZAZNAM == [0.3, 0.3],
          f"Zaznamenané pauzy: {ZAZNAM!r}. Po neúspěšném pokusu zavolejte time.sleep(pauza).")
    c.returns(ns, "stahni_s_opakovanim", (A + "/_nestabilni/a", 3), "Povedlo se")
    c.returns(ns, "stahni_s_opakovanim", (A + "/_nestabilni/b", 2), None)
    c.returns(ns, "stahni_s_opakovanim", (A + "/clanky/2.html",), T(2))
    ok, v = c.call(ns, "stahni_s_opakovanim", (A + "/_nestabilni/c", 1))
    c.add("Při pokusy=1 se pošle jen jeden dotaz", ok and v is None and requests.get(A + "/_nestabilni/c").status_code == 500,
          "Funkce nesmí poslat víc dotazů, než je počet pokusů.")
    c.returns(ns, "stahni_s_opakovanim", ("http://127.0.0.1:1/", 2, 0.01), None)
c.done()
