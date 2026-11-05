"""Katalog a plán samostatného OOP kurzu vedle prvních skutečných lekcí."""
import shutil
import sys
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.app import create_server

server = create_server(ROOT, '127.0.0.1', 0)
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f'http://127.0.0.1:{server.server_address[1]}/'
errors = []
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=shutil.which('chromium') or None, args=['--no-sandbox'])
        page = browser.new_page(viewport={'width':1100,'height':900})
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto(f'{base}?t={server.token}')
        card = page.locator('a.card[href="#/kurz/oop"]')
        card.wait_for()
        assert 'Rozpracováno' in card.inner_text()
        assert '0 / 20 lekcí' in card.inner_text()
        assert '0 / 0' not in card.inner_text()
        assert card.locator('.bar').count()==1
        card.click()
        panel = page.locator('.learning-plan')
        panel.wait_for()
        assert 'Chytré expediční centrum' in panel.inner_text()
        assert '3/4' in panel.inner_text()
        assert '4 z 20 lekcí připraveno' in panel.inner_text()
        assert 'zatím bez realizace' not in panel.inner_text()
        assert page.locator('.mod li').count()==4
        assert page.locator('.editor, .ex-editor, .run-console').count()==0
        assert not panel.locator('details').evaluate('(el) => el.open')
        panel.locator('summary').click()
        text = panel.inner_text()
        assert 'Modul 1' in text and 'Modul 5' in text
        assert 'procházet testy' in text
        assert panel.locator('a[href="https://github.com/cosmicpython/code"]').count()==1
        assert panel.locator('button, textarea, [data-act]').count()==0
        page.set_viewport_size({'width':380,'height':800})
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        page.reload()
        panel.wait_for()
        assert 'Chytré expediční centrum' in panel.inner_text()
        page.goto(f'{base}#/kurz/turtle-oop')
        page.wait_for_selector('.mod li')
        assert page.locator('.learning-plan').count()==0
        assert page.locator('.mod li').count()>=24
        assert not errors,errors
        browser.close()
    print('OK: samostatná karta OOP, plán 20 lekcí, obtížnost 3/4, oddělené Turtle, první čtyři lekce, mobil')
finally:
    server.runs.stop_all(); server.shutdown(); server.server_close()
