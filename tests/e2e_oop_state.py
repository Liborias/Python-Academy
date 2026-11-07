"""Samostatné OOP 5–8: ukázky, odmítnuté operace, řešení a uložený postup."""
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

IDS = ['05-zapouzdreni-a-rozhrani', '06-pravidla-stavu-a-vyjimky', '07-property-a-dostupnost', '08-revize-skladu']
EXPECTED = [
    'Na začátku: 5\nPo příjmu: 8\nPo výdeji: 6\nObaly zůstaly: 2',
    'Nedostupný výdej odmítnut.\nPo odmítnutí: 5\nVýdej posledních kusů: 0\nNový příjem: 2',
    'Volné kusy: 5\nPo rezervaci: 2\nCelkem a rezervováno: 5 3\nPo uvolnění: 3\nDostupnost je pouze pro čtení.',
    "Před rezervací: {'KNIHA': 5, 'OBAL': 2}\nPo odmítnutí: {'KNIHA': 5, 'OBAL': 2}\nPo úspěchu: {'KNIHA': 3, 'OBAL': 1}\nSkutečný sklad: {'KNIHA': 3, 'OBAL': 1}",
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
            page.goto(f'{base}?t={server.token}#/kurz/oop/03-metody-a-prubeh-volani')
            page.wait_for_selector('.editor textarea')
            old_draft = '# Dřívější rozepsaný úkol z prvního modulu\n'
            page.locator('.editor textarea').fill(old_draft)
            page.locator('.done-toggle input').check()
            page.goto(f'{base}#/kurz/oop')
            page.wait_for_selector('.mod li')
            available = page.locator('.mod li').count()
            assert available >= 8
            assert f'{available} z 20 lekcí připraveno' in page.locator('.learning-plan').inner_text()
            for lid, expected in zip(IDS, EXPECTED):
                directory = root/'courses/oop/lessons'/lid
                title = json.loads((directory/'lesson.json').read_text('utf-8'))['title']
                page.goto(f'{base}#/kurz/oop/{lid}')
                page.wait_for_function('(title) => document.querySelector(".lesson h1")?.textContent === title', arg=title)
                page.wait_for_selector('.editor textarea')
                assert page.locator('.quiz fieldset').count() == 3
                page.click('[data-act="run-ex"]')
                page.wait_for_function("document.querySelector('.ex-console .status').textContent === 'Hotovo.'")
                assert page.locator('.ex-console pre.out').inner_text().strip() == expected
                page.click('[data-act="check"]')
                page.wait_for_selector('.results .res.bad')
                assert not page.is_checked('.done-toggle input')
                solution = (directory/'solution.py').read_text('utf-8')
                page.locator('.editor textarea').fill(solution)
                page.click('[data-act="check"]')
                page.wait_for_function("document.querySelectorAll('.results .res.ok').length > 0 && document.querySelectorAll('.results .res.bad').length === 0")
                assert page.is_checked('.done-toggle input')
                response = page.request.post(base+'api/workspace/save', headers={'X-Dilna-Token': server.token},
                                             data={'course': 'oop', 'lesson': lid, 'code': solution})
                assert response.ok, response.text()
                work = root/'workspace/oop'/lid
                assert (work/'reseni.py').read_text('utf-8') == solution
                if (directory/'files').exists():
                    assert (work/'skladova_karta.py').read_text('utf-8') == (directory/'files/skladova_karta.py').read_text('utf-8')
                page.reload()
                page.wait_for_selector('.editor textarea')
                assert page.locator('.editor textarea').input_value() == solution
                assert page.is_checked('.done-toggle input')
            page.goto(f'{base}#/kurz/oop/03-metody-a-prubeh-volani')
            page.wait_for_selector('.editor textarea')
            assert page.locator('.editor textarea').input_value() == old_draft
            assert page.is_checked('.done-toggle input')
            page.goto(f'{base}#/kurz/oop')
            page.wait_for_selector('.mod li')
            assert page.locator('.mod li.done').count() == 5
            page.goto(f'{base}#/')
            page.wait_for_selector('a.card[href="#/kurz/oop"]')
            assert '5 / 20 lekcí' in page.locator('a.card[href="#/kurz/oop"]').inner_text()
            assert not errors, errors
            browser.close()
        print('OK: OOP 5–8, ukázky, řešení, šablony, kvízy, skladová karta, osm připravených lekcí a původní postup')
    finally:
        server.runs.stop_all()
        server.shutdown()
        server.server_close()
