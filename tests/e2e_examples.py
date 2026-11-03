"""Přepínání příkladů, vlastní úpravy, reload, stdin a izolace úkolu v prohlížeči."""
import sys
import shutil
import os
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.app import create_server

srv = create_server(ROOT, '127.0.0.1', 0, python=os.environ.get('DILNA_TEST_PYTHON'))
threading.Thread(target=srv.serve_forever, daemon=True).start()
base = f'http://127.0.0.1:{srv.server_address[1]}/'
errors = []
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=shutil.which('chromium') or None, args=['--no-sandbox'])
        page = browser.new_page(viewport={'width': 1100, 'height': 900})
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto(f'{base}?t={srv.token}#/kurz/zaklady/01-prvni-program')
        page.wait_for_selector('[data-example="2"]')
        task = page.locator('.editor textarea')
        task.fill('# Vlastní rozepsaný úkol\n')
        example = page.locator('.ex-editor textarea')
        original = example.input_value()
        page.get_by_role('button', name='Vizitka', exact=True).click()
        assert 'Jméno: Ema' in example.input_value()
        assert page.get_by_role('button', name='Vizitka', exact=True).get_attribute('aria-pressed') == 'true'
        example.fill('print("Moje upravená vizitka")\n')
        page.get_by_role('button', name='Účtenka', exact=True).click()
        assert '25 + 12' in example.input_value()
        page.get_by_role('button', name='Vizitka', exact=True).click()
        assert 'Moje upravená vizitka' in example.input_value()
        page.click('[data-act="run-ex"]')
        page.wait_for_function("document.querySelector('.ex-console .status').textContent === 'Hotovo.'")
        assert 'Moje upravená vizitka' in page.locator('.ex-console pre.out').inner_text()
        assert task.input_value() == '# Vlastní rozepsaný úkol\n'
        page.get_by_role('button', name='Původní ukázka', exact=True).click()
        assert example.input_value() == original
        page.reload()
        page.wait_for_selector('[data-example="2"]')
        page.get_by_role('button', name='Vizitka', exact=True).click()
        assert 'Moje upravená vizitka' in example.input_value()
        assert task.input_value() == '# Vlastní rozepsaný úkol\n'
        # Na mobilu jsou všechna tlačítka dostupná bez vodorovného posunu.
        page.set_viewport_size({'width': 380, 'height': 800})
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        page.goto(f'{base}#/kurz/zaklady/03-vstup-od-uzivatele')
        page.wait_for_selector('[data-example="2"]')
        page.get_by_role('button', name='Cena svačiny', exact=True).click()
        page.click('[data-act="run-ex"]')
        page.wait_for_function("document.querySelector('.ex-console pre.out').textContent.includes('Cena jednoho')")
        field = page.locator('.ex-console .stdin input')
        field.fill('15'); page.locator('.ex-console .stdin button').click()
        page.wait_for_function("document.querySelector('.ex-console pre.out').textContent.includes('Počet kusů')")
        field.fill('3'); page.locator('.ex-console .stdin button').click()
        page.wait_for_function("document.querySelector('.ex-console .status').textContent === 'Hotovo.'")
        assert '45 Kč' in page.locator('.ex-console pre.out').inner_text()
        # Přepnutí běžící ukázku zastaví.
        page.get_by_role('button', name='Pozdrav', exact=True).click()
        page.click('[data-act="run-ex"]')
        page.wait_for_function("document.querySelector('.ex-console pre.out').textContent.includes('Jméno:')")
        page.get_by_role('button', name='Cena svačiny', exact=True).click()
        page.wait_for_function("document.querySelector('.ex-console .status').textContent === 'Zastaveno.'")
        page.goto(f'{base}#/kurz/zaklady/32-projekt-hadej-planetu')
        page.wait_for_selector('.ex-editor textarea')
        assert page.locator('[data-example]').count() == 0
        assert page.locator('.ex-editor textarea').evaluate('(el) => el.readOnly')
        page.goto(f'{base}#/kurz/zaklady/01-prvni-program')
        page.wait_for_selector('[data-example="2"]')
        page.get_by_role('button', name='Vizitka', exact=True).click()
        page.once('dialog', lambda dialog: dialog.accept())
        page.click('[data-act="reset-ex"]')
        assert 'Jméno: Ema' in example.input_value()
        assert task.input_value() == '# Vlastní rozepsaný úkol\n'
        assert not errors, errors
        browser.close()
    print('OK: přepínání, úpravy, obnovení, běh, vstup, zastavení, mobil a původní projekty')
finally:
    srv.runs.stop_all()
    srv.shutdown()
    srv.server_close()
