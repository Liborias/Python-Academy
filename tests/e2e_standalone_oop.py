"""Samostatný OOP: první modul, skutečné výstupy, drafty a oddělení od Turtle."""
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

IDS = ['01-od-slovniku-k-objektu', '02-konstruktor-a-self', '03-metody-a-prubeh-volani', '04-objednavka-a-jeji-polozky']
EXPECTED = [
    'Slovník: B-001 2\nPrvní balíček: B-001 3\nDruhý balíček: B-002 5',
    'Průvodce Pythonem 250 2\nDárkový obal 30 1\nPo změně: 3 1',
    'Na začátku: 500\nNový počet: 3\nPo přidání: 750\nDruhé čtení: 750',
    'Objednávka: OBJ-001 celkem: 310\nPo změně položky: 560\nŘádky po úpravě přehledu: 2\nDruhá objednávka: 0',
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
            page.goto(f'{base}?t={server.token}#/kurz/turtle-oop/17-trida-a-instance')
            page.wait_for_selector('.editor textarea')
            old_draft = '# Můj rozpracovaný původní úkol\n'
            page.locator('.editor textarea').fill(old_draft)
            page.locator('.done-toggle input').check()
            page.goto(f'{base}#/kurz/oop')
            page.wait_for_selector('.mod li')
            available = page.locator('.mod li').count()
            assert available >= 4
            panel = page.locator('.learning-plan')
            assert f'{available} z 20 lekcí připraveno' in panel.inner_text()
            assert 'zatím bez realizace' not in panel.inner_text()
            assert page.locator('.course-preparation').count() == 1
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
                    assert (work/'polozka.py').read_text('utf-8') == (directory/'files/polozka.py').read_text('utf-8')
                page.reload()
                page.wait_for_selector('.editor textarea')
                assert page.locator('.editor textarea').input_value() == solution
                assert page.is_checked('.done-toggle input')
            page.goto(f'{base}#/kurz/oop')
            page.wait_for_selector('.mod li')
            assert page.locator('.mod li.done').count() == 4
            page.goto(f'{base}#/')
            page.wait_for_selector('a.card[href="#/kurz/oop"]')
            assert '4 / 20 lekcí' in page.locator('a.card[href="#/kurz/oop"]').inner_text()
            page.goto(f'{base}#/kurz/turtle-oop/17-trida-a-instance')
            page.wait_for_selector('.editor textarea')
            assert page.is_checked('.done-toggle input')
            assert page.locator('.editor textarea').input_value() == old_draft
            page.goto(f'{base}#/kurz/turtle-oop')
            page.wait_for_selector('.mod li')
            available = page.locator('.mod li').count()
            assert available >= 40
            assert not errors, errors
            browser.close()
        print('OK: samostatné OOP 1–4, ukázky, řešení, šablony, kvízy, modul položky, 4/20 a oddělený původní postup')
    finally:
        server.runs.stop_all()
        server.shutdown()
        server.server_close()
