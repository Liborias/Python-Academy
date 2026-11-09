"""Pygame 2: všechny varianty, skutečné PNG, řešení, workspace a zachování práce."""
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import threading
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.app import create_server
IDS = ['01-sprite-obraz-a-poloha', '02-pohyb-vektor-a-cas', '03-skupiny-update-a-draw', '04-kolize-a-pravidla-zasahu', '05-stav-hry-pauza-a-restart']
shots = Path(sys.argv[sys.argv.index('--shots') + 1]) if '--shots' in sys.argv else None
if shots:shots.mkdir(parents=True, exist_ok=True)

with tempfile.TemporaryDirectory() as temp:
    root = Path(temp)
    for name in ['courses', 'web', 'lib']:shutil.copytree(ROOT / name, root / name)
    server = create_server(root, '127.0.0.1', 0, python=os.environ.get('DILNA_TEST_PYTHON'))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_address[1]}/'
    errors = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=shutil.which('chromium'), args=['--no-sandbox'])
            page = browser.new_page(viewport={'width': 1100, 'height': 900})
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.set_default_timeout(30000)
            previous = '# Moje předchozí analytická práce\n'
            page.goto(f'{base}?t={server.token}#/kurz/pandas/42-projekt-predani-a-spusteni')
            page.wait_for_selector('.editor textarea')
            page.locator('.editor textarea').fill(previous)
            page.locator('.done-toggle input').check()
            for lid in IDS:
                directory = root / 'courses/pygame-2/lessons' / lid
                title = json.loads((directory / 'lesson.json').read_text())['title']
                page.goto(f'{base}#/kurz/pygame-2/{lid}')
                page.wait_for_function('(title) => document.querySelector(".lesson h1")?.textContent === title', arg=title)
                assert page.locator('[data-example]').count() == 3
                assert page.locator('[data-task]').count() == 5
                assert page.locator('.quiz fieldset').count() == 3
                editor = page.locator('.editor textarea')
                for example in range(3):
                    page.click(f'[data-example="{example}"]')
                    page.click('[data-act="run-ex"]')
                    page.wait_for_function('document.querySelector(".ex-console .status").textContent === "Hotovo."')
                    assert 'Traceback' not in page.locator('.ex-console pre.out').inner_text()
                    page.wait_for_function('document.querySelector(".ex-console .plot-gallery img")?.naturalWidth === 640')
                for task in range(5):
                    target = directory if task == 0 else directory / 'tasks' / f'task-{task+1}'
                    page.click(f'[data-task="{task}"]')
                    source = (target / 'solution.py').read_text('utf-8')
                    starter = (target / 'exercise.py').read_text('utf-8')
                    editor.fill(starter)
                    before = page.evaluate('JSON.stringify(localStorage)')
                    page.locator('.solution-help summary').click()
                    page.wait_for_function('document.querySelector(".solution-help code")?.textContent.length > 0')
                    assert page.locator('.solution-help code').inner_text().rstrip() == source.rstrip()
                    assert editor.input_value() == starter and page.evaluate('JSON.stringify(localStorage)') == before
                    page.click('[data-act="check"]'); page.wait_for_selector('.results .res.bad')
                    editor.fill(source); page.click('[data-act="check"]')
                    page.wait_for_function('document.querySelectorAll(".results .res.ok").length > 0 && document.querySelectorAll(".results .res.bad").length === 0')
                    assert page.is_checked('.done-toggle input')
                    page.click('[data-act="run"]')
                    page.wait_for_function('document.querySelector(".run-console .status").textContent === "Hotovo."')
                    assert 'Traceback' not in page.locator('.run-console pre.out').inner_text()
                    page.wait_for_function('document.querySelector(".run-console .plot-gallery img")?.naturalWidth === 640')
                    context = {'course': 'pygame-2', 'lesson': lid, 'code': source, **({'task': f'task-{task+1}'} if task else {})}
                    saved = page.request.post(base + 'api/workspace/save', headers={'X-Dilna-Token': server.token}, data=context)
                    assert saved.ok, saved.text()
                    work = root / 'workspace/pygame-2' / lid
                    if task:work = work / 'tasks' / f'task-{task+1}'
                    assert (work / 'reseni.py').read_text('utf-8') == source
                    for helper in (target / 'files').glob('*.py'):assert (work / helper.name).read_bytes() == helper.read_bytes()
                    assert page.locator('.editor .ed-lines').inner_text().splitlines()[-1] == str(source.count('\n') + 1)
                page.reload(); page.wait_for_selector('.editor textarea')
                assert editor.input_value() == (directory / 'solution.py').read_text('utf-8')
                assert page.is_checked('.done-toggle input')
                page.click('[data-task="4"]')
                assert editor.input_value() == (directory / 'tasks/task-5/solution.py').read_text('utf-8')
                for width in [380, 320]:
                    page.set_viewport_size({'width': width, 'height': 800})
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), page.url
                page.locator('.solution-help summary').click()
                page.wait_for_function('document.querySelector(".solution-help code")?.textContent.length > 0')
                if shots and lid == IDS[-1]:
                    page.set_viewport_size({'width': 380, 'height': 800})
                    page.locator('.solution-help').screenshot(path=str(shots / 'pygame2-solution-mobile.png'))
                page.set_viewport_size({'width': 1100, 'height': 900})
            page.goto(f'{base}#/kurz/pygame-2'); page.wait_for_selector('.mod li')
            assert page.locator('.mod li').count() == 5 and page.locator('.mod li.done').count() == 5
            page.wait_for_function('document.querySelector(".prep-content")?.textContent.includes("Prvních 5 z 30")')
            page.locator('.learning-plan summary').click()
            plan = page.locator('.learning-plan').inner_text()
            assert '15 ukázek a 25 úkolů' in plan and 'Meteority' in plan
            if shots:page.screenshot(path=str(shots / 'pygame2-course-desktop.png'), full_page=True)
            page.goto(f'{base}#/kurz/pygame-2/{IDS[0]}'); page.wait_for_selector('.editor textarea')
            page.click('[data-act="run-ex"]')
            page.wait_for_function('document.querySelector(".ex-console .plot-gallery img")?.naturalWidth === 640')
            with page.expect_download() as download:page.locator('.ex-console .plot-gallery a').click()
            path = Path(temp) / 'stazeny.png'; download.value.save_as(path)
            assert path.read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
            if shots:
                page.set_viewport_size({'width': 380, 'height': 800})
                page.locator('.ex-console .plot-gallery').evaluate('el => el.scrollIntoView({block:"center"})')
                page.screenshot(path=str(shots / 'pygame2-preview-mobile.png'))
            page.goto(f'{base}#/kurz/pandas/42-projekt-predani-a-spusteni'); page.wait_for_selector('.editor textarea')
            assert page.locator('.editor textarea').input_value() == previous and page.is_checked('.done-toggle input')
            assert not errors, errors
            browser.close()
        print('OK: Pygame 2 1–5, 15 ukázek/25 úkolů a řešení, skutečné PNG a stažení, workspace, číslování, reload/drafty/postup, plán/příprava a mobil')
    finally:
        server.runs.stop_all(); server.shutdown(); server.server_close()
