"""Samostatné OOP 13–16: výpis, rovnost, dataclass, unittest a zachovaný postup."""
import json
import os
import shutil
import sys
import subprocess
import tempfile
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.app import create_server

IDS = ['13-str-a-repr', '14-identita-a-rovnost', '15-dataclass-a-vlastni-seznam', '16-testy-objektu']
EXPECTED = [
    "Pro zákazníka: Balík B-001, 1200 g\nPro vývojáře: PopsanyBalik('B-001', 1200)\nV seznamu: [PopsanyBalik('B-001', 1200)]",
    'Dvě instance: False\nStejné údaje: True\nTentýž objekt: True\nPo opravě PSČ: False\nPůvodní PSČ: 60200',
    "Poznámek po zápisu: 1\nPrvní poznámky: ['Nezvonit.']\nDruhý štítek: []\nShodná data: True\nZáznam: ExpedicniStitek(kod='E-001', adresa=Adresa('Javorová 1', 'Brno', '60200'), poznamky=['Nezvonit.'])",
    None,
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
            page.goto(f'{base}?t={server.token}#/kurz/oop/12-doprava-jako-spoluprace')
            page.wait_for_selector('.editor textarea')
            old_draft = '# Dřívější rozepsaný úkol z třetího modulu\n'
            page.locator('.editor textarea').fill(old_draft)
            page.locator('.done-toggle input').check()
            page.goto(f'{base}#/kurz/oop')
            page.wait_for_selector('.mod li')
            available = page.locator('.mod li').count()
            assert available >= 16
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
                output = page.locator('.ex-console pre.out').inner_text().strip()
                if expected is None:
                    assert 'Ran 4 tests' in output and output.endswith('OK'), output
                    assert 'test_odmitnuta_zmena' in output
                    assert page.locator('.ex-console pre.out .err').count() > 0
                else:
                    assert output == expected, output
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
                for helper in (directory/'files').glob('*.py'):
                    assert (work/helper.name).read_bytes() == helper.read_bytes()
                if lid == '16-testy-objektu':
                    # Stejný uložený soubor funguje také standardním příkazem z výkladu.
                    result = subprocess.run([os.environ.get('DILNA_TEST_PYTHON', sys.executable), '-m', 'unittest', '-v', 'reseni'],
                                            cwd=work, capture_output=True, text=True, timeout=20)
                    assert result.returncode == 0 and 'Ran 4 tests' in result.stderr and result.stderr.rstrip().endswith('OK'), result.stderr
                page.reload()
                page.wait_for_selector('.editor textarea')
                assert page.locator('.editor textarea').input_value() == solution
                assert page.is_checked('.done-toggle input')
            page.goto(f'{base}#/kurz/oop/12-doprava-jako-spoluprace')
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
        print('OK: OOP 13–16, ukázky včetně unittest, řešení, šablony, kvízy, pomocné moduly, příkaz unittest ve workspace a původní postup')
    finally:
        server.runs.stop_all()
        server.shutdown()
        server.server_close()
