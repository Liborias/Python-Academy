"""Lazy odkrývání řešení: vybraný úkol, zpoždění, opakování, drafty a mobil."""
import json
import shutil
import sys
import tempfile
import threading
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.app import create_server

shots = Path(sys.argv[sys.argv.index('--shots')+1]) if '--shots' in sys.argv else None
if shots:
    shots.mkdir(parents=True, exist_ok=True)

with tempfile.TemporaryDirectory() as temp:
    root = Path(temp)
    for name in ['courses', 'web', 'lib']:
        shutil.copytree(ROOT/name, root/name)
    server = create_server(root, '127.0.0.1', 0)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_address[1]}/'
    errors, requests = [], []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=shutil.which('chromium') or None, args=['--no-sandbox'])
            page = browser.new_page(viewport={'width':1100, 'height':900})
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.on('request', lambda request: requests.append(request.url) if '/api/solution?' in request.url else None)
            lid = '01-prvni-program'
            directory = root/'courses/zaklady/lessons'/lid
            def source(task=1):
                d = directory if task == 1 else directory/'tasks'/f'task-{task}'
                return (d/'solution.py').read_text('utf-8').rstrip()
            def shown(expected):
                page.wait_for_selector('.solution-help pre:not([hidden])')
                assert page.locator('.solution-help code').inner_text().rstrip() == expected
            def open_solution():
                page.locator('.solution-help summary').click()
            def storage():
                return page.evaluate('JSON.stringify(localStorage)')
            page.goto(f'{base}?t={server.token}#/kurz/zaklady/{lid}')
            page.wait_for_selector('.solution-help summary')
            assert not requests
            assert not page.locator('.solution-help').evaluate('(el) => el.open')
            assert page.locator('.solution-help code').text_content() == ''
            editor = page.locator('.editor textarea')
            example = page.locator('.ex-editor textarea')
            editor.fill('# Vlastní rozepsaný úkol 1\n')
            example.fill('# Vlastní rozepsaná ukázka\n')
            before = storage()
            summary = page.locator('.solution-help summary')
            summary.focus(); summary.press('Enter')
            shown(source())
            assert len(requests) == 1 and 'task=task-1' in requests[0]
            assert 'jiný kód může správně splnit zadání' in page.locator('.solution-help').inner_text()
            assert page.locator('.solution-help textarea').count() == 0
            assert not page.is_checked('.done-toggle input') and storage() == before
            assert editor.input_value() == '# Vlastní rozepsaný úkol 1\n'
            assert example.input_value() == '# Vlastní rozepsaná ukázka\n'
            summary.press('Enter'); summary.press('Enter')
            shown(source())
            assert len(requests) == 1
            page.click('[data-task="1"]')
            assert not page.locator('.solution-help').evaluate('(el) => el.open')
            assert page.locator('.solution-help code').text_content() == ''
            editor.fill('# Vlastní rozepsaný úkol 2\n')
            open_solution(); shown(source(2))
            assert 'Úkol 2' in page.locator('.solution-context').inner_text()
            assert editor.input_value() == '# Vlastní rozepsaný úkol 2\n'
            editor.fill(source(2))
            page.click('[data-act="check"]')
            page.wait_for_selector('.results .res.ok')
            assert page.locator('.solution-help').evaluate('(el) => el.open'), 'kontrola stejného úkolu panel nezavírá'
            assert '✓' in page.locator('[data-task="1"]').inner_text()
            assert not page.is_checked('.done-toggle input')
            # Pozdní odpověď task-3 nesmí zaměnit již zobrazený task-4.
            pending = []
            def delay(route):
                if parse_qs(urlsplit(route.request.url).query).get('task') == ['task-3']:
                    pending.append(route)
                else:
                    route.continue_()
            page.route('**/api/solution?*', delay)
            page.click('[data-task="2"]'); open_solution()
            page.wait_for_function("document.querySelector('.solution-status').textContent.includes('Načítám')")
            assert len(pending) == 1
            page.click('[data-task="3"]'); open_solution(); shown(source(4))
            pending[0].fulfill(status=200, content_type='application/json', body=json.dumps({'code': source(3)}))
            page.wait_for_timeout(100)
            shown(source(4))
            assert 'Úkol 4' in page.locator('.solution-context').inner_text()
            page.unroute('**/api/solution?*', delay)
            # Po chybě lze opakováním otevření načíst správné řešení.
            page.route('**/api/solution?*', lambda route: route.fulfill(status=503, content_type='application/json', body='{}'), times=1)
            page.click('[data-task="4"]'); open_solution()
            page.wait_for_function("document.querySelector('.solution-status').textContent.includes('nepodařilo')")
            open_solution(); open_solution(); shown(source(5))
            page.click('[data-task="0"]')
            assert editor.input_value() == '# Vlastní rozepsaný úkol 1\n'
            page.reload(); page.wait_for_selector('.solution-help summary')
            assert not page.locator('.solution-help').evaluate('(el) => el.open')
            assert editor.input_value() == '# Vlastní rozepsaný úkol 1\n'
            assert example.input_value() == '# Vlastní rozepsaná ukázka\n'
            page.click('[data-task="1"]')
            assert editor.input_value().rstrip() == source(2)
            assert '✓' in page.locator('[data-task="1"]').inner_text()
            # Zobrazený kód je text i při HTML uvnitř Python řetězce.
            payload = 'print("<img src=x onerror=window.nechtene=1>")\nprint("</code><script>window.nechtene=1</script>")\n'
            page.route('**/api/solution?*', lambda route: route.fulfill(status=200, content_type='application/json', body=json.dumps({'code':payload})))
            page.click('[data-task="0"]'); open_solution(); shown(payload.rstrip())
            assert page.locator('.solution-help img, .solution-help script').count() == 0
            assert page.evaluate('window.nechtene === undefined')
            page.unroute('**/api/solution?*')
            # Samostatný projekt a závěrečný program mají také řešení.
            for lesson in ['32-projekt-hadej-planetu', '40-zaverecny-test']:
                page.goto(f'{base}#/kurz/zaklady/{lesson}')
                page.wait_for_selector('.solution-help summary')
                page.locator('.editor textarea').fill('# Dřívější práce\n')
                page.locator('.done-toggle input').check()
                before = storage()
                open_solution()
                shown((root/'courses/zaklady/lessons'/lesson/'solution.py').read_text('utf-8').rstrip())
                assert storage() == before and page.is_checked('.done-toggle input')
                assert page.locator('.editor textarea').input_value() == '# Dřívější práce\n'
                if lesson.startswith('40'):
                    assert page.locator('.quiz fieldset').count() == 10
                    assert page.locator('.quiz input:checked').count() == 0
            # Skutečný delší kód, tmavý režim a mobilní šířka.
            page.goto(f'{base}#/kurz/zaklady/15-funkce-a-seznamy')
            page.wait_for_selector('.solution-help summary'); open_solution()
            shown((root/'courses/zaklady/lessons/15-funkce-a-seznamy/solution.py').read_text('utf-8').rstrip())
            if shots:
                page.locator('.solution-help').screenshot(path=str(shots/'solution-desktop.png'))
            page.set_viewport_size({'width':380,'height':800})
            page.evaluate("document.documentElement.dataset.theme = 'dark'")
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            if shots:
                page.locator('.solution-help').screenshot(path=str(shots/'solution-mobile-dark.png'))
            courses = ['oop','soubory-web','pygame-1','turtle-oop','tkinter-api','pandas','pygame-2','databaze']
            checked = 0
            for cid in courses:
                course = json.loads((root/'courses'/cid/'course.json').read_text('utf-8'))
                lids = [lid for module in course['modules'] for lid in module['lessons']]
                for index, lesson in enumerate(lids):
                    page.goto(f'{base}#/kurz/{cid}/{lesson}')
                    title = json.loads((root/'courses'/cid/'lessons'/lesson/'lesson.json').read_text('utf-8'))['title']
                    page.wait_for_function('(title)=>document.querySelector(".lesson h1")?.textContent===title', arg=title)
                    panel = page.locator('.solution-help')
                    assert panel.count() == 1 and not panel.evaluate('(el) => el.open')
                    assert panel.locator('code').text_content() == ''
                    draft = f'# Moje práce: {cid}/{lesson}\n'
                    page.locator('.editor textarea').fill(draft)
                    page.locator('.done-toggle input').set_checked(index % 2 == 0)
                    before = page.evaluate('JSON.stringify(localStorage)')
                    count = len(requests)
                    open_solution()
                    shown((root/'courses'/cid/'lessons'/lesson/'solution.py').read_text('utf-8').rstrip())
                    assert len(requests) == count + 1
                    assert page.locator('.editor textarea').input_value() == draft
                    assert page.is_checked('.done-toggle input') == (index % 2 == 0)
                    assert page.evaluate('JSON.stringify(localStorage)') == before
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
                    checked += 1
                page.reload()
                page.wait_for_selector('.solution-help summary')
                assert not page.locator('.solution-help').evaluate('(el) => el.open')
                assert page.locator('.editor textarea').input_value() == draft
                assert page.is_checked('.done-toggle input') == (index % 2 == 0)
            assert checked == 230, checked
            # Opožděný vzor předchozího kurzu se nesmí objevit v nové lekci.
            page.goto(f'{base}#/kurz/oop/20-konzolove-expedicni-centrum')
            page.wait_for_selector('.solution-help summary')
            pending = []
            def delayed_course(route):
                query = parse_qs(urlsplit(route.request.url).query)
                if query.get('course') == ['oop']:
                    pending.append(route)
                else:
                    route.continue_()
            page.route('**/api/solution?*', delayed_course)
            open_solution()
            page.wait_for_function("document.querySelector('.solution-status').textContent.includes('Načítám')")
            page.goto(f'{base}#/kurz/tkinter-api/27-cesty-a-klavesove-zkratky')
            page.wait_for_selector('.solution-help summary')
            open_solution()
            shown((root/'courses/tkinter-api/lessons/27-cesty-a-klavesove-zkratky/solution.py').read_text('utf-8').rstrip())
            assert len(pending) == 1
            pending[0].fulfill(status=200, content_type='application/json', body=json.dumps({'code':'# Opožděné OOP'}))
            page.wait_for_timeout(100)
            assert 'Opožděné OOP' not in page.locator('.solution-help code').inner_text()
            page.unroute('**/api/solution?*', delayed_course)
            if shots:
                page.locator('.solution-help').screenshot(path=str(shots/'solution-all-courses-mobile.png'))
            # Příprava má praktické průvodce bez programového úkolu.
            guides = json.loads((root/'courses/priprava/course.json').read_text('utf-8'))
            first_guide = guides['modules'][0]['lessons'][0]
            page.goto(f'{base}#/kurz/priprava/{first_guide}')
            page.wait_for_selector('.lesson h1')
            assert page.locator('.solution-help').count() == 0
            assert not errors, errors
            browser.close()
        print('OK: řešení Úkolů 1–5 a všech 230 lekcí ostatních kurzů, zpoždění v úkolu i mezi kurzy, opakování, text, drafty/postup, klávesnice a mobil')
    finally:
        server.runs.stop_all()
        server.shutdown()
        server.server_close()
