"""Tkinter 13–16: plán, příprava, kontroly, pracovní soubor a oddělený postup."""
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

IDS = ['13-api-get-a-json', '14-chyby-http-a-platna-data', '15-vlakno-fronta-a-after', '16-projekt-prevodnik-men']
shots = Path(sys.argv[sys.argv.index('--shots')+1]) if '--shots' in sys.argv else None
if shots:
    shots.mkdir(parents=True, exist_ok=True)
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
            page.goto(f'{base}?t={server.token}#/kurz/tkinter-api/12-projekt-ukolnicek')
            page.wait_for_selector('.editor textarea')
            previous = '# Můj dřívější rozepsaný úkolníček\n'
            page.locator('.editor textarea').fill(previous)
            page.locator('.done-toggle input').check()
            page.goto(f'{base}#/')
            card = page.locator('a.card[href="#/kurz/tkinter-api"]')
            card.wait_for()
            assert 'Rozpracováno' in card.inner_text() and '1 / 28 lekcí' in card.inner_text()
            card.click()
            page.wait_for_selector('.mod li')
            available=sum(len(m['lessons']) for m in json.loads((root/'courses/tkinter-api/course.json').read_text('utf-8'))['modules'])
            assert page.locator('.mod li').count() == available
            assert f'{available} z 28 lekcí připraveno' in page.locator('.learning-plan').inner_text()
            assert page.locator('.course-preparation').count() == 1
            assert 'standardní Tkinter a ttk' in page.locator('.prep-content').inner_text()
            page.locator('.learning-plan summary').click()
            assert 'Modul 7' in page.locator('.learning-plan').inner_text()
            for lid in IDS:
                directory = root/'courses/tkinter-api/lessons'/lid
                title = json.loads((directory/'lesson.json').read_text('utf-8'))['title']
                page.goto(f'{base}#/kurz/tkinter-api/{lid}')
                page.wait_for_function('(title) => document.querySelector(".lesson h1")?.textContent === title', arg=title)
                page.wait_for_selector('.editor textarea')
                kind=json.loads((directory/'lesson.json').read_text('utf-8'))['kind']
                if kind=='gui':
                    assert 'otevře okno' in page.locator('.lesson .meta').inner_text()
                else:
                    page.click('[data-act="run-ex"]')
                    page.wait_for_function("document.querySelector('.ex-console .status').textContent === 'Hotovo.'")
                    output=page.locator('.ex-console pre.out').inner_text()
                    assert 'EUR' in output
                    if lid.startswith('14-'):
                        assert 'Přenos se nepodařil.' in output and 'Odpověď nemá platná data.' in output
                    else:
                        assert 'USD' in output
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
                work=root/'workspace/tkinter-api'/lid
                assert (work/'reseni.py').read_text('utf-8') == source
                for helper in (directory/'files').iterdir():
                    if helper.is_file():
                        assert (work/helper.name).read_bytes()==helper.read_bytes()
                page.reload()
                page.wait_for_selector('.editor textarea')
                assert page.locator('.editor textarea').input_value() == source
                assert page.is_checked('.done-toggle input')
            if shots:
                page.screenshot(path=str(shots/'api-desktop.png'),full_page=True)
            page.set_viewport_size({"width":380, "height":800})
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            if shots:
                page.screenshot(path=str(shots/'api-mobile.png'),full_page=True)
            page.goto(f'{base}#/kurz/tkinter-api')
            page.wait_for_selector('.mod li')
            assert page.locator('.mod li.done').count() == 5
            page.set_viewport_size({'width':380, 'height':800})
            page.locator('.learning-plan summary').click()
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            page.goto(f'{base}#/')
            card = page.locator('a.card[href="#/kurz/tkinter-api"]')
            card.wait_for()
            assert '5 / 28 lekcí' in card.inner_text()
            page.goto(f'{base}#/kurz/tkinter-api/12-projekt-ukolnicek')
            page.wait_for_selector('.editor textarea')
            assert page.locator('.editor textarea').input_value() == previous
            assert page.is_checked('.done-toggle input')
            assert not errors, errors
            browser.close()
        print('OK: Tkinter 13–16, plán, příprava, GUI štítky, šablony, správná řešení, workspace, reload, mobil a původní Tkinter postup')
    finally:
        server.runs.stop_all()
        server.shutdown()
        server.server_close()
