"""SQLite6–10: řešení, běhy, vlastnictví dat, konzole a starší postup v prohlížeči."""
import json,os,shutil,subprocess,sys,tempfile,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from server.app import create_server
IDS=['06-null-typy-a-textove-filtry','07-souhrny-a-skupiny','08-cizi-klice-a-vazby','09-spojovani-tabulek','10-projekt-klubovni-evidence']
shots=Path(sys.argv[sys.argv.index('--shots')+1]) if '--shots' in sys.argv else None
if shots:shots.mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory() as temp:
    root=Path(temp)
    for name in ['courses','web','lib']:shutil.copytree(ROOT/name,root/name)
    python=os.environ.get('DILNA_TEST_PYTHON') or sys.executable
    server=create_server(root,'127.0.0.1',0,python=python)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{server.server_address[1]}/';errors=[]
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
            page=browser.new_page(viewport={'width':1100,'height':900})
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.set_default_timeout(30000)
            old='05-transakce-a-vraceni-zmen';previous='# Moje rozepsané transakce skladu\n'
            page.goto(f'{base}?t={server.token}#/kurz/databaze/{old}')
            page.wait_for_selector('.editor textarea')
            page.locator('.editor textarea').fill(previous);page.locator('.done-toggle input').check()
            examples=tasks=0
            for stage,lid in enumerate(IDS):
                d=root/'courses/databaze/lessons'/lid
                title=json.loads((d/'lesson.json').read_text())['title']
                page.goto(f'{base}#/kurz/databaze/{lid}')
                page.wait_for_function('(t)=>document.querySelector(".lesson h1")?.textContent===t',arg=title)
                assert page.locator('[data-example]').count()==(0 if stage==4 else 3)
                assert page.locator('[data-task]').count()==(0 if stage==4 else 5)
                assert page.locator('.quiz fieldset').count()==3
                editor=page.locator('.editor textarea')
                for example in range(1 if stage==4 else 3):
                    if stage<4:page.click(f'[data-example="{example}"]')
                    page.click('[data-act="run-ex"]')
                    page.wait_for_function('document.querySelector(".ex-console .status").textContent==="Hotovo."')
                    out=page.locator('.ex-console pre.out').inner_text();assert 'Traceback' not in out
                    if stage==4:assert 'Podruhé: False' in out and 'Konečný stav:' in out
                    examples+=1
                for task in range(1 if stage==4 else 5):
                    target=d if not task else d/'tasks'/f'task-{task+1}'
                    source=(target/'solution.py').read_text();starter=(target/'exercise.py').read_text()
                    if stage<4:page.click(f'[data-task="{task}"]')
                    editor.fill(starter);before=page.evaluate('JSON.stringify(localStorage)')
                    page.locator('.solution-help summary').click()
                    page.wait_for_function('document.querySelector(".solution-help code")?.textContent.length>0')
                    assert page.locator('.solution-help code').inner_text().rstrip()==source.rstrip()
                    assert editor.input_value()==starter and page.evaluate('JSON.stringify(localStorage)')==before
                    page.click('[data-act="check"]');page.wait_for_selector('.results .res.bad')
                    editor.fill(source);page.click('[data-act="check"]')
                    page.wait_for_function('document.querySelectorAll(".results .res.ok").length>0 && !document.querySelectorAll(".results .res.bad").length')
                    assert page.is_checked('.done-toggle input')
                    page.click('[data-act="run"]')
                    page.wait_for_function('document.querySelector(".run-console .status").textContent==="Hotovo."')
                    assert 'Traceback' not in page.locator('.run-console pre.out').inner_text()
                    data={'course':'databaze','lesson':lid,'code':source,**({'task':f'task-{task+1}'} if task else {})}
                    saved=page.request.post(base+'api/workspace/save',headers={'X-Dilna-Token':server.token},data=data)
                    assert saved.ok,saved.text()
                    work=root/'workspace/databaze'/lid
                    if task:work=work/'tasks'/f'task-{task+1}'
                    assert (work/'reseni.py').read_text()==source
                    for helper in (target/'files').rglob('*'):
                        if helper.is_file():assert (work/helper.relative_to(target/'files')).read_bytes()==helper.read_bytes()
                    assert page.locator('.editor .ed-lines').inner_text().splitlines()[-1]==str(source.count('\n')+1)
                    for width in [380,320]:
                        page.set_viewport_size({'width':width,'height':800})
                        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(lid,task,width)
                    page.set_viewport_size({'width':1100,'height':900});tasks+=1
                page.reload();page.wait_for_selector('.editor textarea')
                assert editor.input_value()==(d/'solution.py').read_text() and page.is_checked('.done-toggle input')
                if stage<4:
                    page.click('[data-task="4"]')
                    assert editor.input_value()==(d/'tasks/task-5/solution.py').read_text()
                page.locator('.solution-help summary').click()
                page.wait_for_function('document.querySelector(".solution-help code")?.textContent.length>0')
                if shots and stage in (2,4):
                    page.set_viewport_size({'width':380,'height':800})
                    page.locator('.solution-help').screenshot(path=str(shots/f'vazby-{stage}-solution-mobile.png'))
                    if stage==4:
                        page.locator('.lesson > .prose').screenshot(path=str(shots/'klub-lesson-mobile.png'))
                        page.click('[data-act="run"]')
                        page.wait_for_function('document.querySelector(".run-console .status").textContent==="Hotovo."')
                        page.locator('.run-console').screenshot(path=str(shots/'klub-output-mobile.png'))
                page.set_viewport_size({'width':1100,'height':900})
            assert (examples,tasks)==(13,21)
            work=root/'workspace/databaze'/IDS[-1];entry=str(work/'spust_klub.py')
            def cli(*args):
                run=subprocess.run([python,'-X','utf8',entry,*args],cwd=root,capture_output=True,text=True,timeout=10)
                assert run.returncode==0,run.stderr+run.stdout
                return run.stdout
            assert 'Kategorie ID: 1' in cli('kategorie','Sport')
            assert 'Pomůcka ID: 1' in cli('pomucka',"Míč O'Neil",'1','--kategorie','1')
            assert 'Výpůjčka ID: 1' in cli('pujcit','1','Žofie')
            assert 'Žofie' in cli('vypujcky')
            assert 'Vráceno: True' in cli('vratit','1')
            assert 'Vráceno: False' in cli('vratit','1')
            assert 'Sport' in cli('prehled') and cli('vypujcky')==''
            assert (work/'klub.sqlite3').read_bytes().startswith(b'SQLite format 3\x00')
            page.goto(f'{base}#/kurz/databaze');page.wait_for_selector('.mod li')
            assert page.locator('.mod li').count()==25 and page.locator('.mod li.done').count()==6
            page.wait_for_function('document.querySelector(".prep-content")?.textContent.includes("Prvních 25 z 32")')
            page.locator('.learning-plan summary').click()
            text=page.locator('.learning-plan').inner_text()
            assert '28 ukázek a 46 úkolů' in text and 'Hotovo: lekce 6–10.' in text
            if shots:page.screenshot(path=str(shots/'sqlite-relations-course.png'),full_page=True)
            page.goto(f'{base}#/kurz/databaze/{old}')
            page.wait_for_selector('.editor textarea')
            assert page.locator('.editor textarea').input_value()==previous and page.is_checked('.done-toggle input')
            assert not errors,errors
            browser.close()
        print('OK: SQLite6–10, 13 ukázek/21 úkolů/řešení, skutečné běhy, exportovaná konzole v několika procesech, workspace, reload/postup, plán/příprava a mobil')
    finally:server.runs.stop_all();server.shutdown();server.server_close()
