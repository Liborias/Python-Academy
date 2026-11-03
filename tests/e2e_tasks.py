"""Pět úkolů: vlastní zadání, řešení, kontroly, soubory a bezpečné přepnutí."""
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

with tempfile.TemporaryDirectory() as temp:
    root = Path(temp)
    for name in ['web','courses','lib']:
        shutil.copytree(ROOT / name, root / name)
    server = create_server(root, '127.0.0.1', 0, python=os.environ.get('DILNA_TEST_PYTHON'))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_address[1]}/'
    errors = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=shutil.which('chromium') or None, args=['--no-sandbox'])
            page = browser.new_page(viewport={'width':1100,'height':900})
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto(f'{base}?t={server.token}#/kurz/zaklady/01-prvni-program')
            page.wait_for_selector('[data-task="4"]')
            assert page.locator('[data-task]').count() == 5
            editor = page.locator('.editor textarea')
            editor.fill('# Původní rozepsané řešení\n')
            page.click('[data-task="1"]')
            assert 'Pozdrav a součet' in page.locator('.task-description').inner_text()
            editor.fill('print("rozepsaný druhý úkol")\n')
            page.click('[data-task="2"]')
            assert 'Dva řádky' in page.locator('.task-description').inner_text()
            page.click('[data-task="1"]')
            assert 'rozepsaný druhý' in editor.input_value()
            solution = (root/'courses/zaklady/lessons/01-prvni-program/tasks/task-2/solution.py').read_text('utf-8')
            editor.fill(solution)
            page.click('[data-act="check"]')
            page.wait_for_selector('.results .res.ok')
            assert '✓' in page.locator('[data-task="1"]').inner_text()
            assert not page.is_checked('.done-toggle input'), 'procvičování nemění splnění původního úkolu'
            page.click('[data-act="run"]')
            page.wait_for_function("document.querySelector('.run-console .status').textContent === 'Hotovo.'")
            assert 'Ahoj, akademie!' in page.locator('.run-console pre.out').inner_text()
            page.click('[data-task="0"]')
            assert editor.input_value() == '# Původní rozepsané řešení\n'
            page.reload(); page.wait_for_selector('[data-task="4"]')
            page.click('[data-task="1"]')
            assert editor.input_value().strip() == solution.strip()
            assert '✓' in page.locator('[data-task="1"]').inner_text()
            page.once('dialog', lambda dialog: dialog.accept())
            page.click('[data-act="reset"]')
            assert editor.input_value().strip() != solution.strip()
            # Pracovní soubor task-3 se načítá pouze do task-3.
            fields = {'course':'zaklady','lesson':'01-prvni-program','task':'task-3','code':'print("Ze souboru task-3")\n'}
            response = page.request.post(base+'api/workspace/save',data=fields,headers={'X-Dilna-Token':server.token})
            assert response.ok
            page.click('[data-task="2"]'); page.click('[data-act="reload"]')
            page.wait_for_function("document.querySelector('.editor textarea').value.includes('Ze souboru task-3')")
            page.click('[data-task="0"]')
            assert editor.input_value() == '# Původní rozepsané řešení\n'
            # Odpověď kontroly po přepnutí se nesmí zobrazit u jiného úkolu.
            pending = []
            page.route('**/api/check', lambda route: pending.append(route))
            page.click('[data-task="2"]'); page.click('[data-act="check"]')
            page.wait_for_timeout(100)
            assert len(pending) == 1
            page.click('[data-task="3"]')
            pending[0].fulfill(status=200,content_type='application/json',body=json.dumps({'ok':True,'results':[]}))
            page.wait_for_timeout(100)
            assert page.locator('.results').inner_text() == ''
            page.unroute('**/api/check')
            # Přepnutí zastaví i čekající běh a další běh už má vlastní výstup.
            page.click('[data-task="1"]')
            editor.fill('input("Čekám: ")\n'); page.click('[data-act="run"]')
            page.wait_for_function("document.querySelector('.run-console pre.out').textContent.includes('Čekám:')")
            page.click('[data-task="4"]')
            editor.fill('print("Pátý úkol")\n'); page.click('[data-act="run"]')
            page.wait_for_function("document.querySelector('.run-console .status').textContent === 'Hotovo.'")
            assert page.locator('.run-console pre.out').inner_text().strip() == 'Pátý úkol'
            page.set_viewport_size({'width':380,'height':800})
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            page.goto(f'{base}#/kurz/zaklady/32-projekt-hadej-planetu')
            page.wait_for_selector('.editor textarea')
            assert page.locator('[data-task]').count() == 0
            assert not errors,errors
            browser.close()
        print('OK: 5 úkolů, vlastní zadání/draft/check/soubory, restart, reset, pozdní kontrola, přepnutí běhu, mobil, původní projekty')
    finally:
        server.runs.stop_all(); server.shutdown(); server.server_close()
