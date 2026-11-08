"""Test chytrého editoru (psaní kláves v Chromiu)."""
import shutil, sys, threading
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.app import create_server

shots = Path(sys.argv[sys.argv.index("--shots") + 1]) if "--shots" in sys.argv else None
srv = create_server(ROOT, "127.0.0.1", 0, courses_dir=ROOT / "tests" / "fixtures")
threading.Thread(target=srv.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{srv.server_address[1]}/"
errors, fails = [], []

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=shutil.which('chromium') or None, args=['--no-sandbox'])
    pg = b.new_page(viewport={"width": 1000, "height": 900})
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.goto(f"{base}?t={srv.token}#/kurz/demo/01-pozdrav")
    pg.wait_for_selector(".editor .ed-ta")
    ta = pg.locator(".editor .ed-ta")

    def fresh(text=""):
        ta.click(); pg.keyboard.press("Control+A"); pg.keyboard.press("Delete")
        if text: pg.keyboard.type(text)

    def val(): return ta.input_value()
    def hidden():
        pg.wait_for_timeout(120); return pg.locator(".ac").is_hidden()
    def expect(name, got, want):
        if got != want: fails.append(f"{name}: čekáno {want!r}, je {got!r}")

    fresh("def f(a):"); pg.keyboard.press("Enter"); pg.keyboard.type("x = a"); pg.keyboard.press("Enter")
    expect("odsazení po dvojtečce", val(), "def f(a):\n    x = a\n    ")
    pg.keyboard.type("return x"); pg.keyboard.press("Enter")
    expect("zpět po return", val().split("\n")[-1], "")
    fresh("print("); expect("auto závorka", val(), "print()")
    pg.keyboard.type("1)"); expect("přeskočení závorky", val(), "print(1)")
    fresh('x = "ah'); expect("auto uvozovka", val(), 'x = "ah"')
    pg.keyboard.type('"'); expect("přeskočení uvozovky", val(), 'x = "ah"')
    fresh("don"); pg.keyboard.type("'t"); expect("apostrof za slovem", val(), "don't")
    fresh('f"a'); expect("f-řetězec", val(), 'f"a"')
    fresh("("); pg.keyboard.press("Backspace"); expect("Backspace maže pár", val(), "")
    fresh("x = [");
    pg.keyboard.press("Enter"); expect("Enter mezi závorkami", val(), "x = [\n    \n]")
    fresh("if a:"); pg.keyboard.press("Enter"); pg.keyboard.type("pass"); pg.keyboard.press("Enter")
    pg.keyboard.type("else:"); expect("dedent else", val(), "if a:\n    pass\nelse:")
    fresh("if a:"); pg.keyboard.press("Enter"); pg.keyboard.press("Backspace"); expect("Backspace po 4 mezerách", val(), "if a:\n")
    fresh("a"); pg.keyboard.press("Tab"); expect("Tab do násobku 4", val(), "a   ")
    fresh("x"); pg.keyboard.press("Control+/"); expect("komentář zap", val(), "# x")
    pg.keyboard.press("Control+/"); expect("komentář vyp", val(), "x")
    fresh("a\nb"); pg.keyboard.press("Control+A"); pg.keyboard.press("Tab"); expect("blokové odsazení", val(), "    a\n    b")
    pg.keyboard.press("Shift+Tab"); expect("blokové předsazení", val(), "a\nb")
    ta.fill("\tx  \n\n\n\n\ny"); pg.keyboard.press("Control+Shift+F"); expect("zarovnání", val(), "    x\n\n\ny\n")
    fresh("a"); pg.keyboard.press("Enter"); pg.keyboard.press("Control+Z"); expect("zpět funguje", val(), "a")
    pg.keyboard.press("Escape"); pg.keyboard.press("Tab")  # Esc+Tab = opuštění editoru, nic se nevloží
    expect("Esc+Tab", val(), "a")

    # našeptávač
    fresh("pri"); pg.wait_for_selector(".ac:not([hidden])")
    assert "print" in pg.inner_text(".ac")
    pg.keyboard.press("Enter"); expect("našeptávač vloží úryvek", val(), "print()")
    assert ta.evaluate("e => e.selectionStart") == 6, "kurzor v závorce"
    fresh("def"); pg.wait_for_selector(".ac:not([hidden])"); pg.keyboard.press("Tab")
    expect("úryvek def", val(), "def ():\n    ")
    fresh("for"); pg.keyboard.press("Escape")
    fresh("moje_promenna = 1\nmoje_"); pg.wait_for_selector(".ac:not([hidden])")
    assert "moje_promenna" in pg.inner_text(".ac")
    pg.keyboard.press("Escape"); assert hidden()
    fresh("s = 'a'\ns."); pg.wait_for_selector(".ac:not([hidden])"); assert "append" in pg.inner_text(".ac") or "split" in pg.inner_text(".ac")
    pg.keyboard.press("Escape")
    fresh('# print'); assert hidden(), "v komentáři se nenašeptává"


    # f-řetězce: zvýraznění
    pg.evaluate("import('/js/editor/highlight.js').then(m => window.__hl = m.highlight)"); pg.wait_for_function("typeof window.__hl === 'function'")
    h = pg.evaluate("s => window.__hl(s)", 'print(f"Ahoj {jmeno}, ti {vek + 1:>{w}} {len(a):.2f} {d[\'k\']!r} {{x}}")')
    for cls in ("c-brace", "c-var", "c-num", "c-spec", "c-par", "c-bi", "c-str"):
        if f'class="{cls}"' not in h: fails.append("f-řetězec: chybí " + cls)
    if h.count('class="c-brace"') != 10: fails.append(f"f-řetězec: špatný počet závorek {h.count('class=\"c-brace\"')}")
    if 'class="c-var">jmeno<' not in h or 'class="c-var">vek<' not in h: fails.append("f-řetězec: proměnné nejsou odlišené")
    if "{{x}}" not in h: fails.append("f-řetězec: {{ }} se má brát jako text")
    plain = pg.evaluate("s => window.__hl(s)", 'x = "{a}"')
    if "c-brace" in plain: fails.append("obyčejný řetězec nemá mít barevné závorky")

    # f-řetězce: psaní a našeptávač
    fresh('jmeno = "Eva"\nvek = 15\nprint(f"Ahoj ')
    pg.keyboard.type("{")
    expect("{ se spáruje", val().split("\n")[-1], 'print(f"Ahoj {}")')
    pg.wait_for_selector(".ac:not([hidden])"); acs = pg.inner_text(".ac")
    assert "jmeno" in acs and "vek" in acs, "po { se nabídnou proměnné: " + acs
    pg.keyboard.type("jm"); pg.keyboard.press("Enter")
    expect("vložení proměnné v {}", val().split("\n")[-1], 'print(f"Ahoj {jmeno}")')
    pg.keyboard.press("ArrowRight")                                      # za }
    pg.keyboard.type(", ti je {v")
    pg.wait_for_selector(".ac:not([hidden])"); assert "vek" in pg.inner_text(".ac")
    pg.keyboard.press("Tab"); expect("druhá proměnná", val().split("\n")[-1], 'print(f"Ahoj {jmeno}, ti je {vek}")')
    fresh('moje = 1\nprint(f"pri'); assert hidden(), "v textu f-řetězce se nenašeptává"
    fresh('moje = 1\nprint("{mo'); assert hidden(), "v obyčejném řetězci se nenašeptává"
    fresh('moje = 1\nprint(f"{moje:>'); assert hidden(), "ve formátu se nenašeptává"
    fresh('s = "a"\nprint(f"{s.up'); pg.wait_for_selector(".ac:not([hidden])"); assert "upper" in pg.inner_text(".ac")
    pg.keyboard.press("Escape")
    fresh('def secti(a, b):\n    return a + b\nprint(f"{sec'); pg.wait_for_selector(".ac:not([hidden])")
    assert "secti" in pg.inner_text(".ac") and "funkce" in pg.inner_text(".ac")
    pg.keyboard.press("Escape")
    fresh('pocet = 3\nprin'); pg.keyboard.press("Escape")
    fresh('pocet = 3\nx = poc'); pg.wait_for_selector(".ac:not([hidden])"); assert "pocet" in pg.inner_text(".ac") and "proměnná" in pg.inner_text(".ac")
    pg.keyboard.press("Escape")

    # zvýrazňování a nápověda
    fresh('def f(): return "a" # k')
    html = pg.inner_html(".editor .ed-hl")
    for cls in ("c-kw", "c-fn", "c-str", "c-com"):
        if cls not in html: fails.append("chybí zvýraznění " + cls)
    if shots: pg.screenshot(path=str(shots / "editor.png"), clip={"x": 0, "y": 600, "width": 1000, "height": 300})
    pg.click(".editor .ed-help"); pg.wait_for_selector("dialog[open]")
    assert "Ctrl+/" in pg.inner_text("dialog"); pg.keyboard.press("Escape")
    # ukázka je jen ke čtení
    assert pg.locator(".ex-editor .ed-ta").evaluate("e => e.readOnly")
    assert pg.locator(".ex-editor .ed-help").count() == 0
    b.close()
srv.shutdown()
shutil.rmtree(ROOT / "workspace" / "demo", ignore_errors=True)
for f in fails: print("SELHÁNÍ:", f)
print("CHYBY JS:", errors) if errors else None
print("OK" if not fails and not errors else "NEPROŠLO")
sys.exit(1 if fails or errors else 0)
