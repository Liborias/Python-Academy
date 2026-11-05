"""Závěrečný projekt kvízu: skutečný konzolový vstup, kontroly a stav kurzu."""
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

IDS = ['37-kviz-otazka-a-skore', '38-kviz-data-json', '39-kviz-api-a-zaloha', '40-kviz-hotova-aplikace']
EXPECTED = [
    'Seznam lze měnit.\nPrvní odpověď je správná: True\nDruhá odpověď je správná: True\nSkóre: 2 z 2',
    'Počet otázek: 5\nPrvní: Pythonovský seznam lze měnit po vytvoření.\nSprávná odpověď: True',
    'Zdroj: offline otázky: 5\nZdroj: API otázky: 2\nZdroj: záloha otázky: 5\nAPI nelze použít: Ukázkový výpadek spojení',
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
            assert page.locator('.mod li').count() == 40
            page.goto(f'{base}#/kurz/turtle-oop/36-snake-hotova-hra')
            page.wait_for_selector('.done-toggle input')
            page.locator('.done-toggle input').check()
            for index, lid in enumerate(IDS):
                directory = root/'courses/turtle-oop/lessons'/lid
                title = json.loads((directory/'lesson.json').read_text('utf-8'))['title']
                page.goto(f'{base}#/kurz/turtle-oop/{lid}')
                page.wait_for_function('(title) => document.querySelector(".lesson h1")?.textContent === title', arg=title)
                page.wait_for_selector('.editor textarea')
                assert page.locator('.quiz fieldset').count() == 3
                assert page.locator('.meta .badge').count() == 0
                page.click('[data-act="run-ex"]')
                if index < 3:
                    page.wait_for_function("document.querySelector('.ex-console .status').textContent === 'Hotovo.'")
                    assert page.locator('.ex-console pre.out').inner_text().strip() == EXPECTED[index]
                else:
                    def send(value):
                        field = page.locator('.ex-console .stdin input')
                        field.fill(value)
                        field.press('Enter')
                    page.wait_for_function("document.querySelector('.ex-console .out').textContent.includes('Zdroj [')")
                    send('')
                    page.wait_for_function("document.querySelector('.ex-console .out').textContent.includes('1/5:')")
                    send('?')
                    page.wait_for_function("document.querySelector('.ex-console .out').textContent.includes('Zadejte a, n nebo q.')")
                    for number, answer in enumerate([' A ', 'n', 'a', 'N', 'a'], 1):
                        page.wait_for_function('(n) => document.querySelector(".ex-console .out").textContent.includes(`${n}/5:`)', arg=number)
                        send(answer)
                    page.wait_for_function("document.querySelector('.ex-console .status').textContent === 'Hotovo.'")
                    assert 'Výsledek: 5/5' in page.locator('.ex-console pre.out').inner_text()
                    page.click('[data-act="run-ex"]')
                    page.wait_for_function("document.querySelector('.ex-console .out').textContent.includes('Zdroj [')")
                    send('')
                    page.wait_for_function("document.querySelector('.ex-console .out').textContent.includes('1/5:')")
                    send('a')
                    page.wait_for_function("document.querySelector('.ex-console .out').textContent.includes('2/5:')")
                    send(' Q ')
                    page.wait_for_function("document.querySelector('.ex-console .status').textContent === 'Hotovo.'")
                    assert 'Průběžné skóre: 1/1' in page.locator('.ex-console pre.out').inner_text()
                    page.click('[data-act="check"]')
                    page.wait_for_selector('.results .res.bad')
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
                if (directory/'files').exists():
                    for path in (directory/'files').iterdir():
                        if path.is_file():
                            assert (work/path.name).read_bytes() == path.read_bytes()
                page.reload()
                page.wait_for_selector('.editor textarea')
                assert page.locator('.editor textarea').input_value() == solution
                assert page.is_checked('.done-toggle input')
            assert page.locator('.lesson-foot a.primary').count() == 0
            page.goto(f'{base}#/kurz/turtle-oop')
            page.wait_for_selector('.mod li')
            assert page.locator('.mod li.done').count() == 5
            page.goto(f'{base}#/kurz/oop')
            page.wait_for_selector('.learning-plan')
            assert page.locator('.mod li').count() >= 4
            assert not errors, errors
            browser.close()
        print('OK: 40 lekcí, kvíz 37–40, simulace API i záloha, živý konzolový vstup, 5/5, předčasný konec, kontroly a zachování postupu')
    finally:
        server.runs.stop_all()
        server.shutdown()
        server.server_close()
