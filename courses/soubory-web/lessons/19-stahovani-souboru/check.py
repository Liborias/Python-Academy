import os, sys
sys.path.insert(0, os.getcwd())
from dilna_web import spust
from dilna_check import check
import ast
from pathlib import Path
c = check()
c.imports("requests", "Použijte balíček requests.")
f1 = c.function("stahni_soubor")
c.add("stahni_soubor zapisuje binárně (režim wb nebo write_bytes)",
      f1 is not None and (bool(c.calls_in(f1, "write_bytes")) or any(isinstance(n, ast.Constant) and n.value == "wb" for n in ast.walk(f1))),
      "Obrázek je binární: otevřete soubor s \"wb\" nebo použijte write_bytes.")
c.add("stahni_soubor používá content (ne text)", f1 is not None and any(isinstance(n, ast.Attribute) and n.attr == "content" for n in ast.walk(f1)),
      "Bajty jsou v odpoved.content.")
f2 = c.function("stahni_obrazky")
c.add("stahni_obrazky používá urljoin", f2 is not None and bool(c.calls_in(f2, "urljoin")), "Adresy obrázků složte funkcí urljoin.")
ns = c.load()
if ns is not None:
    A = spust()
    puvodni = {n: Path("web/img/" + n + ".png").read_bytes() for n in ("a", "b", "c")}
    ok, v = c.call(ns, "stahni_soubor", (A + "/img/a.png", "kopie.png"))
    c.add("stahni_soubor vrací počet bajtů", ok and v == len(puvodni["a"]), f"Vrátila {v!r}, čekáme {len(puvodni['a'])}.")
    c.add("Stažený soubor je shodný s originálem", Path("kopie.png").is_file() and Path("kopie.png").read_bytes() == puvodni["a"],
          "Obsah souboru se liší, zkontrolujte režim zápisu.")
    ok, v = c.call(ns, "stahni_soubor", (A + "/img/neni.png", "chyba.png"))
    c.add("Při 404 vrací None a soubor nevytvoří", ok and v is None and not Path("chyba.png").exists(),
          f"Vrátila {v!r}; soubor chyba.png nesmí vzniknout.")
    ok, v = c.call(ns, "stahni_soubor", ("http://127.0.0.1:1/x.png", "chyba2.png"))
    c.add("Nepřipojení vrací None", ok and v is None and not Path("chyba2.png").exists(), "Zachyťte requests.RequestException.")
    ok, v = c.call(ns, "stahni_obrazky", (A + "/galerie.html", "galerie"))
    c.add("stahni_obrazky vrací jména souborů v pořadí", ok and v == ["a.png", "b.png", "c.png"], f"Vrátila {v!r}.")
    for n in ("a", "b", "c"):
        c.add(f"galerie/{n}.png je shodný s originálem", Path(f"galerie/{n}.png").is_file() and Path(f"galerie/{n}.png").read_bytes() == puvodni[n],
              f"Soubor galerie/{n}.png chybí nebo je poškozený.")
    ok, v = c.call(ns, "stahni_obrazky", (A + "/galerie.html", "galerie"))
    c.add("Druhé spuštění do existující složky nespadne", ok and v == ["a.png", "b.png", "c.png"], "Použijte mkdir(exist_ok=True).")
    ok, v = c.call(ns, "stahni_obrazky", (A + "/index.html", "prazdna"))
    c.add("Stránka bez obrázků vrací []", ok and v == [], f"Vrátila {v!r}.")
c.done()
