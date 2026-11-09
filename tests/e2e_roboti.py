"""Chyť robota: úkoly/řešení, skutečné SDL běhy, PNG, postup a mobil."""
import json
import os
from pathlib import Path
import random
import shutil
import sys
import tempfile
import threading
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.app import create_server

IDS = ['11-roboti-cil-a-kliknuti','12-roboti-ruzne-pohyby','13-roboti-zasahy-a-body','14-roboti-cas-a-vlny','15-roboti-nabidka-a-restart']
shots = Path(sys.argv[sys.argv.index('--shots') + 1]) if '--shots' in sys.argv else None
if shots:
    shots.mkdir(parents=True, exist_ok=True)
rng = random.Random(11)
for i in range(3):
    point = (rng.randint(114, 606), rng.randint(118, 434))
    if i % 2 == 0:
        rng.choice((-1, 1))

# Vykreslení, fonty i hodiny zůstávají skutečné. Do SDL přidáváme jen události.
SCRIPT = '''import pygame
_dilna_frame = 0
_dilna_get = pygame.event.get
def _dilna_events():
    global _dilna_frame
    if _dilna_frame == 0:
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
    if _dilna_frame == 1:
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=__POINT__))
    if _dilna_frame in (3, 5):
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p))
    if _dilna_frame == 7:
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r))
    if _dilna_frame == 9:
        pygame.event.post(pygame.event.Event(pygame.QUIT))
    _dilna_frame += 1
    return _dilna_get()
pygame.event.get = _dilna_events
'''

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
            browser = p.chromium.launch(executable_path=shutil.which('chromium'), args=['--no-sandbox'])
            page = browser.new_page(viewport={'width': 1100, 'height': 900})
            page.set_default_timeout(30000)
            page.on('pageerror', lambda error: errors.append(str(error)))

            def scripted_run(route):
                body = route.request.post_data_json
                if body.get('course') == 'pygame-2' and body.get('lesson') in IDS:
                    target = point if IDS.index(body['lesson']) >= 3 else (160, 200)
                    body['code'] = SCRIPT.replace('__POINT__', repr(target)) + '\n' + body['code']
                    route.continue_(post_data=json.dumps(body))
                else:
                    route.continue_()

            page.route('**/api/run', scripted_run)
            previous = '# Moje rozepsaná úprava Meteoritu\n'
            old_id = '10-meteority-pauza-a-restart'
            page.goto(f'{base}?t={server.token}#/kurz/pygame-2/{old_id}')
            page.wait_for_selector('.editor textarea')
            page.locator('.editor textarea').fill(previous)
            page.locator('.done-toggle input').check()
            for lid in IDS:
                directory = root/'courses/pygame-2/lessons'/lid
                title = json.loads((directory/'lesson.json').read_text())['title']
                source, starter = [(directory/name).read_text() for name in ['solution.py', 'exercise.py']]
                page.goto(f'{base}#/kurz/pygame-2/{lid}')
                page.wait_for_function('(title)=>document.querySelector(".lesson h1")?.textContent===title', arg=title)
                assert not page.locator('[data-task]').count() and not page.locator('[data-example]').count()
                assert page.locator('.quiz fieldset').count() == 3
                assert page.locator('.ex-editor textarea').evaluate('el=>el.readOnly')
                editor = page.locator('.editor textarea')
                assert editor.input_value().rstrip() == starter.rstrip()
                before = page.evaluate('JSON.stringify(localStorage)')
                page.locator('.solution-help summary').click()
                page.wait_for_function('document.querySelector(".solution-help code")?.textContent.length>0')
                assert page.locator('.solution-help code').inner_text().rstrip() == source.rstrip()
                assert editor.input_value().rstrip() == starter.rstrip() and page.evaluate('JSON.stringify(localStorage)') == before
                page.click('[data-act="check"]')
                page.wait_for_selector('.results .res.bad')
                assert not page.is_checked('.done-toggle input')
                editor.fill(source)
                page.click('[data-act="check"]')
                page.wait_for_function('document.querySelectorAll(".results .res.ok").length>0 && document.querySelectorAll(".results .res.bad").length===0')
                assert page.is_checked('.done-toggle input')
                for action, console in [('run-ex', 'ex-console'), ('run', 'run-console')]:
                    page.click(f'[data-act="{action}"]')
                    page.wait_for_function('(selector)=>document.querySelector(selector+" .status").textContent==="Hotovo."', arg='.'+console)
                    output = page.locator(f'.{console} pre.out').inner_text()
                    assert 'Poslední snímek: roboti.png' in output and 'Traceback' not in output
                    page.wait_for_function('(selector)=>document.querySelector(selector+" .plot-gallery img")?.naturalWidth===720', arg='.'+console)
                    assert page.locator(f'.{console} img').evaluate('el=>el.naturalHeight') == 520
                with page.expect_download() as download:
                    page.locator('.run-console .plot-gallery a').click()
                path = root/'snímek.png'
                download.value.save_as(path)
                assert path.read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
                saved = page.request.post(base+'api/workspace/save', headers={'X-Dilna-Token': server.token}, data={'course':'pygame-2', 'lesson':lid, 'code':source})
                assert saved.ok, saved.text()
                work = root/'workspace/pygame-2'/lid
                assert (work/'reseni.py').read_text() == source
                for helper in (directory/'files').glob('*.py'):
                    assert (work/helper.name).read_bytes() == helper.read_bytes()
                page.reload()
                page.wait_for_selector('.editor textarea')
                assert editor.input_value() == source and page.is_checked('.done-toggle input')
                assert not page.locator('.solution-help').evaluate('el=>el.open')
                for width in [380, 320]:
                    page.set_viewport_size({'width': width, 'height': 800})
                    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'), (page.url, width, page.evaluate('document.documentElement.scrollWidth'))
                page.locator('.solution-help summary').click()
                page.wait_for_function('document.querySelector(".solution-help code")?.textContent.length>0')
                if shots and lid == IDS[-1]:
                    page.set_viewport_size({'width': 380, 'height': 800})
                    page.locator('.solution-help').screenshot(path=str(shots/'roboti-solution-mobile.png'))
                    page.click('[data-act="run"]')
                    page.wait_for_function('document.querySelector(".run-console .plot-gallery img")?.naturalWidth===720')
                    page.locator('.run-console .plot-gallery').evaluate('el=>el.scrollIntoView({block:"center"})')
                    page.screenshot(path=str(shots/'roboti-preview-mobile.png'))
                page.set_viewport_size({'width': 1100, 'height': 900})
            page.unroute('**/api/run', scripted_run)
            page.click('[data-act="run"]')
            page.wait_for_function('document.querySelector(".run-console .status").textContent==="Běží…"')
            assert page.locator('.run-console .plot-gallery').is_hidden()
            page.click('[data-act="stop"]')
            page.wait_for_function('document.querySelector(".run-console .status").textContent==="Zastaveno."')
            page.goto(f'{base}#/kurz/pygame-2')
            page.wait_for_selector('.mod li')
            assert page.locator('.mod li').count() == 20 and page.locator('.mod li.done').count() == 6
            page.wait_for_function('document.querySelector(".prep-content")?.textContent.includes("Prvních 20 z 30")')
            page.locator('.learning-plan summary').click()
            text = page.locator('.learning-plan').inner_text()
            assert 'Hotovo: lekce 11–15.' in text and '40 ukázek a 60 úkolů' in text
            if shots:
                page.screenshot(path=str(shots/'roboti-course-desktop.png'), full_page=True)
            page.goto(f'{base}#/kurz/pygame-2/{old_id}')
            page.wait_for_selector('.editor textarea')
            assert page.locator('.editor textarea').input_value() == previous and page.is_checked('.done-toggle input')
            assert not errors, errors
            browser.close()
        print('OK: Roboti 11–15, šablony/řešení, 10 skutečných SDL běhů/PNG/stažení, živý běh/Stop, workspace, readonly, postup, plán/příprava a mobil')
    finally:
        server.runs.stop_all()
        server.shutdown()
        server.server_close()
