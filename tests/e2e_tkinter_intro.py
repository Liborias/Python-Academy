"""První Tkinter: plán, příprava, kontroly, pracovní soubor a oddělený postup."""
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

IDS = ['01-prvni-okno-a-mainloop', '02-popisky-a-pack', '03-tlacitka-a-zpetna-volani', '04-vstupni-pole-a-grid']
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
            page = browser.new_page(viewport={'width':1100, 'height':900})
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto(f'{base}?t={server.token}#/kurz/oop/20-konzolove-expedicni-centrum')
            page.wait_for_selector('.editor textarea')
            previous = '# Můj dřívější rozepsaný OOP projekt\n'
            page.locator('.editor textarea').fill(previous)
            page.locator('.done-toggle input').check()
            page.goto(f'{base}#/')
            card = page.locator('a.card[href="#/kurz/tkinter-api"]')
            card.wait_for()
            assert 'Rozpracováno' in card.inner_text() and '0 / 28 lekcí' in card.inner_text()
            card.click()
            page.wait_for_selector('.mod li')
            assert page.locator('.mod li').count() == 8
            assert '8 z 28 lekcí připraveno' in page.locator('.learning-plan').inner_text()
            assert page.locator('.course-preparation').count() == 1
            assert 'Prvních osm' in page.locator('.prep-content').inner_text()
            page.locator('.learning-plan summary').click()
            assert 'Modul 7' in page.locator('.learning-plan').inner_text()
            for lid in IDS:
                directory = root/'courses/tkinter-api/lessons'/lid
                title = json.loads((directory/'lesson.json').read_text('utf-8'))['title']
                page.goto(f'{base}#/kurz/tkinter-api/{lid}')
                page.wait_for_function('(title) => document.querySelector(".lesson h1")?.textContent === title', arg=title)
                page.wait_for_selector('.editor textarea')
                assert 'otevře okno' in page.locator('.lesson .meta').inner_text()
                assert page.locator('.quiz fieldset').count() == 3
                assert page.locator('.solution-help').count() == 0
                page.click('[data-act="check"]')
                page.wait_for_selector('.results .res.bad')
                assert not page.is_checked('.done-toggle input')
                source = (directory/'solution.py').read_text('utf-8')
                page.locator('.editor textarea').fill(source)
                page.click('[data-act="check"]')
                page.wait_for_function("document.querySelectorAll('.results .res.ok').length > 0 && document.querySelectorAll('.results .res.bad').length === 0")
                assert page.is_checked('.done-toggle input')
                saved = page.request.post(base+'api/workspace/save', headers={'X-Dilna-Token':server.token},
                                          data={'course':'tkinter-api', 'lesson':lid, 'code':source})
                assert saved.ok, saved.text()
                assert (root/'workspace/tkinter-api'/lid/'reseni.py').read_text('utf-8') == source
                page.reload()
                page.wait_for_selector('.editor textarea')
                assert page.locator('.editor textarea').input_value() == source
                assert page.is_checked('.done-toggle input')
            page.goto(f'{base}#/kurz/tkinter-api')
            page.wait_for_selector('.mod li')
            assert page.locator('.mod li.done').count() == 4
            page.set_viewport_size({'width':380, 'height':800})
            page.locator('.learning-plan summary').click()
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            page.goto(f'{base}#/')
            card = page.locator('a.card[href="#/kurz/tkinter-api"]')
            card.wait_for()
            assert '4 / 28 lekcí' in card.inner_text()
            page.goto(f'{base}#/kurz/oop/20-konzolove-expedicni-centrum')
            page.wait_for_selector('.editor textarea')
            assert page.locator('.editor textarea').input_value() == previous
            assert page.is_checked('.done-toggle input')
            assert not errors, errors
            browser.close()
        print('OK: Tkinter 4/28, plán, příprava, GUI štítky, šablony, správná řešení, workspace, reload, mobil a původní OOP postup')
    finally:
        server.runs.stop_all()
        server.shutdown()
        server.server_close()
