import json
import sys
from pathlib import Path
from types import SimpleNamespace
from contextlib import contextmanager
from unittest.mock import Mock,patch
from dilna_check import check
c=check();sys.path.insert(0,str(c.student.parent));work=c.student.parent;ns=c.load()
model={'prijemce':'  jan@example.test ','predmet':'  České předání  ','text':' A\nB\n','priloha':''}
path=work/'predani-test.json';attachment=work/'česká příloha.txt';attachment.write_bytes('Žofie\n'.encode('utf-8'))
if ns:
    for file in ('',str(attachment)):
        path.write_text(json.dumps({'verze':1,'koncept':dict(model,priloha=file)},ensure_ascii=False),encoding='utf-8')
        ok,report=c.call(ns,'prover_predani',(str(path),))
        expected={'stav':'prijato','zachyceno':1,'prijemce':'jan@example.test','predmet':'České předání','text':model['text'],
                  'prilohy':[{'nazev':attachment.name,'velikost':len(attachment.read_bytes())}] if file else []}
        c.add('Skutečná zpráva v místním záchytu '+str(bool(file)),ok and report==expected,'Vraťte stav, počet, obálkového příjemce, dekódovaný předmět/tělo a názvy/velikosti přijatých příloh.')
    for status in ('odmitnuto','nejiste','chyba'):
        def result(message,host,port,timeout,fronta):fronta.put(status)
        worker=Mock(side_effect=result)
        with patch.dict(ns,predat_zpravu=worker):ok,error=c.call(ns,'prover_predani',(str(path),))
        c.add('Neúspěch bez opakování '+status,not ok and isinstance(error,RuntimeError) and worker.call_count==1,'Jiný stav než prijato ohlaste RuntimeError. Žádný automatický další pokus.')
    def no_message(message,host,port,timeout,fronta):fronta.put('prijato')
    with patch.dict(ns,predat_zpravu=no_message):ok,error=c.call(ns,'prover_predani',(str(path),))
    c.add('Potvrzení nestačí bez zachycené zprávy',not ok and isinstance(error,RuntimeError),'Po potvrzení ověřte skutečný počet záznamů, nepoužívejte pevné číslo.')
    import queue
    puvodni_prenos=ns['predat_zpravu']
    def uncertain_after_receipt(message,host,port,timeout,fronta):
        original_result=queue.Queue()
        puvodni_prenos(message,host,port,timeout,original_result)
        fronta.put('nejiste')
    with patch.dict(ns,predat_zpravu=uncertain_after_receipt):ok,error=c.call(ns,'prover_predani',(str(path),))
    c.add('Převzetí s nejistým potvrzením není úspěšné předání',not ok and isinstance(error,RuntimeError),
          'I při jedné skutečně zachycené zprávě vyžaduje stav nejiste chybu a žádný automatický další pokus.')
    from zpravy import vytvor_zpravu
    received=vytvor_zpravu('eva@example.test','jana@example.test','Jiný přijatý předmět','Přijaté tělo')
    record=SimpleNamespace(prijemci=('obalkovy@example.test',),data=received.as_bytes())
    @contextmanager
    def capture():yield SimpleNamespace(host='127.0.0.1',port=43210,zpravy=[record])
    with patch.dict(ns,cvicna_posta=capture,predat_zpravu=no_message):ok,report=c.call(ns,'prover_predani',(str(path),))
    c.add('Souhrn čte skutečně přijatá data',ok and report=={'stav':'prijato','zachyceno':1,'prijemce':'obalkovy@example.test','predmet':'Jiný přijatý předmět','text':'Přijaté tělo\n','prilohy':[]}, 'Údaje berte ze zaznam.data a obálky, nikoli z původního konceptu.')
r=c.run()
if c.no_error(r):c.add('Závěrečná ukázka skutečně proběhne','Závěrečné místní ověření:' in r.out and '"zachyceno": 1' in r.out,'Ponechte čitelný souhrn jednoho místního předání.')
c.done()
