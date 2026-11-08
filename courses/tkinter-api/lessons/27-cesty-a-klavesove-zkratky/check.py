import json
import sys
from pathlib import Path
from unittest.mock import patch
import tkinter
from dilna_check import check
c=check();sys.path.insert(0,str(c.student.parent));work=c.student.parent
with patch.object(tkinter,'Tk',side_effect=RuntimeError('Import nesmí otevřít okno.')):ns=c.load()
for file,home in [(work/'zdroje s mezerou/app.py',work/'uživatel'),(work/'balicek/_internal/aplikace.py',work/'jiný domov')]:
    ok,paths=c.call(ns,'cesty_projektu',(str(file),str(home)))
    c.add('Cesty určuje program a domov',ok and paths=={'data':file.resolve().parent/'data','koncepty':home.resolve()},'Nepoužívejte cwd ani umístění sys.executable. Vraťte absolutní Path pro data vedle souboru a zadaný domov.')
    c.add('Výpočet cest nic nezapisuje',not file.parent.exists() and not home.exists(),'Cesty jen vypočtěte; zápis provede až zvolená souborová operace.')

def click(text):return {'action':'click','text':text}
def fill(name,value):return {'action':'fill_text' if name=='telo' else 'fill','name':name,'value':value}
def focus(name,kind='text'):return {'action':'focus','kind':kind,'name':name}
def key(sequence):return {'action':'key','sequence':sequence}
def named(r,name,index=-1):return next((w for w in r.widgets(index=index) if w.get('name')==name),{})
model={'prijemce':'zofie@example.test','predmet':'  Zkouška cest  ','text':' A\nB\n','priloha':''}
asset=work/'data/vychozi-koncept.json';asset.parent.mkdir(exist_ok=True)
asset.write_text(json.dumps({'verze':1,'koncept':model},ensure_ascii=False),encoding='utf-8')
save=work/'klavesnice.json';send='Předat místnímu záchytu'
wait={'action':'wait','until':{'text':send,'state':'normal'},'timeout':2}
actions=[click('Načíst ukázku'),focus('telo'),key('<Control-Return>'),key('<Control-s>'),fill('predmet','Změněno'),key('<Control-o>'),
         click('Opožděné potvrzení'),click(send),key('<Control-s>'),key('<Control-o>'),click('Načíst ukázku'),wait]
r=c.tk_run(actions,dialogs=[{'kind':'save','path':str(save)},{'kind':'open','path':str(save)}],extra_env={'DILNA_SMTP_HOST':'127.0.0.1','DILNA_SMTP_TIMEOUT':'2'})
if c.tk_no_error(r):
    c.add('Text má vlastní zkratky před třídní vazbou',all(sequence in named(r,'telo',0).get('bindings',[]) for sequence in ('<Control-s>','<Control-o>','<Control-Return>')),
          'Ponechte vlastní vazby také na Text, aby jeho třídní obsluha nevložila znak před callbackem okna.')
    for index in (1,6):
        c.add('Úplně načtený koncept '+str(index),[named(r,k,index).get('value') for k in ('prijemce','predmet','telo')]==[model[k] for k in ('prijemce','predmet','text')], 'Použijte všechny hodnoty ze zdroje či JSON, žádné předvyplněné konstanty.')
    c.add('Ctrl+Enter ověřuje a neposílá',named(r,'stav',3).get('text')=='Zpráva je připravená. Nic se neodeslalo.' and named(r,'zachyt',3).get('text')=='Zachyceno: 0','Klávesová zkratka má pouze obnovit ověřený náhled.')
    c.add('Ctrl+S/Ctrl+O jen jednou a bez změny textu',len(r.dialogs or [])==2 and named(r,'telo',6).get('value')==model['text'], 'Vazby na polích vracejí break; nemá se vložit nový řádek ani otevřít druhý dialog.')
    for index in (9,10,11):
        c.add('Klávesnice a ukázka respektují přenos '+str(index),named(r,'stav',index).get('text')=='Předávám zprávu místnímu záchytu...'
              and named(r,'predmet',index).get('value')==model['predmet'],'Busy chrání i klávesovou cestu, nikoli pouze disabled tlačítko.')
    c.add('Přenos po klávesovém ovládání',named(r,'stav',12).get('text')=='Zprávu převzal místní záchyt.','Původní předání do záchytu nadále funguje.')
for broken in ('{',None):
    if broken is None:asset.unlink()
    else:asset.write_text(broken,encoding='utf-8')
    bad=c.tk_run([fill('prijemce','jan@'),fill('predmet','Rozepsáno'),fill('telo',' A\n'),click('Načíst ukázku')])
    if c.tk_no_error(bad,'Chyba zdroje zachová formulář'):
        c.add('Srozumitelná chyba zdroje',named(bad,'stav').get('text')=='Ukázkový koncept není dostupný. Zkontrolujte složku data.'
              and named(bad,'predmet').get('value')=='Rozepsáno' and named(bad,'telo').get('value')==' A\n','Chybějící nebo vadný zdroj nesmí nahradit rozepsaná pole.')
c.done()
