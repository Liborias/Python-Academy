"""První pandas: 15 ukázek, 25 úkolů/vzorů, CSV, pracovní soubory a starší postup."""
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

IDS = ['01-series-a-popisky', '02-vypocty-se-series', '03-vyber-loc-a-iloc',
       '04-prvni-dataframe', '05-csv-a-prvni-pruzkum']
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
            page.set_default_timeout(30000)
            page.on('pageerror', lambda error: errors.append(str(error)))
            previous = '# Můj rozepsaný korespondenční projekt\n'
            page.goto(f'{base}?t={server.token}#/kurz/tkinter-api/24-projekt-korespondencni-dilna')
            page.wait_for_selector('.editor textarea')
            page.locator('.editor textarea').fill(previous)
            page.locator('.done-toggle input').check()
            page.goto(f'{base}#/')
            card = page.locator('a.card[href="#/kurz/pandas"]')
            card.wait_for()
            assert 'Rozpracováno' in card.inner_text() and '0 / 42 lekcí' in card.inner_text()
            card.click()
            page.wait_for_selector('.mod li')
            available = sum(len(m['lessons']) for m in json.loads((root/'courses/pandas/course.json').read_text('utf-8'))['modules'])
            assert page.locator('.mod li').count() == available
            assert f'{available} z 42 lekcí připraveno' in page.locator('.learning-plan').inner_text()
            page.wait_for_function('document.querySelector(".prep-content")?.textContent.includes("pandas řady 3")')
            page.locator('.learning-plan summary').click()
            assert 'Modul 8' in page.locator('.learning-plan').inner_text()
            assert 'VS Code/VSCodium/PyCharm' in page.locator('.learning-plan').inner_text()
            for lid in IDS:
                directory = root/'courses/pandas/lessons'/lid
                title = json.loads((directory/'lesson.json').read_text('utf-8'))['title']
                page.goto(f'{base}#/kurz/pandas/{lid}')
                page.wait_for_function('(title) => document.querySelector(".lesson h1")?.textContent === title', arg=title)
                page.wait_for_selector('[data-task="4"]')
                assert page.locator('[data-example]').count() == 3
                assert page.locator('[data-task]').count() == 5
                assert page.locator('.quiz fieldset').count() == 3
                editor, example = page.locator('.editor textarea'), page.locator('.ex-editor textarea')
                draft = f'# Moje práce v {lid}\n'
                editor.fill(draft)
                for index in range(3):
                    page.click(f'[data-example="{index}"]')
                    assert page.locator(f'[data-example="{index}"]').get_attribute('aria-pressed') == 'true'
                    page.click('[data-act="run-ex"]')
                    page.wait_for_function("document.querySelector('.ex-console .status').textContent === 'Hotovo.'")
                    assert 'Traceback' not in page.locator('.ex-console pre.out').inner_text()
                    assert page.locator('.ex-console pre.out').inner_text().strip()
                    assert editor.input_value() == draft
                original_example = example.input_value()
                example.fill(original_example+'\n# Moje poznámka k ukázce\n')
                # Nejprve procvičení: jeho úspěch nesmí označit původní úkol.
                for task in [2,3,4,5,1]:
                    page.click(f'[data-task="{task-1}"]')
                    d = directory if task == 1 else directory/'tasks'/f'task-{task}'
                    panel = page.locator('.solution-help')
                    assert not panel.evaluate('(el) => el.open')
                    if task == 1:
                        assert editor.input_value() == draft
                    before_code = editor.input_value()
                    before = page.evaluate('JSON.stringify(localStorage)')
                    panel.locator('summary').click()
                    page.wait_for_function('document.querySelector(".solution-help code")?.textContent.length > 0')
                    source = (d/'solution.py').read_text('utf-8')
                    assert panel.locator('code').inner_text().rstrip() == source.rstrip()
                    assert editor.input_value() == before_code
                    assert page.evaluate('JSON.stringify(localStorage)') == before
                    page.click('[data-act="check"]')
                    page.wait_for_selector('.results .res.bad')
                    assert not page.is_checked('.done-toggle input')
                    editor.fill(source)
                    page.click('[data-act="check"]')
                    page.wait_for_function("document.querySelectorAll('.results .res.ok').length > 0 && document.querySelectorAll('.results .res.bad').length === 0")
                    assert '✓' in page.locator(f'[data-task="{task-1}"]').inner_text()
                    assert page.is_checked('.done-toggle input') == (task == 1)
                    if lid == IDS[-1]:
                        # Každý CSV úkol má své soubory i pro běh a editor.
                        page.click('[data-act="run"]')
                        page.wait_for_function("document.querySelector('.run-console .status').textContent === 'Hotovo.'")
                        assert 'Traceback' not in page.locator('.run-console pre.out').inner_text()
                        fields = {'course':'pandas','lesson':lid,'task':f'task-{task}','code':source}
                        saved = page.request.post(base+'api/workspace/save', headers={'X-Dilna-Token':server.token}, data=fields)
                        assert saved.ok, saved.text()
                        target = root/'workspace/pandas'/lid
                        if task > 1:
                            target = target/'tasks'/f'task-{task}'
                        assert (target/'reseni.py').read_text('utf-8') == source
                        for f in (d/'files').iterdir():
                            assert (target/f.name).read_bytes() == f.read_bytes()
                page.reload()
                page.wait_for_selector('[data-task="4"]')
                assert page.is_checked('.done-toggle input')
                assert not page.locator('.solution-help').evaluate('(el) => el.open')
                page.click('[data-example="2"]')
                assert 'Moje poznámka k ukázce' in example.input_value()
                for task in range(1,6):
                    page.click(f'[data-task="{task-1}"]')
                    d = directory if task == 1 else directory/'tasks'/f'task-{task}'
                    assert editor.input_value() == (d/'solution.py').read_text('utf-8')
                    assert '✓' in page.locator(f'[data-task="{task-1}"]').inner_text()
                page.set_viewport_size({'width':380,'height':800})
                page.locator('.solution-help summary').click()
                page.wait_for_function('document.querySelector(".solution-help code")?.textContent.length > 0')
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
                if shots and lid == IDS[-1]:
                    page.locator('.solution-help').screenshot(path=str(shots/'pandas-solution-mobile.png'))
                    page.screenshot(path=str(shots/'pandas-lesson-mobile.png'), full_page=True)
                page.set_viewport_size({'width':1100,'height':900})
            page.goto(f'{base}#/kurz/pandas')
            page.wait_for_selector('.mod li')
            assert page.locator('.mod li.done').count() == 5
            page.locator('.learning-plan summary').click()
            if shots:
                page.screenshot(path=str(shots/'pandas-course-desktop.png'), full_page=True)
            page.goto(f'{base}#/kurz/tkinter-api/24-projekt-korespondencni-dilna')
            page.wait_for_selector('.editor textarea')
            assert page.locator('.editor textarea').input_value() == previous
            assert page.is_checked('.done-toggle input')
            assert not errors, errors
            browser.close()
        print('OK: pandas úvod 1–5, plán/příprava, 15 skutečných ukázek, 25 šablon/řešení, vlastní CSV, workspace, drafty/postup a mobil')
    finally:
        server.runs.stop_all()
        server.shutdown()
        server.server_close()
