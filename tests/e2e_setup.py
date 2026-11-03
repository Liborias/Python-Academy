"""Test stránky Příprava prostředí."""
import sys, threading, shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.app import create_server
srv = create_server(ROOT, "127.0.0.1", 0); threading.Thread(target=srv.serve_forever, daemon=True).start()
errors = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=shutil.which('chromium') or None, args=['--no-sandbox']); pg = b.new_page(viewport={"width": 1000, "height": 900})
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.goto(f"http://127.0.0.1:{srv.server_address[1]}/?t={srv.token}#/priprava")
    pg.wait_for_function("document.querySelector('#setup-doc h3')")
    assert "Windows" in pg.inner_text("#setup-doc")
    pg.click('button[data-t="vscodium"]')
    pg.wait_for_function("document.querySelectorAll('input[data-chk]').length >= 8")
    pg.check('input[data-chk="chk-2"]')
    pg.goto(pg.url); pg.click('a[href="#/priprava"]'); pg.click('button[data-t="vscodium"]')
    pg.wait_for_function("document.querySelectorAll('input[data-chk]').length >= 8")
    assert pg.is_checked('input[data-chk="chk-2"]'), "zaškrtnutí se pamatuje"
    pg.click('button[data-t="reseni-problemu"]')
    pg.wait_for_function("document.querySelector('#setup-doc').textContent.includes('Python Environments')")
    pg.screenshot(path=sys.argv[1]) if len(sys.argv) > 1 else None
    b.close()
srv.shutdown()
print("CHYBY:", errors) if errors else print("OK")
sys.exit(1 if errors else 0)
