"""Závěr Pygame 2: 21 úkolů/řešení, 13 ukázek, skutečný běh a mobil."""
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import threading
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from server.app import create_server
IDS=['26-rizene-herni-scenare','27-vlastni-testy-hry','28-vysledky-v-json','29-priprava-a-baleni-hry','30-kuryrska-smena-a-predani']
shots=Path(sys.argv[sys.argv.index('--shots')+1]) if '--shots' in sys.argv else None
if shots:shots.mkdir(parents=True,exist_ok=True)
SCRIPT="""import pygame
_dilna_frame = 0
_dilna_get = pygame.event.get
def _dilna_events():
    global _dilna_frame
    if _dilna_frame == 0:
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
    if _dilna_frame in (3, 5):
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p))
    if _dilna_frame == 7:
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r))
    if _dilna_frame == 70:
        pygame.event.post(pygame.event.Event(pygame.QUIT))
    _dilna_frame += 1
    return _dilna_get()
pygame.event.get = _dilna_events
"""
with tempfile.TemporaryDirectory() as temp:
    root=Path(temp)
    for name in ['courses','web','lib']:shutil.copytree(ROOT/name,root/name)
    server=create_server(root,'127.0.0.1',0,python=os.environ.get('DILNA_TEST_PYTHON'))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{server.server_address[1]}/'
    errors=[]
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
            page=browser.new_page(viewport={'width':1100,'height':900})
            page.set_default_timeout(30000)
            page.on('pageerror',lambda e:errors.append(str(e)))
            def scripted_run(route):
                body=route.request.post_data_json
                if body.get('course')=='pygame-2' and body.get('lesson')==IDS[-1]:
                    body['code']=SCRIPT+'\n'+body['code']
                    route.continue_(post_data=json.dumps(body))
                else:route.continue_()
            page.route('**/api/run',scripted_run)
            old='25-droni-hra-pauza-a-vysledek'
            previous='# Moje rozepsaná mise s drony\n'
            page.goto(f'{base}?t={server.token}#/kurz/pygame-2/{old}')
            page.wait_for_selector('.editor textarea')
            page.locator('.editor textarea').fill(previous)
            page.locator('.done-toggle input').check()
            examples=tasks=0
            for stage,lid in enumerate(IDS):
                d=root/'courses/pygame-2/lessons'/lid
                title=json.loads((d/'lesson.json').read_text())['title']
                page.goto(f'{base}#/kurz/pygame-2/{lid}')
                page.wait_for_function('(t)=>document.querySelector(".lesson h1")?.textContent===t',arg=title)
                assert page.locator('.quiz fieldset').count()==3
                assert page.locator('.ex-editor textarea').evaluate('el=>el.readOnly') == (stage==4)
                assert page.locator('[data-example]').count()==(0 if stage==4 else 3)
                assert page.locator('[data-task]').count()==(0 if stage==4 else 5)
                editor=page.locator('.editor textarea')
                for example in range(1 if stage==4 else 3):
                    if stage!=4:page.click(f'[data-example="{example}"]')
                    page.click('[data-act="run-ex"]')
                    page.wait_for_function('document.querySelector(".ex-console .status").textContent==="Hotovo."')
                    output=page.locator('.ex-console pre.out').inner_text()
                    assert 'Traceback' not in output
                    if stage==1:assert 'Ran 3 tests' in output and 'OK' in output
                    if stage==4:page.wait_for_function('document.querySelector(".ex-console .plot-gallery img")?.naturalWidth===720')
                    examples+=1
                for task in range(1 if stage==4 else 5):
                    target=d if task==0 else d/'tasks'/f'task-{task+1}'
                    if stage!=4:page.click(f'[data-task="{task}"]')
                    source=(target/'solution.py').read_text()
                    starter=(target/'exercise.py').read_text()
                    editor.fill(starter)
                    before=page.evaluate('JSON.stringify(localStorage)')
                    page.locator('.solution-help summary').click()
                    page.wait_for_function('document.querySelector(".solution-help code")?.textContent.length>0')
                    assert page.locator('.solution-help code').inner_text().rstrip()==source.rstrip()
                    assert editor.input_value()==starter and page.evaluate('JSON.stringify(localStorage)')==before
                    page.click('[data-act="check"]')
                    page.wait_for_selector('.results .res.bad')
                    editor.fill(source)
                    page.click('[data-act="check"]')
                    page.wait_for_function('document.querySelectorAll(".results .res.ok").length>0 && !document.querySelectorAll(".results .res.bad").length')
                    assert page.is_checked('.done-toggle input')
                    page.click('[data-act="run"]')
                    page.wait_for_function('document.querySelector(".run-console .status").textContent==="Hotovo."')
                    output=page.locator('.run-console pre.out').inner_text()
                    assert 'Traceback' not in output
                    if stage==1:assert 'Ran ' in output and 'OK' in output
                    if stage==4:page.wait_for_function('document.querySelector(".run-console .plot-gallery img")?.naturalWidth===720')
                    context={'course':'pygame-2','lesson':lid,'code':source,**({'task':f'task-{task+1}'} if task else {})}
                    saved=page.request.post(base+'api/workspace/save',headers={'X-Dilna-Token':server.token},data=context)
                    assert saved.ok,saved.text()
                    work=root/'workspace/pygame-2'/lid
                    if task:work=work/'tasks'/f'task-{task+1}'
                    assert (work/'reseni.py').read_text()==source
                    for helper in (target/'files').rglob('*'):
                        if helper.is_file():assert (work/helper.relative_to(target/'files')).read_bytes()==helper.read_bytes()
                    assert page.locator('.editor .ed-lines').inner_text().splitlines()[-1]==str(source.count('\n')+1)
                    for width in [380,320]:
                        page.set_viewport_size({'width':width,'height':800})
                        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(lid,task,width)
                    page.set_viewport_size({'width':1100,'height':900})
                    tasks+=1
                page.reload()
                page.wait_for_selector('.editor textarea')
                assert editor.input_value()==(d/'solution.py').read_text()
                assert page.is_checked('.done-toggle input')
                if stage!=4:
                    page.click('[data-task="4"]')
                    assert editor.input_value()==(d/'tasks/task-5/solution.py').read_text()
                page.locator('.solution-help summary').click()
                page.wait_for_function('document.querySelector(".solution-help code")?.textContent.length>0')
                if shots and stage in (2,4):
                    page.set_viewport_size({'width':380,'height':800})
                    page.locator('.solution-help').screenshot(path=str(shots/f'predani-{stage}-solution-mobile.png'))
                page.set_viewport_size({'width':1100,'height':900})
            assert (examples,tasks)==(13,21),(examples,tasks)
            page.click('[data-act="run"]')
            page.wait_for_function('document.querySelector(".run-console .plot-gallery img")?.naturalWidth===720')
            with page.expect_download() as download:page.locator('.run-console .plot-gallery a').click()
            path=root/'snimek.png';download.value.save_as(path)
            assert path.read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
            if shots:
                page.set_viewport_size({'width':380,'height':800})
                page.locator('.run-console .plot-gallery').evaluate('el=>el.scrollIntoView({block:"center"})')
                page.screenshot(path=str(shots/'predani-preview-mobile.png'))
                page.set_viewport_size({'width':1100,'height':900})
            page.unroute('**/api/run',scripted_run)
            page.click('[data-act="run"]')
            page.wait_for_function('document.querySelector(".run-console .status").textContent==="Běží…"')
            page.click('[data-act="stop"]')
            page.wait_for_function('document.querySelector(".run-console .status").textContent==="Zastaveno."')
            page.goto(f'{base}#/kurz/pygame-2')
            page.wait_for_selector('.mod li')
            assert page.locator('.mod li').count()==30 and page.locator('.mod li.done').count()==6
            page.wait_for_function('document.querySelector(".prep-content")?.textContent.includes("Všech 30 lekcí")')
            page.locator('.learning-plan summary').click()
            plan=page.locator('.learning-plan').inner_text()
            assert 'Hotovo: lekce 26–30.' in plan and '58 ukázek a 86 úkolů' in plan
            if shots:page.screenshot(path=str(shots/'predani-course-desktop.png'),full_page=True)
            page.goto(f'{base}#/kurz/pygame-2/{old}')
            page.wait_for_selector('.editor textarea')
            assert page.locator('.editor textarea').input_value()==previous and page.is_checked('.done-toggle input')
            assert not errors,errors
            browser.close()
        print('OK: závěr26–30, 13 ukázek/21 úkolů/řešení, běhy včetně unittest a GUI, PNG/stažení, workspace, reload/postup, plán/příprava a mobil')
    finally:
        server.runs.stop_all();server.shutdown();server.server_close()
