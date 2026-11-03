"""Úvodní koncept, příprava všech kurzů a volby editoru/systému v prohlížeči."""
import json
import shutil
import sys
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.app import create_server

server = create_server(ROOT, '127.0.0.1', 0)
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f'http://127.0.0.1:{server.server_address[1]}/'
errors = []
try:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=shutil.which('chromium') or None, args=['--no-sandbox'])
        page = browser.new_page(viewport={'width': 1100, 'height': 900})
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto(f'{base}?t={server.token}')
        page.wait_for_selector('.card')
        assert page.locator('.card').count() == 10
        assert page.locator('.card').first.get_attribute('href') == '#/kurz/priprava'
        assert 'Koncept' in page.locator('.card').first.inner_text()
        catalog = json.loads((ROOT / 'courses/catalog.json').read_text())['courses']
        for course in catalog:
            page.goto(f'{base}#/kurz/{course["id"]}')
            page.wait_for_selector('[data-prep="editor"]')
            assert page.locator('.course-preparation').count() == 1
            assert page.locator('.prep-instructions').inner_text()
            assert page.locator('[data-prep-check]').count() == 1
            # Příprava je před lekcemi i u plánovaných podkurzů.
            assert page.evaluate("!!document.querySelector('.course-preparation') && (!document.querySelector('.mod') || !!(document.querySelector('.course-preparation').compareDocumentPosition(document.querySelector('.mod')) & Node.DOCUMENT_POSITION_FOLLOWING))")
        page.goto(f'{base}#/kurz/pygame-1')
        page.wait_for_selector('[data-prep="editor"]')
        assert 'pygame-ce' in page.locator('.prep-content').inner_text()
        for system in ['windows', 'macos', 'linux']:
            page.select_option('[data-prep="os"]', system)
            for editor in ['vscode', 'vscodium', 'pycharm']:
                page.select_option('[data-prep="editor"]', editor)
                instructions = page.locator('.prep-instructions').inner_text()
                assert ('py -3.14' if system == 'windows' else 'python3') in instructions
                assert ('Scripts\\python.exe' if system == 'windows' else '.venv/bin/python') in instructions
                assert {'vscode': 'VS Code', 'vscodium': 'VSCodium', 'pycharm': 'PyCharm'}[editor] in instructions
        page.check('[data-prep-check]')
        page.reload()
        page.wait_for_selector('[data-prep="editor"]')
        assert page.locator('[data-prep="os"]').input_value() == 'linux'
        assert page.locator('[data-prep="editor"]').input_value() == 'pycharm'
        assert page.is_checked('[data-prep-check]')
        page.goto(f'{base}#/kurz/zaklady')
        page.wait_for_selector('[data-prep="editor"]')
        assert not page.is_checked('[data-prep-check]'), 'potvrzení je oddělené pro podkurzy'
        page.goto(f'{base}#/kurz/priprava/05-virtualni-prostredi')
        page.wait_for_selector('.prose input[data-chk]')
        assert page.locator('.editor textarea').count() == 0
        assert 'Návrh lekce' in page.locator('.lesson > .note').inner_text()
        page.locator('.prose input[data-chk]').first.check()
        assert not page.is_checked('.done-toggle input'), 'vlastní checklist neoznačuje automaticky splnění'
        page.reload()
        page.wait_for_selector('.prose input[data-chk]')
        assert page.locator('.prose input[data-chk]').first.is_checked()
        for doc, title in [('vscode', 'VS Code'), ('pycharm', 'PyCharm'), ('vscodium', 'VSCodium')]:
            page.goto(f'{base}#/priprava/{doc}')
            page.wait_for_function('(title) => document.querySelector("#setup-doc")?.textContent.includes(title)', arg=title)
            assert page.locator('#prep-course').count() == 1
        page.select_option('#prep-course', 'databaze')
        page.wait_for_function('document.querySelector("#course-preparation").textContent.includes("SQLite")')
        assert '--extras' in page.locator('#course-preparation').inner_text() or page.locator('#course-preparation details').count() == 1
        page.set_viewport_size({'width': 380, 'height': 800})
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'mobil bez vodorovného posunu'
        assert not errors, errors
        browser.close()
    print('OK: úvodní koncept, všech 10 profilů, 3 systémy × 3 editory, uložení voleb a checklistů, dokumenty a mobil')
finally:
    server.runs.stop_all()
    server.shutdown()
    server.server_close()
