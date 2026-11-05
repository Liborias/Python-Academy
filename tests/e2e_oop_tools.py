"""Lekce 25–28 kombinovaného kurzu v prohlížeči, včetně běhu a zachování postupu."""
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

IDS = ['25-specialni-metody', '26-identita-a-rovnost', '27-poradi-dedeni-mro', '28-dataclass']
EXPECTED = [
    "Doma, knih: 2\nPolicka(nazev='Doma', knihy=['Les', 'Řeka'])\n2\n[Policka(nazev='Doma', knihy=['Les', 'Řeka'])]",
    'True\nFalse\nTrue\nFalse\nFalse',
    "['Znacka', 'Ramovani', 'Zvyrazneni', 'Popisek', 'object']\n['rámeček', 'zvýraznění', 'popisek']\n['rámeček', 'popisek']",
    "Vyprava(cil='Les', ucastnici=[])\n['Ema']\n[]\nTrue",
]

with tempfile.TemporaryDirectory() as temp:
    root = Path(temp)
    for name in ['courses', 'web', 'lib']:
        shutil.copytree(ROOT/name, root/name)
    server = create_server(root, '127.0.0.1', 0, python=os.environ.get('DILNA_TEST_PYTHON'))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_address[1]}/'
    errors = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=shutil.which('chromium') or None, args=['--no-sandbox'])
            page = browser.new_page(viewport={'width': 1100, 'height': 900})
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto(f'{base}?t={server.token}#/kurz/turtle-oop')
            page.wait_for_selector('.mod li')
            assert page.locator('.mod li').count() >= 28
            # Dříve dokončená lekce zůstane splněná i po práci na nových lekcích.
            page.goto(f'{base}#/kurz/turtle-oop/24-super-a-rozsireni')
            page.wait_for_selector('.done-toggle input')
            page.locator('.done-toggle input').check()
            for lid, expected in zip(IDS, EXPECTED):
                directory = root/'courses/turtle-oop/lessons'/lid
                metadata = json.loads((directory/'lesson.json').read_text('utf-8'))
                page.goto(f'{base}#/kurz/turtle-oop/{lid}')
                page.wait_for_function('(title) => document.querySelector(".lesson h1")?.textContent === title', arg=metadata['title'])
                page.wait_for_selector('.editor textarea')
                assert page.locator('.quiz fieldset').count() == 3
                assert page.locator('.ex-editor textarea').input_value() == (directory/'example.py').read_text('utf-8')
                page.click('[data-act="run-ex"]')
                page.wait_for_function("document.querySelector('.ex-console .status').textContent === 'Hotovo.'")
                assert page.locator('.ex-console pre.out').inner_text().strip() == expected, lid
                solution = (directory/'solution.py').read_text('utf-8')
                page.locator('.editor textarea').fill(solution)
                page.click('[data-act="check"]')
                page.wait_for_selector('.results .res.ok')
                assert page.is_checked('.done-toggle input')
                page.reload()
                page.wait_for_selector('.editor textarea')
                assert page.locator('.editor textarea').input_value() == solution
                assert page.is_checked('.done-toggle input')
            page.goto(f'{base}#/kurz/turtle-oop')
            page.wait_for_selector('.mod li')
            assert page.locator('.mod li.done').count() == 5
            page.goto(f'{base}#/kurz/oop')
            page.wait_for_selector('.learning-plan')
            assert page.locator('.mod li').count() >= 4
            assert not errors, errors
            browser.close()
        print('OK: OOP 25–28, 4 ukázky, 4 řešení, kvízy, drafty a zachování dosavadního postupu; samostatné OOP má vlastní lekce')
    finally:
        server.runs.stop_all()
        server.shutdown()
        server.server_close()
