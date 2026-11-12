"""SQLite: 15 ukázek, 25 úkolů/řešení, export pracovních souborů a mobil."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from server.app import create_server
IDS=['01-sqlite-spojeni-a-soubor','02-tabulky-a-omezeni','03-parametrizovane-zmeny','04-vyber-a-razeni-dat','05-transakce-a-vraceni-zmen']
shots=Path(sys.argv[sys.argv.index('--shots')+1]) if '--shots' in sys.argv else None
if shots:shots.mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory() as temp:
    root=Path(temp)
    for name in ['courses','web','lib']:shutil.copytree(ROOT/name,root/name)
    python=os.environ.get('DILNA_TEST_PYTHON') or sys.executable
    server=create_server(root,'127.0.0.1',0,python=python)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{server.server_address[1]}/'
    errors=[]
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
            page=browser.new_page(viewport={'width':1100,'height':900})
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.set_default_timeout(30000)
            old='30-kuryrska-smena-a-predani'
            previous='# Moje rozepsaná Kurýrská směna\n'
            page.goto(f'{base}?t={server.token}#/kurz/pygame-2/{old}')
            page.wait_for_selector('.editor textarea')
            page.locator('.editor textarea').fill(previous)
            page.locator('.done-toggle input').check()
            page.goto(f'{base}#/')
            page.wait_for_selector('a.card[href="#/kurz/databaze"]')
            page.click('a.card[href="#/kurz/databaze"]')
            page.wait_for_selector('.mod li')
            assert page.locator('.mod li').count()==25
            assert not page.locator('.mod li.done').count()
            page.wait_for_function('document.querySelector(".prep-content")?.textContent.includes("Prvních 25 z 32")')
            page.locator('.learning-plan summary').click()
            assert '15 ukázek a 25 úkolů' in page.locator('.learning-plan').inner_text()
            examples=tasks=0
            for lid in IDS:
                d=root/'courses/databaze/lessons'/lid
                title=json.loads((d/'lesson.json').read_text())['title']
                page.goto(f'{base}#/kurz/databaze/{lid}')
                page.wait_for_function('(t)=>document.querySelector(".lesson h1")?.textContent===t',arg=title)
                assert page.locator('[data-example]').count()==3
                assert page.locator('[data-task]').count()==5
                assert page.locator('.quiz fieldset').count()==3
                editor=page.locator('.editor textarea')
                for example in range(3):
                    page.click(f'[data-example="{example}"]')
                    page.click('[data-act="run-ex"]')
                    page.wait_for_function('document.querySelector(".ex-console .status").textContent==="Hotovo."')
                    assert 'Traceback' not in page.locator('.ex-console pre.out').inner_text()
                    examples+=1
                for task in range(5):
                    target=d if task==0 else d/'tasks'/f'task-{task+1}'
                    source=(target/'solution.py').read_text()
                    starter=(target/'exercise.py').read_text()
                    page.click(f'[data-task="{task}"]')
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
                    assert 'Traceback' not in page.locator('.run-console pre.out').inner_text()
                    context={'course':'databaze','lesson':lid,'code':source,**({'task':f'task-{task+1}'} if task else {})}
                    saved=page.request.post(base+'api/workspace/save',headers={'X-Dilna-Token':server.token},data=context)
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
                    page.set_viewport_size({'width':1100,'height':900})
                    tasks+=1
                page.reload();page.wait_for_selector('.editor textarea')
                assert editor.input_value()==(d/'solution.py').read_text()
                assert page.is_checked('.done-toggle input')
                page.click('[data-task="4"]')
                assert editor.input_value()==(d/'tasks/task-5/solution.py').read_text()
                page.locator('.solution-help summary').click()
                page.wait_for_function('document.querySelector(".solution-help code")?.textContent.length>0')
                if shots and lid==IDS[-1]:
                    page.set_viewport_size({'width':380,'height':800})
                    page.locator('.solution-help').screenshot(path=str(shots/'sqlite-solution-mobile.png'))
                    page.locator('.task-description').screenshot(path=str(shots/'sqlite-exercise-mobile.png'))
                page.set_viewport_size({'width':1100,'height':900})
            assert (examples,tasks)==(15,25)
            # Skutečný uložený studentský kód pracuje se stejným souborem i v novém procesu.
            work=root/'workspace/databaze'/IDS[2]
            code="""import sqlite3
import reseni
from schema import vytvor_pomucky
con = sqlite3.connect('trvale.sqlite3', autocommit=True)
vytvor_pomucky(con)
reseni.pridej_pomucku(con, "Žofie O'Neil", 3)
con.close()
"""
            run=subprocess.run([python,'-X','utf8','-c',code],cwd=work,capture_output=True,text=True,timeout=10)
            assert run.returncode==0,run.stderr
            code="""import sqlite3
con = sqlite3.connect('trvale.sqlite3', autocommit=True)
assert con.execute('SELECT nazev, kusy FROM pomucky').fetchall() == [("Žofie O'Neil", 3)]
con.close()
"""
            run=subprocess.run([python,'-X','utf8','-c',code],cwd=work,capture_output=True,text=True,timeout=10)
            assert run.returncode==0,run.stderr
            assert (work/'trvale.sqlite3').read_bytes().startswith(b'SQLite format 3\x00')
            page.goto(f'{base}#/kurz/databaze')
            page.wait_for_selector('.mod li')
            assert page.locator('.mod li.done').count()==5
            page.locator('.learning-plan summary').click()
            assert 'Hotovo: lekce 1–5.' in page.locator('.learning-plan').inner_text()
            if shots:page.screenshot(path=str(shots/'sqlite-course-desktop.png'),full_page=True)
            page.goto(f'{base}#/kurz/pygame-2/{old}')
            page.wait_for_selector('.editor textarea')
            assert page.locator('.editor textarea').input_value()==previous and page.is_checked('.done-toggle input')
            assert not errors,errors
            browser.close()
        print('OK: SQLite1–5, 15 ukázek/25 úkolů/řešení, skutečné běhy, SQL soubor ve dvou procesech, workspace, reload/postup, příprava/plán a mobil')
    finally:
        server.runs.stop_all();server.shutdown();server.server_close()
