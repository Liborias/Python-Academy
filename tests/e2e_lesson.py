"""Test stránky lekce v prohlížeči (Playwright) s ukázkovým obsahem z tests/fixtures."""
import shutil, sys, threading
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.app import create_server

shots = Path(sys.argv[sys.argv.index("--shots") + 1]) if "--shots" in sys.argv else None
srv = create_server(ROOT, "127.0.0.1", 0, courses_dir=ROOT / "tests" / "fixtures")
port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{port}/"
errors = []
try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1000, "height": 900})
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.on("dialog", lambda d: d.accept())
        pg.goto(f"{base}?t={srv.token}#/kurz/demo")
        pg.wait_for_selector(".mod li")
        assert pg.locator(".mod li").count() == 2
        pg.click(".mod li a >> nth=0")
        pg.wait_for_selector(".lesson h1")
        assert "Pozdrav" in pg.inner_text("h1")
        assert pg.locator(".prose code").count() >= 2 and pg.locator(".prose a[rel~=noopener]").count() == 1
        assert pg.locator(".prose .note").count() == 1 and "<script" not in pg.inner_html(".prose")

        # ukázka s input()
        pg.click('[data-act="run-ex"]')
        pg.wait_for_selector(".ex-console .stdin:not([hidden])")
        pg.wait_for_function("document.querySelector('.ex-console .out').textContent.includes('Jak se jmenuješ?')")
        pg.fill(".ex-console .stdin input", "Eva"); pg.press(".ex-console .stdin input", "Enter")
        pg.wait_for_function("document.querySelector('.ex-console .out').textContent.includes('Ahoj Eva')")
        pg.wait_for_function("document.querySelector('.ex-console .status').textContent.includes('Hotovo')")

        # špatné řešení neprojde, správné projde
        pg.fill(".editor textarea", 'print("Ahoj Karle")')
        pg.click('[data-act="check"]')
        pg.wait_for_selector(".results .res.bad")
        pg.fill(".editor textarea", 'j = input("Jméno: ")\nprint("Ahoj", j)')
        pg.click('[data-act="check"]')
        pg.wait_for_selector(".results .res.ok")
        assert pg.is_checked(".done-toggle input"), "po úspěšné kontrole je lekce splněna"

        # kód se pamatuje po obnovení stránky
        pg.reload(); pg.wait_for_selector(".editor textarea")
        assert "Ahoj" in pg.input_value(".editor textarea")

        # chyba za běhu se ukáže
        pg.fill(".editor textarea", "print(1/0)")
        pg.click('[data-act="run"]')
        pg.wait_for_function("document.querySelector('.run-console .out .err')")
        assert "ZeroDivisionError" in pg.inner_text(".run-console .out")
        pg.wait_for_function("document.querySelector('.run-console .status').textContent.includes('chybou')")
        assert not pg.is_visible(".run-console .stdin"), "vstup se po skončení skryje"

        # VSCodium: uloží soubor, bez příkazu codium zobrazí ruční postup
        pg.fill(".editor textarea", "print('z editoru')")
        pg.click('[data-act="vsc"]')
        pg.wait_for_selector('[data-role="hint"] code')
        f = ROOT / "workspace" / "demo" / "01-pozdrav" / "reseni.py"
        assert f.read_text(encoding="utf-8") == "print('z editoru')"
        f.write_text("print('změna z VSCodium')", encoding="utf-8")
        pg.click('[data-act="reload"]')
        pg.wait_for_function("document.querySelector('.editor textarea').value.includes('VSCodium')")

        # kvíz
        pg.check('input[name="q0"][value="0"]'); assert "Zkuste" in pg.inner_text(".quiz .why")
        pg.check('input[name="q0"][value="1"]'); assert "Správně" in pg.inner_text(".quiz .why")

        if shots: pg.screenshot(path=str(shots / "lekce.png"), full_page=True)
        # navigace
        pg.click(".lesson-foot a.primary")
        pg.wait_for_function("document.querySelector('h1').textContent.includes('Funkce')")
        b.close()
finally:
    shutil.rmtree(ROOT / "workspace" / "demo", ignore_errors=True)
    srv.runs.stop_all(); srv.shutdown()
print("CHYBY:", errors) if errors else print("OK")
sys.exit(1 if errors else 0)
