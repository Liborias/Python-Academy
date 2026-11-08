import sys
from unittest.mock import patch
import tkinter
from dilna_check import check

c = check()
sys.path.insert(0, str(c.student.parent))
with patch.object(tkinter, "Tk", side_effect=RuntimeError("Import nesmí otevřít okno.")):
    ns = c.load()
work = c.student.parent


def named(r, name, index=-1):
    return next((w for w in r.widgets(index=index) if w.get("name") == name), {})


def fill(name, value):
    return {"action": "fill_text" if name == "telo" else "fill", "name": name, "value": value}


def click(text):
    return {"action": "click", "text": text}

import json
from copy import deepcopy
model={'prijemce':'nedopsaná@','predmet':'  Český koncept  ','text':'  A\nB\n','priloha':str(work/'chybejici-priloha.txt')}
valid=work/'koncept-valid.json';valid.write_text(json.dumps({'verze':1,'koncept':model},ensure_ascii=False),encoding='utf-8')
empty=work/'koncept-prazdny.json';empty.write_text(json.dumps({'verze':1,'koncept':dict.fromkeys(model,'')}),encoding='utf-8')
bad=[]
for i,data in enumerate([{},[],{'verze':True,'koncept':model},{'verze':2,'koncept':model},{'verze':1,'koncept':{}},
                          {'verze':1,'koncept':dict(model,text=3)},{'verze':1,'koncept':dict(model,priloha='relativni.txt')}]):
    p=work/f'koncept-bad-{i}.json';p.write_text(json.dumps(data),encoding='utf-8');bad.append(p)
broken=work/'rozbity.json';broken.write_text('{',encoding='utf-8');bad.append(broken)
encoding=work/'encoding.json';encoding.write_bytes(b'\xff');bad.append(encoding)
if ns:
    for path,expected in [(valid,model),(empty,dict.fromkeys(model,''))]:c.returns(ns,'nacti_koncept',(str(path),),expected)
    for path in bad:c.raises(ns,'nacti_koncept',(str(path),),ValueError,'Ověřte verzi, všechna textová pole a absolutní cestu přílohy. Neexistující absolutní cesta smí být uložená.')
    target=work/'ulozeny.json';before=deepcopy(model)
    ok,value=c.call(ns,'uloz_koncept',(str(target),model))
    try:
        raw=target.read_text('utf-8');saved=json.loads(raw)
        good=ok and value is None and saved=={'verze':1,'koncept':model} and 'Český koncept' in raw and before==model
    except (OSError,ValueError):good=False
    c.add('Uložení neúplného konceptu v UTF-8',good,'Ukládejte přesné texty a cestu, nikoli přílohu, hesla ani stav přenosu; nejde o validaci pro odeslání.')
    target.write_text('Původní obsah',encoding='utf-8')
    ok,error=c.call(ns,'uloz_koncept',(str(target),dict(model,text=None)))
    c.add('Neplatný model nepoškodí cíl',not ok and isinstance(error,ValueError) and target.read_text('utf-8')=='Původní obsah','Vstup ověřte před otevřením cílového souboru.')
    if 'os' in ns:
        with patch.object(ns['os'],'replace',side_effect=OSError('Cvičné selhání nahrazení')):
            ok,error=c.call(ns,'uloz_koncept',(str(target),model))
        c.add('Chyba před nahrazením zachová původní soubor',not ok and isinstance(error,OSError) and target.read_text('utf-8')=='Původní obsah'
              and not list(work.glob('.koncept-*.tmp')), 'Dočasný soubor zavřete, použijte os.replace a ve finally ukliďte zbytek.')
    else:c.add('Nahrazení cíle',False,'Použijte os.replace nad zavřeným dočasným souborem ve stejné složce.')

save=work/'gui-koncept.json'
form=[fill('prijemce','jan@example.test'),fill('predmet','  Rozpracováno  '),fill('telo','Tělo s mezerou \n')]
actions=form+[click('Ověřit a zobrazit'),click('Uložit koncept'),click('Načíst koncept'),click('Načíst koncept'),click('Načíst koncept'),
              click('Uložit koncept'),fill('predmet','Přepsáno'),click('Načíst koncept'),click('Načíst koncept'),click('Ověřit a zobrazit'),
              click('Načíst koncept'),click('Ověřit a zobrazit')]
dialogs=[{'kind':'save','path':str(save)},{'kind':'open','path':''},{'kind':'open','path':str(broken)},
         {'kind':'open','path':str(encoding)},{'kind':'save','path':str(work)},{'kind':'open','path':str(save)},
         {'kind':'open','path':str(empty)},{'kind':'open','path':str(valid)}]
r=c.tk_run(actions,dialogs=dialogs)
if c.tk_no_error(r):
    for index,status in [(5,'Koncept uložen. Nejde o potvrzení přenosu.'),(6,'Načítání zrušeno.'),
                         (7,'Koncept se nepodařilo načíst.'),(8,'Koncept se nepodařilo načíst.'),(9,'Koncept se nepodařilo uložit.')]:
        c.add('Souborová chyba zachová práci '+str(index),named(r,'stav',index).get('text')==status
              and named(r,'predmet',index).get('value')=='  Rozpracováno  ' and named(r,'telo',index).get('value')=='Tělo s mezerou \n'
              and named(r,'nahled',index).get('value')==named(r,'nahled',4).get('value'), 'Zrušení a chyba ponechají pole, přílohu i náhled.')
    c.add('Načtení přepíše celý formulář až po ověření',named(r,'predmet',11).get('value')=='  Rozpracováno  '
          and all(named(r,k,12).get('value')=='' for k in ('prijemce','predmet','telo'))
          and named(r,'nahled',12).get('value')=='Načtený koncept zatím není ověřený.', 'Platný prázdný koncept vymaže pole, neplatný soubor nic nemění; načtení nepotvrzuje odeslání.')
    c.add('Neúplná adresa jde načíst a opravit',named(r,'prijemce',14).get('value')==model['prijemce']
          and named(r,'soubor',14).get('text')=='Příloha: chybejici-priloha.txt'
          and named(r,'stav',15).get('text')=='Příjemce: zadejte jednu platnou adresu.', 'Načtení konceptu neověřuje schránku ani existenci přílohy; validace přijde před předáním.')
    c.add('Náhled zůstává pouze pro čtení',all(named(r,'nahled',i).get('state')=='disabled' for i in range(len(actions)+1)), 'Žádný souborový průchod nesmí nechat náhled editovatelný.')
c.done()
