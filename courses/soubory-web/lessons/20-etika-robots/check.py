import os, sys
sys.path.insert(0, os.getcwd())
from dilna_web import spust
from dilna_check import check
import json
import time
from pathlib import Path
import requests
ZAZNAM = []
time.sleep = lambda s: ZAZNAM.append(s)      # místo čekání jen zapíšeme, jak dlouho se mělo čekat
def T(n):
    return Path(f"web/clanky/{n}.html").read_bytes().decode("utf-8")


c = check()
c.imports("requests", "Použijte balíček requests.")
c.add("Používá RobotFileParser", c.uses_call("RobotFileParser"), "Pravidla čtěte pomocí urllib.robotparser.RobotFileParser.")
f2 = c.function("stahni_jako")
c.add("stahni_jako posílá headers", f2 is not None and any(k.arg == "headers" for call in c.calls_in(f2, "get") for k in call.keywords),
      "Do requests.get přidejte headers={\"User-Agent\": agent}.")
ns = c.load()
if ns is not None:
    A = spust()
    c.returns(ns, "smi_stahovat", (A, "/index.html"), True)
    c.returns(ns, "smi_stahovat", (A, "/soukrome/tajne.html"), False)
    c.returns(ns, "smi_stahovat", (A, "/clanky/1.html"), True)
    c.returns(ns, "smi_stahovat", (A, "/index.html", "zlybot"), False)
    c.returns(ns, "smi_stahovat", (A + "/bez", "/index.html"), True)    # na /bez/robots.txt nic není
    ok, v = c.call(ns, "stahni_jako", (A + "/_hlavicky", "Skola-Python/1.0"))
    try:
        agent = json.loads(v)["user-agent"]
    except Exception:
        agent = None
    c.add("stahni_jako pošle vlastní User-Agent", ok and agent == "Skola-Python/1.0", f"Server dostal: {agent!r}.")
    c.returns(ns, "stahni_jako", (A + "/clanky/3.html", "x"), T(3))
    ZAZNAM.clear()
    urls = [A + "/clanky/1.html", A + "/clanky/2.html", A + "/clanky/3.html"]
    c.returns(ns, "stahni_slusne", (urls, 0.5), [T(1), T(2), T(3)])
    c.add("stahni_slusne čeká mezi dotazy (2 až 3 pauzy)", len(ZAZNAM) in (2, 3) and all(s == 0.5 for s in ZAZNAM),
          f"Zaznamenané pauzy: {ZAZNAM!r}.")
    ZAZNAM.clear()
    c.returns(ns, "stahni_slusne", ([A + "/clanky/1.html"], 2), [T(1)])
    c.add("Jediná stránka nepotřebuje čekat dlouho", sum(ZAZNAM) <= 2, "Pauza se nemá zdržovat zbytečně.")
c.done()
