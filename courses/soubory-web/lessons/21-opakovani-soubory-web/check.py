import ast
import csv
import json
from pathlib import Path
from dilna_check import check
c = check()
c.utf8()
c.imports("csv", "Použijte modul csv.")
c.imports("json", "Použijte modul json.")
c.imports("bs4", "Použijte BeautifulSoup.")
fj = c.function("uloz_jako_json")
c.add("uloz_jako_json používá json.dump(s) a ensure_ascii=False",
      fj is not None and any(k.arg == "ensure_ascii" for name in ("dump", "dumps") for call in c.calls_in(fj, name) for k in call.keywords),
      "Použijte json.dump(data, soubor, ensure_ascii=False, indent=2).")
ns = c.load()
if ns is not None:
    c.returns(ns, "body_podle_tridy", ("body.csv",), {"7.A": 92, "7.B": 63})
    _ok, _v = c.call(ns, "body_podle_tridy", ("body.csv",))
    c.add("Součty bodů jsou celá čísla", _ok and isinstance(_v, dict) and all(type(x) is int for x in _v.values()), "Převeďte body na int().")
    c.returns(ns, "body_podle_tridy", ("neni.csv",), {})
    c.returns(ns, "nejlepsi_zak", ("body.csv",), "Petra")
    c.returns(ns, "nejlepsi_zak", ("neni.csv",), None)
    Path("prazdny.csv").write_text("jmeno,trida,body\n", encoding="utf-8")
    c.returns(ns, "nejlepsi_zak", ("prazdny.csv",), None)
    Path("devet.csv").write_text("jmeno,trida,body\nA,x,9\nB,x,100\n", encoding="utf-8")
    c.returns(ns, "nejlepsi_zak", ("devet.csv",), "B")
    ok, v = c.call(ns, "uloz_jako_json", ("body.csv", "zaci.json"))
    c.add("uloz_jako_json vrací počet žáků", ok and v == 4, f"Vrátila {v!r}, čekáme 4.")
    try:
        text = Path("zaci.json").read_text(encoding="utf-8")
        data = json.loads(text)
    except Exception as e:
        text, data = "", None
    c.add("JSON obsahuje žáky s body jako čísla", isinstance(data, list) and len(data) == 4 and data[0] == {"jmeno": "Eva", "trida": "7.A", "body": 42},
          f"Soubor obsahuje: {data!r}")
    c.add("Čeština je v JSON čitelná", "Tomáš" in text, "Použijte ensure_ascii=False.")
    c.returns(ns, "uloz_jako_json", ("neni.csv", "nic.json"), 0)
    c.add("Pro chybějící CSV nevzniká JSON", not Path("nic.json").exists(), "Soubor nic.json nesmí vzniknout.")
    c.returns(ns, "odkazy", ('<a href="/a">A</a><a name="x">bez</a><p><a href="https://b.cz">B</a></p>',), ["/a", "https://b.cz"])
    c.returns(ns, "odkazy", ("<p>nic</p>",), [])
c.done()
