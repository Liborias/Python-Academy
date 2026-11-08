import io
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
import tkinter
from dilna_check import check

c=check();sys.path.insert(0,str(c.student.parent))
import dilna,prenos,priprava

def load():
    with patch.object(tkinter,'Tk',side_effect=RuntimeError('Testy nemají otevírat okno.')):
        return c.load()

def run(ns):
    cls=ns.get('TestDilna') if ns else None
    if not isinstance(cls,type) or not issubclass(cls,unittest.TestCase):
        raise ValueError('Definujte TestDilna jako potomka unittest.TestCase.')
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(cls)
    return unittest.TextTestRunner(stream=io.StringIO()).run(suite)

try:
    result=run(load())
    valid=result.wasSuccessful() and result.testsRun>=5 and not result.skipped and not result.expectedFailures
    c.add('Pět skutečných testů projde správným projektem',valid,'Doplňte pět scénářů, používejte unittest a testy nepřeskakujte.')
    puvodni_nacti=dilna.nacti_koncept;puvodni_uloz=dilna.uloz_koncept;puvodni_worker=prenos.predat_zpravu;puvodni_zprava=priprava.sestav_zpravu
    def trim(cesta):
        model=puvodni_nacti(cesta);model['text']=model['text'].strip();return model
    def bez_prilohy(cesta):
        model=puvodni_nacti(cesta);model['priloha']='';return model
    def verze(cesta):return dilna.over_ulozitelny_koncept(json.loads(Path(cesta).read_text('utf-8'))['koncept'])
    def typ(cesta):
        doc=json.loads(Path(cesta).read_text('utf-8'))
        if doc.get('verze')==1 and not isinstance(doc['koncept'].get('text'),str):return doc['koncept']
        return puvodni_nacti(cesta)
    def znic_cil(cesta,model):
        Path(cesta).write_text('',encoding='utf-8');return puvodni_uloz(cesta,model)
    def zamen_stav(zprava,host,port,timeout,fronta):
        import queue
        q=queue.Queue();puvodni_worker(zprava,host,port,timeout,q)
        stav=q.get_nowait();fronta.put('prijato' if stav=='odmitnuto' else stav)
    def ignoruj_timeout(zprava,host,port,timeout,fronta):return puvodni_worker(zprava,host,port,2,fronta)
    def orizni_telo(model):
        zprava=puvodni_zprava(model);zprava.get_body(preferencelist=('plain',)).set_content(model['text'].strip());return zprava
    mutants=[(dilna,'nacti_koncept',trim,'ztrátu mezer a řádků'),(dilna,'nacti_koncept',bez_prilohy,'ztrátu cesty přílohy'),
             (dilna,'nacti_koncept',verze,'přijetí neplatné verze'),(dilna,'nacti_koncept',typ,'přijetí chybného typu textu'),
             (dilna,'uloz_koncept',znic_cil,'zničení starší práce při chybě'),(prenos,'predat_zpravu',zamen_stav,'záměnu odmítnutí za přijetí'),
             (prenos,'predat_zpravu',ignoruj_timeout,'ignorování předaného timeoutu'),(priprava,'sestav_zpravu',orizni_telo,'změnu těla při sestavení')]
    if valid:
        for owner,name,replacement,label in mutants:
            with patch.object(owner,name,replacement):
                result=run(load())
            c.add('Testy odhalí '+label,bool(result.failures or result.errors),'Přidejte ověření uvedeného výsledku či zachovaného stavu přes veřejné rozhraní.')
except BaseException as error:
    c.add('Sadu lze spustit',False,f'{type(error).__name__}: {error}')
r=c.run()
if c.no_error(r):c.add('Hlavní blok provede unittest','Ran ' in r.out+r.err and 'OK' in r.out+r.err,'Ponechte unittest.main v hlavním bloku; běžný výstup testů může být na stderr.')
c.done()
