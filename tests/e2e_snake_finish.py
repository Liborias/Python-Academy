"""Dokončení Snake: nové lekce, řešení, pracovní soubory a zachování postupu."""
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

IDS = ['33-snake-potrava-a-rust', '34-snake-kolize-s-telem', '35-snake-skore-a-stav', '36-snake-hotova-hra']
EXPECTED = [
    'Nová hlava: (5, 1) délka: 4\nPřes okraj: (0, 1) délka: 4',
    'Do odcházejícího ocasu: (0, 1)\nKolize zachycena; tělo: [(0, 1), (1, 1), (1, 0), (0, 0)]',
    'Start: hra skóre: 0\nKrok: hra skóre: 10 délka: 3\nKrok: hra skóre: 20 délka: 4',
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
            assert page.locator('.mod li').count() >= 36
            page.goto(f'{base}#/kurz/turtle-oop/32-snake-ovladani')
            page.wait_for_selector('.done-toggle input')
            page.locator('.done-toggle input').check()
            for index, lid in enumerate(IDS):
                directory = root/'courses/turtle-oop/lessons'/lid
                metadata = json.loads((directory/'lesson.json').read_text('utf-8'))
                page.goto(f'{base}#/kurz/turtle-oop/{lid}')
                page.wait_for_function('(title) => document.querySelector(".lesson h1")?.textContent === title', arg=metadata['title'])
                page.wait_for_selector('.editor textarea')
                assert page.locator('.quiz fieldset').count() == 3
                assert page.locator('.meta .badge').count() == int(index == 3)
                if index < 3:
                    page.click('[data-act="run-ex"]')
                    page.wait_for_function("document.querySelector('.ex-console .status').textContent === 'Hotovo.'")
                    assert page.locator('.ex-console pre.out').inner_text().strip() == EXPECTED[index]
                else:
                    page.click('[data-act="check"]')
                    page.wait_for_selector('.results .res.bad')
                    assert not page.is_checked('.done-toggle input')
                solution = (directory/'solution.py').read_text('utf-8')
                page.locator('.editor textarea').fill(solution)
                page.click('[data-act="check"]')
                page.wait_for_function("document.querySelectorAll('.results .res.ok').length > 0 && document.querySelectorAll('.results .res.bad').length === 0")
                assert page.is_checked('.done-toggle input')
                response = page.request.post(base+'api/workspace/save', headers={'X-Dilna-Token': server.token},
                                             data={'course': 'turtle-oop', 'lesson': lid, 'code': solution})
                assert response.ok, response.text()
                work = root/'workspace/turtle-oop'/lid
                assert (work/'reseni.py').read_text('utf-8') == solution
                for path in (directory/'files').glob('*.py'):
                    assert (work/path.name).read_text('utf-8') == path.read_text('utf-8')
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
        print('OK: Snake 33–36, tři konzolové ukázky, řešení, šablona, kvízy, pracovní moduly a zachování postupu')
    finally:
        server.runs.stop_all()
        server.shutdown()
        server.server_close()
