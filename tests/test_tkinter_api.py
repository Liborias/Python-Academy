"""Tkinter 13–16: přenos, schéma dat, odezva GUI a skutečné místní API."""
import json
import os
import runpy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import requests

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from server.checker import run_check

BASE=ROOT/'courses/tkinter-api/lessons'
IDS=['13-api-get-a-json','14-chyby-http-a-platna-data','15-vlakno-fronta-a-after','16-projekt-prevodnik-men']


class TkinterApiTest(unittest.TestCase):
    def source(self,index):return (BASE/IDS[index]/'solution.py').read_text('utf-8')
    def variants(self,index,wrong,correct):
        for expected,variants in [(False,wrong),(True,correct)]:
            for code in variants:
                self.assertNotEqual(code,self.source(index))
                with self.subTest(expected=expected,code=code),tempfile.TemporaryDirectory() as temp:
                    result=run_check(BASE/IDS[index],code,ROOT/'lib',Path(temp))
                    self.assertNotIn('error',result,result)
                    self.assertEqual(result.get('ok'),expected,result)

    def test_get_parameters_timeout_and_status(self):
        s=self.source(0)
        wrong=[s.replace('symbol = mena.strip().upper()','symbol = mena.upper()'),s.replace('params={"mena": symbol}','params={"mena": "EUR"}'),
               s.replace(', timeout=2',''),s.replace('"/kurz"','"/jiny"'),s.replace('odpoved.raise_for_status()',''),
               s.replace('return odpoved.json()','return odpoved.text'),s.replace('adresa.rstrip("/")','"http://pevna.test"')]
        correct=[s.replace('requests.get(','requests.Session().get('),s.replace('params={"mena": symbol}','params=[("mena", symbol)]'),s.replace('timeout=2','timeout=(1, 2)')]
        self.variants(0,wrong,correct)

    def test_schema_and_failed_transport(self):
        s=self.source(1)
        wrong=[s.replace('odpoved.raise_for_status()',''),s.replace('mena.strip().upper()','mena.upper()'),
               s.replace('isinstance(kurz, bool) or ',''),s.replace('kurz <= 0','kurz < 0'),
               s.replace('not math.isfinite(kurz) or ',''),s.replace(' or data.get("mena") != symbol',''),
               s.replace('date.fromisoformat(datum).isoformat() != datum','False'),s.replace(' or not zdroj.strip()',''),
               s.replace('    return {"mena": symbol','    data["zdroj"] = zdroj.strip()\n    return {"mena": symbol'),
               s.replace('timeout=timeout','timeout=2')]
        correct=[s.replace('requests.get(','requests.Session().get('),s.replace('isinstance(kurz, bool)','type(kurz) is bool'),
                 s.replace('zdroj.strip()','zdroj.lstrip().rstrip()')]
        self.variants(1,wrong,correct)

    def test_background_task_and_recovery(self):
        s=self.source(2)
        wrong=[s.replace('target=pracovnik, args=(url,)','target=pracovnik(url), args=(url,)'),
               s.replace('            okno.after(25, vyzvedni)','            pass'),
               s.replace('data = nacti_kurz(url,','data = nacti_kurz(adresa + rezim.get(),'),
               s.replace('            vysledky.put((True, data))','            kurz_text.configure(text="Špatné vlákno")\n            vysledky.put((True, data))'),
               s.replace('threading.Thread(target=pracovnik, args=(url,), daemon=True).start()','t = threading.Thread(target=pracovnik, args=(url,), daemon=True)\n        t.start()\n        t.join()'),
               s.replace('tlacitko.configure(state="disabled")','tlacitko.configure(state="normal")'),
               s.replace('tlacitko.configure(state="normal")','tlacitko.configure(state="disabled")'),
               s.replace('pocitadlo.set(pocitadlo.get() + 1)','pocitadlo.set(1)')]
        correct=[s.replace('queue.Queue()','queue.SimpleQueue()'),s.replace('after(25,','after(10,'),
                 s.replace('threading.Thread(target=pracovnik, args=(url,), daemon=True).start()','threading.Thread(target=lambda: pracovnik(url), daemon=True).start()')]
        self.variants(2,wrong,correct)

    def test_conversion_current_rate_sources_and_error_state(self):
        s=self.source(3)
        wrong=[s.replace('castka * kurz','castka / kurz'),s.replace('return vysledek','return round(vysledek, 2)'),
               s.replace('castka < 0','castka < -10'),s.replace('isinstance(hodnota, bool) or ',''),
               s.replace('if not math.isfinite(vysledek):','if False:'),s.replace('.replace(",", ".")',''),
               s.replace('nacteno.clear()','pass'),s.replace('preved_castku(cislo, nacteno[0]["czk_za_jednotku"])','preved_castku(cislo, 25)'),
               s.replace('prvek.configure(state="disabled")','prvek.configure(state="normal")'),
               s.replace('prevod.configure(state="disabled")','prevod.configure(state="normal")')]
        correct=[s.replace('castka * kurz','kurz * castka'),s.replace('hlavni','spust_okno'),
                 s.replace('f"Výsledek: {hodnota:.2f} CZK"','"Výsledek: {:.2f} CZK".format(hodnota)')]
        self.variants(3,wrong,correct)

    def test_metadata_and_identical_helper_copies(self):
        course=json.loads((BASE.parent/'course.json').read_text('utf-8'))
        self.assertEqual(course['modules'][3]['lessons'],IDS)
        for index,lid in enumerate(IDS):
            d=BASE/lid
            self.assertEqual(json.loads((d/'lesson.json').read_text('utf-8'))['kind'],'console' if index<2 else 'gui')
            self.assertEqual(len(json.loads((d/'quiz.json').read_text('utf-8'))),3)
            self.assertEqual((d/'files/cvicne_api.py').read_bytes(),(BASE.parent/'shared/cvicne_api.py').read_bytes())
        for index in (2,3):self.assertEqual((BASE/IDS[index]/'files/kurzy.py').read_bytes(),(BASE/IDS[1]/'solution.py').read_bytes())
        data=json.loads((BASE/IDS[3]/'files/kurzy.json').read_text('utf-8'))
        self.assertEqual((data['EUR']['czk_za_jednotku'],data['USD']['czk_za_jednotku']),(24,19))

    def test_actual_api_statuses_timeout_and_scoped_loopback_proxy(self):
        helper=runpy.run_path(str(BASE.parent/'shared/cvicne_api.py'))
        with patch.dict(os.environ,{'NO_PROXY':'example.test','no_proxy':'example.test'}):
            with helper['cvicne_api']() as address:
                self.assertIn('127.0.0.1',os.environ['NO_PROXY'])
                self.assertIn('example.test',os.environ['NO_PROXY'])
                data=requests.get(address+'/kurz',params={'mena':'EUR'},timeout=2).json()
                self.assertEqual((data['czk_za_jednotku'],data['zdroj']),(25,'Cvičné API'))
                self.assertEqual(requests.get(address+'/kurz',params={'mena':'USD'},timeout=2).json()['czk_za_jednotku'],20)
                self.assertEqual(requests.get(address+'/chyba/kurz?mena=EUR',timeout=2).status_code,503)
                self.assertEqual(requests.get(address+'/kurz?mena=XYZ',timeout=2).status_code,404)
                with self.assertRaises(ValueError):requests.get(address+'/neplatny-json/kurz?mena=EUR',timeout=2).json()
                with self.assertRaises(requests.Timeout):requests.get(address+'/pomalu/kurz?mena=EUR',timeout=.03)
            self.assertEqual(os.environ['NO_PROXY'],'example.test')
            self.assertEqual(os.environ['no_proxy'],'example.test')

    def test_actual_validating_client_and_recovery(self):
        path=BASE/IDS[1]/'solution.py'
        previous=sys.modules.pop('cvicne_api',None);sys.path.insert(0,str(path.parent/'files'))
        try:
            ns=runpy.run_path(str(path),run_name='transport_test')
            with ns['cvicne_api']() as address:
                self.assertEqual(ns['nacti_kurz'](address,' eur ')['czk_za_jednotku'],25)
                for suffix,error in [('/chyba',requests.HTTPError),('/neplatny-json',ValueError),('/spatna-data',ValueError)]:
                    with self.subTest(suffix=suffix),self.assertRaises(error):ns['nacti_kurz'](address+suffix,'EUR')
                with self.assertRaises(requests.Timeout):ns['nacti_kurz'](address+'/pomalu','EUR',timeout=.03)
                self.assertEqual(ns['nacti_kurz'](address,'USD')['czk_za_jednotku'],20)
        finally:
            sys.path.pop(0);sys.modules.pop('cvicne_api',None)
            if previous is not None:sys.modules['cvicne_api']=previous


if __name__=='__main__':unittest.main()
