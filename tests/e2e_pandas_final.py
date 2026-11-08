"""Sedm navazujících kroků: řešení, audity, soubory, notebook, předání a postup."""
import json,os,shutil,sys,tempfile,threading
from pathlib import Path
from zipfile import ZipFile
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
from server.app import create_server
IDS=['36-projekt-otazka-a-zdroje','37-projekt-cisteni-s-auditem','38-projekt-spojeni-a-souhrny','39-projekt-graf-a-zprava','40-projekt-testy-vysledku','41-projekt-volitelny-notebook','42-projekt-predani-a-spusteni']
shots=Path(sys.argv[sys.argv.index('--shots')+1]) if '--shots' in sys.argv else None
if shots:shots.mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory() as temp:
    root=Path(temp)
    for name in ['courses','web','lib']:shutil.copytree(ROOT/name,root/name)
    server=create_server(root,'127.0.0.1',0,python=os.environ.get('DILNA_TEST_PYTHON'))
    threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_address[1]}/'
    errors=[]
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
            page=browser.new_page(viewport={'width':1100,'height':900});page.set_default_timeout(30000)
            page.on('pageerror',lambda e:errors.append(str(e)))
            previous='# Moje rozepsaná měsíční analýza\n'
            page.goto(f'{base}?t={server.token}#/kurz/pandas/35-projekt-mesicni-prehled')
            page.wait_for_selector('.editor textarea');page.locator('.editor textarea').fill(previous);page.locator('.done-toggle input').check()
            for i,lid in enumerate(IDS):
                directory=root/'courses/pandas/lessons'/lid;title=json.loads((directory/'lesson.json').read_text())['title']
                page.goto(f'{base}#/kurz/pandas/{lid}');page.wait_for_function('(title)=>document.querySelector(".lesson h1")?.textContent===title',arg=title)
                assert page.locator('[data-task]').count()==0 and page.locator('[data-example]').count()==0
                assert page.locator('.quiz fieldset').count()==3
                assert page.locator('.ex-editor textarea').evaluate('(el)=>el.readOnly')
                editor=page.locator('.editor textarea');draft=f'# Moje práce v {lid}\n';editor.fill(draft)
                before=page.evaluate('JSON.stringify(localStorage)')
                page.locator('.solution-help summary').click();page.wait_for_function('document.querySelector(".solution-help code")?.textContent.length>0')
                source=(directory/'solution.py').read_text()
                assert page.locator('.solution-help code').inner_text().rstrip()==source.rstrip()
                assert editor.input_value()==draft and page.evaluate('JSON.stringify(localStorage)')==before
                page.click('[data-act="check"]');page.wait_for_selector('.results .res.bad');assert not page.is_checked('.done-toggle input')
                editor.fill(source);page.click('[data-act="check"]')
                page.wait_for_function('document.querySelectorAll(".results .res.ok").length>0 && document.querySelectorAll(".results .res.bad").length===0')
                assert page.is_checked('.done-toggle input')
                for act,console in [('run-ex','ex-console'),('run','run-console')]:
                    page.click(f'[data-act="{act}"]');page.wait_for_function('(sel)=>document.querySelector(sel+" .status").textContent==="Hotovo."',arg='.'+console)
                    assert 'Traceback' not in page.locator(f'.{console} pre.out').inner_text()
                    assert page.locator(f'.{console} .file-downloads a').count()>=4
                    if i>=3 and i!=4:
                        page.wait_for_function('(sel)=>document.querySelector(sel+" .plot-gallery img")?.naturalWidth===720',arg='.'+console)
                    if i>=5:
                        link=page.locator(f'.{console} .file-downloads a[download="analyticka_dilna.ipynb"]')
                        with page.expect_download() as download:link.click()
                        path=Path(temp)/'stazeny.ipynb';download.value.save_as(path)
                        notebook=json.loads(path.read_text('utf-8'));assert notebook['nbformat']==4 and len(notebook['cells'])==6
                    if i==6:
                        assert page.locator(f'.{console} .file-downloads a').count()==12
                        assert not page.locator(f'.{console} .file-downloads .hint').count()
                        link=page.locator(f'.{console} .file-downloads a[download="zprava.md"]')
                        with page.expect_download() as download:link.click()
                        path=Path(temp)/'zprava.md';download.value.save_as(path);text=path.read_text('utf-8')
                        assert 'Celkový průměr: 4,67 °C' in text and 'Odmítnuté záznamy: 4.' in text
                        link=page.locator(f'.{console} .file-downloads a[download="prehled.xlsx"]')
                        with page.expect_download() as download:link.click()
                        path=Path(temp)/'prehled.xlsx';download.value.save_as(path)
                        with ZipFile(path) as wb:assert 'xl/worksheets/sheet4.xml' in wb.namelist()
                saved=page.request.post(base+'api/workspace/save',headers={'X-Dilna-Token':server.token},data={'course':'pandas','lesson':lid,'code':source})
                assert saved.ok,saved.text();target=root/'workspace/pandas'/lid
                assert (target/'reseni.py').read_text()==source
                for f in (directory/'files').rglob('*'):
                    if f.is_file() and '__pycache__' not in f.parts:assert (target/f.relative_to(directory/'files')).read_bytes()==f.read_bytes()
                page.reload();page.wait_for_selector('.editor textarea');assert editor.input_value()==source and page.is_checked('.done-toggle input')
                assert not page.locator('.solution-help').evaluate('(el)=>el.open')
                assert page.locator('.file-downloads').last.is_hidden()
                page.set_viewport_size({'width':380,'height':800})
                page.locator('.solution-help summary').click();page.wait_for_function('document.querySelector(".solution-help code")?.textContent.length>0')
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),page.url
                if shots and i==6:
                    page.locator('.solution-help').screenshot(path=str(shots/'final-solution-mobile.png'))
                    page.click('[data-act="run"]');page.wait_for_function('document.querySelector(".run-console .status").textContent==="Hotovo."')
                    page.locator('.run-console .file-downloads').evaluate('(el)=>el.scrollIntoView({block:"center"})')
                    page.wait_for_timeout(150);page.screenshot(path=str(shots/'final-downloads-mobile.png'))
                page.set_viewport_size({'width':1100,'height':900})
            page.goto(f'{base}#/kurz/pandas');page.wait_for_selector('.mod li')
            assert page.locator('.mod li').count()==42 and page.locator('.mod li.done').count()==8
            page.locator('.learning-plan summary').click()
            if shots:page.screenshot(path=str(shots/'final-course-desktop.png'),full_page=True)
            page.goto(f'{base}#/kurz/pandas/35-projekt-mesicni-prehled');page.wait_for_selector('.editor textarea')
            assert page.locator('.editor textarea').input_value()==previous and page.is_checked('.done-toggle input')
            assert not errors,errors;browser.close()
        print('OK: pandas 36–42, 7 ukázek/kontrol/řešení/běhů, MD/IPYNB/XLSX/CSV/PNG, samostatný projekt, workspace, přesné řešení, reload, zachovaný postup a mobil')
    finally:server.runs.stop_all();server.shutdown();server.server_close()
