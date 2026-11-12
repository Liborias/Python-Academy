"""Účty 21–25 v prohlížeči: devět ukázek, pět úkolů a uložená práce."""
import json,os,shutil,sys,tempfile,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from server.app import create_server
IDS=['21-scrypt-sul-a-overeni-hesla','22-registrace-a-jedinecnost','23-mistni-prihlaseni-a-poznamky','24-volitelne-cteni-textu-offline','25-zlib-base64-a-prenos-poznamek']
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
            page=browser.new_page(viewport={'width':1100,'height':900});page.set_default_timeout(30000)
            page.on('pageerror',lambda e:errors.append(str(e)))
            old='20-export-zaloha-a-testy-trackeru';previous='# Moje rozepsané exporty BMI\n'
            page.goto(f'{base}?t={server.token}#/kurz/databaze/{old}');page.wait_for_selector('.editor textarea')
            page.locator('.editor textarea').fill(previous);page.locator('.done-toggle input').check()
            examples=0
            for stage,lid in enumerate(IDS):
                d=root/'courses/databaze/lessons'/lid;meta=json.loads((d/'lesson.json').read_text())
                source=(d/'solution.py').read_text();starter=(d/'exercise.py').read_text()
                page.goto(f'{base}#/kurz/databaze/{lid}')
                page.wait_for_function('(t)=>document.querySelector(".lesson h1")?.textContent===t',arg=meta['title'])
                editor=page.locator('.editor textarea');assert editor.input_value()==starter
                assert page.locator('[data-example]').count()==(3 if stage in (0,4) else 0)
                assert page.locator('[data-task]').count()==0 and page.locator('.quiz fieldset').count()==3
                before=page.evaluate('JSON.stringify(localStorage)');page.locator('.solution-help summary').click()
                page.wait_for_function('document.querySelector(".solution-help code")?.textContent.length>0')
                assert page.locator('.solution-help code').inner_text().rstrip()==source.rstrip()
                assert editor.input_value()==starter and page.evaluate('JSON.stringify(localStorage)')==before
                page.click('[data-act="check"]');page.wait_for_selector('.results .res.bad')
                editor.fill(source);page.click('[data-act="check"]')
                page.wait_for_function('document.querySelectorAll(".results .res.ok").length>0 && !document.querySelectorAll(".results .res.bad").length')
                assert page.is_checked('.done-toggle input')
                for example in range(3 if stage in (0,4) else 1):
                    if stage in (0,4):page.click(f'[data-example="{example}"]')
                    page.click('[data-act="run-ex"]')
                    page.wait_for_function('document.querySelector(".ex-console .status").textContent==="Hotovo."')
                    assert 'Traceback' not in page.locator('.ex-console pre.out').inner_text();examples+=1
                page.click('[data-act="run"]')
                page.wait_for_function('document.querySelector(".run-console .status").textContent==="Hotovo."')
                out=page.locator('.run-console pre.out').inner_text();assert 'Traceback' not in out
                if stage==3:assert 'Režim: nahled' in out
                saved=page.request.post(base+'api/workspace/save',headers={'X-Dilna-Token':server.token},data={'course':'databaze','lesson':lid,'code':source})
                assert saved.ok,saved.text();work=root/'workspace/databaze'/lid
                assert (work/'reseni.py').read_text()==source
                for helper in (d/'files').rglob('*'):
                    if helper.is_file():assert (work/helper.relative_to(d/'files')).read_bytes()==helper.read_bytes()
                assert not list(work.glob('*.sqlite3'))
                for width in [380,320]:
                    page.set_viewport_size({'width':width,'height':800});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(lid,width)
                if shots and stage in (0,4):
                    page.locator('.solution-help').screenshot(path=str(shots/f'ucty-{stage}-solution-mobile.png'))
                    page.locator('.lesson > .prose').screenshot(path=str(shots/f'ucty-{stage}-lesson-mobile.png'))
                page.reload();page.wait_for_selector('.editor textarea')
                assert editor.input_value()==source and page.is_checked('.done-toggle input')
                page.set_viewport_size({'width':1100,'height':900})
            assert examples==9
            page.goto(f'{base}#/kurz/databaze');page.wait_for_selector('.mod li')
            assert page.locator('.mod li').count()==32 and page.locator('.mod li.done').count()==6
            page.wait_for_function('document.querySelector(".prep-content")?.textContent.includes("Všech 32 lekcí")')
            page.locator('.learning-plan summary').click()
            assert '49 ukázek a 61 úkolů' in page.locator('.learning-plan').inner_text()
            if shots:page.screenshot(path=str(shots/'ucty-course.png'),full_page=True)
            page.goto(f'{base}#/kurz/databaze/{old}');page.wait_for_selector('.editor textarea')
            assert page.locator('.editor textarea').input_value()==previous and page.is_checked('.done-toggle input')
            assert not errors,errors;browser.close()
        print('OK: účty21–25, devět ukázek/pět úkolů/řešení, skutečné běhy, workspace, reload/starší postup, plán/příprava a mobil 380/320')
    finally:server.runs.stop_all();server.shutdown();server.server_close()
