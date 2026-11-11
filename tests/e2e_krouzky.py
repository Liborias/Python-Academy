"""Evidence kroužků 11–15 v prohlížeči: řešení, GUI běhy/stop a uložená práce."""
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
IDS=['11-datova-vrstva-krouzku','12-formular-a-pridani-krouzku','13-upravy-a-mazani-krouzku','14-prihlasky-a-kapacita','15-dokonceni-a-testy-evidence']
shots=Path(sys.argv[sys.argv.index('--shots')+1]) if '--shots' in sys.argv else None
if shots:shots.mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory() as temp:
    root=Path(temp)
    for name in ['courses','web','lib']:shutil.copytree(ROOT/name,root/name)
    server=create_server(root,'127.0.0.1',0,python=os.environ.get('DILNA_TEST_PYTHON') or sys.executable)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{server.server_address[1]}/';errors=[]
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
            page=browser.new_page(viewport={'width':1100,'height':900})
            page.on('pageerror',lambda error:errors.append(str(error)))
            page.set_default_timeout(30000)
            old='10-projekt-klubovni-evidence';previous='# Moje rozepsaná klubovní evidence\n'
            page.goto(f'{base}?t={server.token}#/kurz/databaze/{old}')
            page.wait_for_selector('.editor textarea');page.locator('.editor textarea').fill(previous)
            page.locator('.done-toggle input').check()
            for stage,lid in enumerate(IDS):
                d=root/'courses/databaze/lessons'/lid
                meta=json.loads((d/'lesson.json').read_text());source=(d/'solution.py').read_text();starter=(d/'exercise.py').read_text()
                page.goto(f'{base}#/kurz/databaze/{lid}')
                page.wait_for_function('(t)=>document.querySelector(".lesson h1")?.textContent===t',arg=meta['title'])
                editor=page.locator('.editor textarea')
                assert editor.input_value()==starter
                assert page.locator('[data-example]').count()==0 and page.locator('[data-task]').count()==0
                assert page.locator('.quiz fieldset').count()==3
                if stage in (1,2,3):assert 'otevře okno' in page.locator('.lesson .meta').inner_text()
                before=page.evaluate('JSON.stringify(localStorage)')
                page.locator('.solution-help summary').click()
                page.wait_for_function('document.querySelector(".solution-help code")?.textContent.length>0')
                assert page.locator('.solution-help code').inner_text().rstrip()==source.rstrip()
                assert editor.input_value()==starter and before==page.evaluate('JSON.stringify(localStorage)')
                page.click('[data-act="check"]');page.wait_for_selector('.results .res.bad')
                editor.fill(source);page.click('[data-act="check"]')
                page.wait_for_function('document.querySelectorAll(".results .res.ok").length>0 && !document.querySelectorAll(".results .res.bad").length')
                assert page.is_checked('.done-toggle input')
                for action,console,stop in [('run-ex','.ex-console','stop-ex'),('run','.run-console','stop')]:
                    page.click(f'[data-act="{action}"]')
                    if stage in (1,2,3):
                        page.wait_for_function('(s)=>document.querySelector(s+" .status").textContent==="Běží…"',arg=console)
                        page.wait_for_timeout(600)
                        assert page.locator(console+' .status').inner_text()=='Běží…',page.locator(console).inner_text()
                        page.click(f'[data-act="{stop}"]')
                        page.wait_for_function('(s)=>document.querySelector(s+" .status").textContent==="Zastaveno."',arg=console)
                    else:
                        page.wait_for_function('(s)=>document.querySelector(s+" .status").textContent==="Hotovo."',arg=console)
                        out=page.locator(console+' pre.out').inner_text()
                        assert 'Traceback' not in out
                        if stage==4:assert 'Ran 6 tests' in out and 'OK' in out
                saved=page.request.post(base+'api/workspace/save',headers={'X-Dilna-Token':server.token},data={'course':'databaze','lesson':lid,'code':source})
                assert saved.ok,saved.text()
                work=root/'workspace/databaze'/lid
                assert (work/'reseni.py').read_text()==source
                for helper in (d/'files').rglob('*'):
                    if helper.is_file():assert (work/helper.relative_to(d/'files')).read_bytes()==helper.read_bytes()
                assert not list(work.glob('*.sqlite3'))
                for width in [380,320]:
                    page.set_viewport_size({'width':width,'height':800})
                    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(lid,width)
                if shots and stage in (3,4):
                    page.locator('.solution-help').screenshot(path=str(shots/f'krouzky-{stage}-solution-mobile.png'))
                    page.locator('.lesson > .prose').screenshot(path=str(shots/f'krouzky-{stage}-lesson-mobile.png'))
                page.reload();page.wait_for_selector('.editor textarea')
                assert editor.input_value()==source and page.is_checked('.done-toggle input')
                page.set_viewport_size({'width':1100,'height':900})
            page.goto(f'{base}#/kurz/databaze');page.wait_for_selector('.mod li')
            assert page.locator('.mod li').count()==15 and page.locator('.mod li.done').count()==6
            page.wait_for_function('document.querySelector(".prep-content")?.textContent.includes("Prvních 15 z 32")')
            assert 'python -m tkinter' in page.locator('.prep-content').inner_text()
            page.locator('.learning-plan summary').click()
            assert '33 ukázek a 51 úkolů' in page.locator('.learning-plan').inner_text()
            if shots:page.screenshot(path=str(shots/'krouzky-course.png'),full_page=True)
            page.goto(f'{base}#/kurz/databaze/{old}');page.wait_for_selector('.editor textarea')
            assert page.locator('.editor textarea').input_value()==previous and page.is_checked('.done-toggle input')
            assert not errors,errors
            browser.close()
        print('OK: kroužky 11–15, pět řešení/úkolů, skutečné GUI start/stop, konzolové běhy, workspace, reload/postup a mobil 380/320')
    finally:
        server.runs.stop_all();server.shutdown();server.server_close()
