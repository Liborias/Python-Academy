"""Závěrečný OOP projekt 17–20: rezervace, storno, živá konzole a pracovní složka."""
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

IDS = ['17-navrh-expedicniho-centra', '18-rezervace-a-bezpecne-storno', '19-centrum-a-vymenna-doprava', '20-konzolove-expedicni-centrum']
EXPECTED = [
    "Zboží celkem: 780\nPožadavek: {'KNIHA': 3, 'OBAL': 1}\nPo uzavření: {'KNIHA': 3, 'OBAL': 1}",
    "Po první rezervaci: {'KNIHA': 2}\nPo druhé rezervaci: {'KNIHA': 0}\nPo stornu první: {'KNIHA': 3}\nDruhé storno odmítnuto: {'KNIHA': 3}\nDruhá objednávka: rezervovana",
    "Kurýr: 99\nCyklodoprava: 59\nNabídka: 559\nPo stornu: {'KNIHA': 5}\nStornovanou objednávku již neměníme.",
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
    run_requests = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=shutil.which('chromium') or None, args=['--no-sandbox'])
            page = browser.new_page(viewport={'width': 1100, 'height': 900})
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.on('request', lambda request: run_requests.append(request.post_data_json) if request.url.endswith('/api/run') and request.method == 'POST' else None)
            page.goto(f'{base}?t={server.token}#/kurz/oop/16-testy-objektu')
            page.wait_for_selector('.editor textarea')
            old_draft = '# Dřívější rozepsaný úkol ze čtvrtého modulu\n'
            page.locator('.editor textarea').fill(old_draft)
            page.locator('.done-toggle input').check()
            page.goto(f'{base}#/kurz/oop')
            page.wait_for_selector('.mod li')
            available = page.locator('.mod li').count()
            assert available == 20
            assert f'{available} z 20 lekcí připraveno' in page.locator('.learning-plan').inner_text()
            for lid, expected in zip(IDS, EXPECTED):
                directory = root/'courses/oop/lessons'/lid
                title = json.loads((directory/'lesson.json').read_text('utf-8'))['title']
                page.goto(f'{base}#/kurz/oop/{lid}')
                page.wait_for_function('(title) => document.querySelector(".lesson h1")?.textContent === title', arg=title)
                page.wait_for_selector('.editor textarea')
                assert page.locator('.quiz fieldset').count() == 3
                page.click('[data-act="run-ex"]')
                if expected is None:
                    page.wait_for_function("document.querySelector('.ex-console .out').textContent.includes('Příkazy:')")
                    assert run_requests[-1]["timeout"] == 600
                    page.wait_for_function("document.querySelector('.ex-console .out').textContent.includes('Příkazy:')")
                    def send(command, marker):
                        offset = page.locator('.ex-console pre.out').evaluate('(el) => el.textContent.length')
                        field = page.locator('.ex-console .stdin input')
                        field.fill(command)
                        field.press('Enter')
                        page.wait_for_function('({offset, marker}) => document.querySelector(".ex-console .out").textContent.slice(offset).includes(marker)', arg={'offset': offset, 'marker': marker})
                    for command, marker in [
                        ('stav', 'Sklad: KNIHA=5, OBAL=2'), ('nova A 2 1 1200', 'Přijato: A'),
                        ('doprava A kolo', 'Doprava: 59 Kč'), ('poznamka A Nezvonit prosím', 'Poznámek: 1'),
                        ('prehled A', 'Nabídka: 589 Kč'), ('nova B 4 0 800', 'Odmítnuto:'),
                        ('storno A', 'Stornováno: A'), ('storno A', 'Odmítnuto:'),
                        ('nova B 4 0 800', 'Přijato: B'), ('stav', 'Sklad: KNIHA=1, OBAL=2'),
                        ('konec', 'Na shledanou.')]:
                        send(command, marker)
                    page.wait_for_function("document.querySelector('.ex-console .status').textContent === 'Hotovo.'")
                else:
                    page.wait_for_function("document.querySelector('.ex-console .status').textContent === 'Hotovo.'")
                    assert page.locator('.ex-console pre.out').inner_text().strip() == expected
                    assert run_requests[-1]['timeout'] == 20
                page.click('[data-act="check"]')
                page.wait_for_selector('.results .res.bad')
                assert not page.is_checked('.done-toggle input')
                solution = (directory/'solution.py').read_text('utf-8')
                page.locator('.editor textarea').fill(solution)
                if lid == '20-konzolove-expedicni-centrum':
                    page.click('[data-act="run"]')
                    page.wait_for_function("document.querySelector('.run-console pre.out').textContent.includes('Příkazy:')")
                    assert run_requests[-1]['timeout'] == 600
                    field = page.locator('.run-console .stdin input')
                    field.fill('konec')
                    field.press('Enter')
                    page.wait_for_function("document.querySelector('.run-console .status').textContent === 'Hotovo.'")
                page.click('[data-act="check"]')
                page.wait_for_function("document.querySelectorAll('.results .res.ok').length > 0 && document.querySelectorAll('.results .res.bad').length === 0")
                assert page.is_checked('.done-toggle input')
                response = page.request.post(base+'api/workspace/save', headers={'X-Dilna-Token': server.token},
                                             data={'course': 'oop', 'lesson': lid, 'code': solution})
                assert response.ok, response.text()
                work = root/'workspace/oop'/lid
                assert (work/'reseni.py').read_text('utf-8') == solution
                for helper in (directory/'files').iterdir():
                    assert (work/helper.name).read_bytes() == helper.read_bytes()
                if lid == '20-konzolove-expedicni-centrum':
                    # Stejný uložený soubor funguje také standardním příkazem z výkladu.
                    result = subprocess.run([os.environ.get('DILNA_TEST_PYTHON', sys.executable), '-m', 'unittest', '-v', 'test_centrum'],
                                            cwd=work, capture_output=True, text=True, timeout=20)
                    assert result.returncode == 0 and 'Ran 4 tests' in result.stderr and result.stderr.rstrip().endswith('OK'), result.stderr
                    result = subprocess.run([os.environ.get('DILNA_TEST_PYTHON', sys.executable), 'reseni.py'], cwd=work,
                                            input=(directory/'example.stdin').read_text('utf-8'), capture_output=True, text=True, timeout=20)
                    assert result.returncode == 0 and 'Sklad: KNIHA=1, OBAL=2' in result.stdout and 'Na shledanou.' in result.stdout, result.stderr
                    assert (work/'README.md').exists()
                page.reload()
                page.wait_for_selector('.editor textarea')
                assert page.locator('.editor textarea').input_value() == solution
                assert page.is_checked('.done-toggle input')
            assert page.locator('.lesson-foot a.primary').count() == 0
            page.goto(f'{base}#/kurz/oop/16-testy-objektu')
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
        print('OK: OOP 20/20, lekce 17–20, živý konzolový scénář, odmítnuté operace, řešení, šablony, kvízy, README, moduly, unittest/CLI ve workspace a původní postup')
    finally:
        server.runs.stop_all()
        server.shutdown()
        server.server_close()
