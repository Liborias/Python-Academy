"""Test webu v prohlížeči (Playwright). Spuštění: python tests/e2e_web.py [--shots DIR]"""
import sys, threading, shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.app import create_server

shots = Path(sys.argv[sys.argv.index("--shots") + 1]) if "--shots" in sys.argv else None
srv = create_server(ROOT, "127.0.0.1", 0)
port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{port}/"
errors = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=shutil.which('chromium') or None, args=['--no-sandbox'])
    pg = b.new_page(viewport={"width": 1100, "height": 800})
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.on("console", lambda m: m.type == "error" and "fonts.g" not in m.text and "ERR_" not in m.text and errors.append(m.text))
    pg.goto(f"{base}?t={srv.token}")
    pg.wait_for_selector(".card")
    assert pg.locator(".card").count() == 10, "10 podkurzů včetně samostatného návrhu OOP"
    assert "t=" not in pg.url, "token odstraněn z adresy"
    pg.click('.filters button[data-l="4"]')
    assert pg.locator(".card").count() == 2, "filtr obtížnosti 4"
    pg.click('.filters button[data-l="0"]')
    if shots: pg.screenshot(path=str(shots / "katalog-svetly.png"))
    pg.click("#theme")
    assert pg.evaluate("document.documentElement.dataset.theme") in ("dark", "light")
    if shots: pg.screenshot(path=str(shots / "katalog-tmavy.png"))
    pg.click('a.card[href="#/kurz/pygame-2"]')
    pg.wait_for_function("document.querySelector('h1').textContent.includes('Pygame 2')")
    assert pg.locator(".chip").count() == 2, "tipy předpokladů"
    if shots: pg.screenshot(path=str(shots / "kurz.png"))
    pg.set_viewport_size({"width": 380, "height": 800})
    pg.goto(f"{base}#/")
    pg.wait_for_selector(".card")
    assert pg.evaluate("document.documentElement.scrollWidth <= innerWidth"), "bez vodorovného posunu"
    if shots: pg.screenshot(path=str(shots / "mobil.png"))
    pg.goto(f"{base}#/neexistuje")
    pg.wait_for_function("document.querySelector('h1').textContent.includes('nenalezena')")
    b.close()
srv.shutdown()
print("CHYBY:", errors) if errors else print("OK")
sys.exit(1 if errors else 0)
