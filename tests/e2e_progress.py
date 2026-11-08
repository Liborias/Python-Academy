"""Postup v několika kartách, obnova po vadných datech a odmítnutém zápisu."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
import threading
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from server.app import create_server

KEY='dilna-python-v1'
shots=Path(sys.argv[sys.argv.index('--shots')+1]) if '--shots' in sys.argv else None
if shots:shots.mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory() as folder:
    root=Path(folder)
    for name in ('courses','web','lib'):shutil.copytree(ROOT/name,root/name)
    server=create_server(root,'127.0.0.1',0)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{server.server_address[1]}/?t={server.token}'
    errors=[]
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
            def page(context,lid=None,init=None):
                result=context.new_page();result.on('pageerror',lambda e:errors.append(str(e)))
                if init:result.add_init_script(init)
                result.goto(base+('#/kurz/zaklady/'+lid if lid else '#/'))
                result.wait_for_selector('.done-toggle input' if lid else 'a.card')
                return result
            def store(pg,name,*args):
                return pg.evaluate('async ([name,args]) => { const s=await import("/js/store.js"); return s[name](...args); }',[name,args])
            def saved(pg):return pg.evaluate('JSON.parse(localStorage.getItem("dilna-python-v1"))')

            # Dvě skutečné karty původně přepisovaly druhým kliknutím první lekci.
            ctx=browser.new_context();one=page(ctx,'01-prvni-program');two=page(ctx,'02-promenne')
            one.locator('.editor textarea').fill('# Práce v první kartě\n')
            two.locator('.editor textarea').fill('# Práce v druhé kartě\n')
            one.locator('.done-toggle input').check();two.locator('.done-toggle input').check()
            assert saved(two)['done']['zaklady']=={'01-prvni-program':1,'02-promenne':1}
            one.reload();one.wait_for_selector('.done-toggle input')
            assert one.is_checked('.done-toggle input') and one.locator('.editor textarea').input_value()=='# Práce v první kartě\n'
            one.locator('.done-toggle input').uncheck()
            store(two,'setCheck','prep:tkinter-api:windows:vscode',True)
            store(one,'markTaskDone','zaklady','01-prvni-program','task-2')
            store(two,'setTheme','light')
            result=saved(one)
            assert result['done']['zaklady']=={'02-promenne':1}
            assert result['checks']['prep:tkinter-api:windows:vscode']==1
            assert result['tasks']['zaklady']['01-prvni-program']['task-2']==1
            editor=two.locator('.editor textarea');editor.focus()
            editor.evaluate('(el)=>el.setSelectionRange(3,8)')
            store(one,'setTheme','dark')
            two.wait_for_function('document.documentElement.dataset.theme === "dark"')
            assert 'Světlý' in two.locator('#theme').inner_text()
            assert editor.input_value()=='# Práce v druhé kartě\n'
            assert editor.evaluate('(el)=>[el.selectionStart,el.selectionEnd]')==[3,8]
            store(two,'setCheck','prep:tkinter-api:windows:vscode',False)
            store(one,'markDone','oop','01-test',True)
            assert saved(one)['checks']['prep:tkinter-api:windows:vscode']==0
            ctx.close()
            print('OK: dvě karty, zrušení splnění, procvičení, checklisty, vzhled i zachovaný text/fokus',flush=True)

            # Bez doručených storage událostí musí zápis také načíst poslední stav.
            ctx=browser.new_context();one=page(ctx,'01-prvni-program')
            two=page(ctx,'02-promenne',"addEventListener('storage',e=>e.stopImmediatePropagation(),true)")
            one.locator('.done-toggle input').check();two.locator('.done-toggle input').check()
            assert saved(two)['done']['zaklady']=={'01-prvni-program':1,'02-promenne':1}
            ctx.close()
            print('OK: zápis ze zastaralé karty i bez storage události',flush=True)

            ctx=browser.new_context();one=page(ctx)
            legacy={'done':{'zaklady':{'01-prvni-program':1,'02-promenne':False,'neplatne':'1'},'oop':None,'pandas':[]},
                    'theme':'dark','checks':{'pripraveno':True,'vypnuto':False,'chyba':{}},
                    'tasks':{'zaklady':{'01-prvni-program':{'task-2':True,'task-3':None},'chyba':[]}},
                    'budouci_pole':{'poznamka':'Zachovat'}}
            raw=json.dumps(legacy,ensure_ascii=False)
            one.evaluate('raw=>localStorage.setItem("dilna-python-v1",raw)',raw)
            one.reload();one.wait_for_selector('a.card')
            assert one.evaluate('localStorage.getItem("dilna-python-v1")')==raw,'Čtení nesmí přepsat původní záznam'
            assert '1 / 40 lekcí' in one.locator('a.card[href="#/kurz/zaklady"]').inner_text()
            assert store(one,'isTaskDone','zaklady','01-prvni-program','task-2') is True
            assert store(one,'getChecks')=={'pripraveno':1,'vypnuto':0}
            assert store(one,'getTheme')=='dark'
            store(one,'markDone','oop','01-test',True)
            result=saved(one)
            assert result['done']['zaklady']=={'01-prvni-program':1} and result['budouci_pole']==legacy['budouci_pole']
            assert result['tasks']['zaklady']['01-prvni-program']=={'task-2':1}
            for raw in ['{','null','[]','23','"text"','{"done":null,"theme":"dark"}']:
                one.evaluate('raw=>localStorage.setItem("dilna-python-v1",raw)',raw)
                one.reload();one.wait_for_selector('a.card')
                assert one.locator('h1').inner_text()=='Vyberte si, co se chcete naučit'
                assert one.evaluate('localStorage.getItem("dilna-python-v1")')==raw
            ctx.close()
            print('OK: neúplný starší postup, platná část dat, vadný JSON a nesprávné typy bez pádu',flush=True)

            # Zápis odmítnutý kvótou smí ponechat práci v paměti a uložit ji později.
            ctx=browser.new_context()
            quota='''const original=Storage.prototype.setItem;
window.povolitZapis=false;
Storage.prototype.setItem=function(key,value){
    if(key==='dilna-python-v1'&&!window.povolitZapis)throw new DOMException('Plné úložiště','QuotaExceededError');
    return original.call(this,key,value);
};'''
            one=page(ctx,'01-prvni-program',quota);two=page(ctx,'02-promenne')
            one.locator('.done-toggle input').check()
            store(one,'markTaskDone','zaklady','01-prvni-program','task-2')
            assert one.locator('#storage-warning').is_visible()
            if shots:
                one.set_viewport_size({'width':380,'height':800})
                assert one.evaluate('document.documentElement.scrollWidth <= innerWidth')
                one.locator('#storage-warning').screenshot(path=str(shots/'storage-warning-mobile.png'))
            two.locator('.done-toggle input').check()
            store(one,'setCheck','pripraveno',True)
            assert store(one,'isDone','zaklady','01-prvni-program') is True
            assert store(one,'isDone','zaklady','02-promenne') is True
            assert store(one,'isTaskDone','zaklady','01-prvni-program','task-2') is True
            one.evaluate('window.povolitZapis=true')
            store(one,'setTheme','dark')
            result=saved(one)
            assert result['done']['zaklady']=={'01-prvni-program':1,'02-promenne':1}
            assert result['tasks']['zaklady']['01-prvni-program']['task-2']==1 and result['checks']['pripraveno']==1
            assert one.locator('#storage-warning').is_hidden()
            ctx.close()
            print('OK: odmítnutý zápis, uchování změn v paměti a uložení po obnovení bez ztráty druhé karty',flush=True)

            # Při nepřístupném úložišti funguje aktuální stránka bez výjimky.
            ctx=browser.new_context()
            blocked='''const get=Storage.prototype.getItem,set=Storage.prototype.setItem;
Storage.prototype.getItem=function(k){if(k==='dilna-python-v1')throw new DOMException('Zakázáno','SecurityError');return get.call(this,k);};
Storage.prototype.setItem=function(k,v){if(k==='dilna-python-v1')throw new DOMException('Zakázáno','SecurityError');return set.call(this,k,v);};'''
            one=page(ctx,'01-prvni-program',blocked)
            one.locator('.done-toggle input').check()
            store(one,'markDone','zaklady','02-promenne',True)
            store(one,'setCheck','kontrola',True)
            store(one,'setTheme','dark')
            assert store(one,'doneCount','zaklady')==2 and store(one,'getChecks')['kontrola']==1
            assert one.evaluate('document.documentElement.dataset.theme')=='dark'
            assert one.locator('#storage-warning').is_visible()
            ctx.close()
            print('OK: nepřístupné úložiště, práce v paměti a vzhled',flush=True)

            # Úmyslné vymazání postupu nemá další karta vrátit ze starého snímku.
            ctx=browser.new_context();one=page(ctx,'01-prvni-program');two=page(ctx,'02-promenne')
            one.locator('.done-toggle input').check()
            one.evaluate('localStorage.removeItem("dilna-python-v1")')
            two.wait_for_function('localStorage.getItem("dilna-python-v1") === null')
            store(two,'markDone','zaklady','02-promenne',True)
            assert saved(two)['done']['zaklady']=={'02-promenne':1}
            one.evaluate('localStorage.clear()')
            store(two,'setCheck','nova-kontrola',True)
            assert saved(two)['done']=={} and saved(two)['checks']=={'nova-kontrola':1}
            ctx.close()
            assert not errors,errors
            browser.close()
            print('OK: vymazání a nové uložení bez obnovení starého postupu',flush=True)
    finally:
        server.runs.stop_all();server.shutdown();server.server_close()
