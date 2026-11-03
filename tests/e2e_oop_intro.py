"""OOP lekce 17–20: dostupnost v kurzu, ukázky a skutečné odeslání řešení."""
import json
import os
import shutil
import sys
import tempfile
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.app import create_server

IDS = ['17-trida-a-instance','18-konstruktor-init','19-metody-a-stav','20-vlastni-seznam-objektu']
EXPECTED = ['Vydra 9\nJezevec 3\n10','Řeka 80\n81 200','21\n19\n19 22',"1\n['Lesní cesta']\n[]"]
with tempfile.TemporaryDirectory() as temp:
    root = Path(temp)
    for name in ['courses','lib','web']:
        shutil.copytree(ROOT/name, root/name)
    server = create_server(root, '127.0.0.1', 0, python=os.environ.get('DILNA_TEST_PYTHON'))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_address[1]}/'
    errors = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=shutil.which('chromium') or None, args=['--no-sandbox'])
            page = browser.new_page(viewport={'width':1100, 'height':900})
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto(f'{base}?t={server.token}#/kurz/turtle-oop')
            page.wait_for_selector('.mod li')
            assert page.locator('.mod li').count() >= 20
            assert page.locator('.mod li.done').count() == 0
            for lid, expected in zip(IDS, EXPECTED):
                directory = root/'courses/turtle-oop/lessons'/lid
                title = json.loads((directory/'lesson.json').read_text('utf-8'))['title']
                page.goto(f'{base}#/kurz/turtle-oop/{lid}')
                page.wait_for_function('(title) => document.querySelector(".lesson h1")?.textContent === title', arg=title)
                page.wait_for_selector('.editor textarea')
                assert page.locator('.quiz fieldset').count() == 3
                page.click('[data-act="run-ex"]')
                page.wait_for_function("document.querySelector('.ex-console .status').textContent === 'Hotovo.'")
                assert page.locator('.ex-console pre.out').inner_text().strip() == expected, lid
                page.locator('.editor textarea').fill((directory/'solution.py').read_text('utf-8'))
                page.click('[data-act="check"]')
                page.wait_for_selector('.results .res.ok')
                assert page.is_checked('.done-toggle input')
            page.goto(f'{base}#/kurz/turtle-oop')
            page.wait_for_selector('.mod li')
            assert page.locator('.mod li.done').count() == 4
            assert not errors, errors
            browser.close()
        print('OK: OOP 17–20, 4 ukázky s výstupy, 4 řešení a jejich postup, kvízy a přehled kurzu')
    finally:
        server.runs.stop_all(); server.shutdown(); server.server_close()
