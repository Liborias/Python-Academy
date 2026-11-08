"""Projekt 21–24: čerstvé koncepty, pole chyb, snímek SMTP a zachování uložené práce."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from server.checker import run_check

BASE=ROOT/'courses/tkinter-api/lessons'
IDS=['21-koncept-a-formular','22-overeni-zpravy-a-prilohy','23-predani-snimku-na-pozadi','24-projekt-korespondencni-dilna']


class CorrespondenceTest(unittest.TestCase):
    def source(self,index):return (BASE/IDS[index]/'solution.py').read_text('utf-8')
    def variants(self,index,wrong,correct):
        for expected,variants in [(False,wrong),(True,correct)]:
            for code in variants:
                self.assertNotEqual(code,self.source(index))
                with self.subTest(expected=expected,code=code),tempfile.TemporaryDirectory() as temp:
                    result=run_check(BASE/IDS[index],code,ROOT/'lib',Path(temp))
                    self.assertNotIn('error',result,result)
                    self.assertEqual(result.get('ok'),expected,result)
    def isolated(self,index,program):
        with tempfile.TemporaryDirectory() as temp:
            work=Path(temp)
            for f in (BASE/IDS[index]/'files').glob('*'):
                if f.is_file():shutil.copy2(f,work/f.name)
            (work/'student_model.py').write_text(self.source(index),encoding='utf-8')
            result=subprocess.run([sys.executable,'-X','utf8','-c',program],cwd=work,capture_output=True,text=True,timeout=15)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)

    def test_concept_preserves_incomplete_data_and_fresh_widget_values(self):
        s=self.source(0)
        wrong=[s.replace('"prijemce": prijemce','"prijemce": prijemce.strip()'),
               s.replace('"text": text','"text": text.strip()'),s.replace('"priloha": priloha','"priloha": ""'),
               s.replace('if not all(isinstance(v, str) for v in (prijemce, predmet, text, priloha)):','if False:'),
               s.replace('telo.get("1.0", "end-1c")','telo.get("1.0", "end")'),
               s.replace('prijemce.get(), predmet.get(),','"jan@example.test", "První",'),
               s.replace('nahled.configure(state="disabled")','nahled.configure(state="normal")')]
        correct=[s.replace('"prijemce": prijemce, "predmet": predmet','"predmet": predmet, "prijemce": prijemce'),
                 s.replace('raise ValueError("Pole konceptu musí být texty.")','raise ValueError("Koncept potřebuje textová pole.")'),
                 s.replace('koncept = vytvor_koncept','aktualni = vytvor_koncept').replace('nahled_konceptu(koncept))','nahled_konceptu(aktualni))')]
        self.variants(0,wrong,correct)

    def test_validation_targets_field_and_attachments_are_snapshots(self):
        s=self.source(1)
        wrong=[s.replace('prijemce = over_adresu(kandidat["prijemce"])','prijemce = "jan@example.test"'),
               s.replace('ChybaPole("predmet",','ChybaPole("text",'),
               s.replace('if not kandidat["text"].strip():','if False:'),
               s.replace('kandidat["text"])','kandidat["text"].strip())'),
               s.replace('pridej_prilohu(zprava, kandidat["priloha"])','pass'),
               s.replace('model["priloha"] = str(Path(cesta).resolve())','model["priloha"] = ""'),
               s.replace('if not cesta:\n            stav.configure(text="Výběr přílohy zrušen.")','if not cesta:\n            model["priloha"] = ""\n            soubor_text.configure(text="Bez přílohy.")\n            stav.configure(text="Výběr přílohy zrušen.")'),
               s.replace('pole.get(chyba.pole, prijemce).focus_set()','prijemce.focus_set()')]
        correct=[s.replace('kandidat','overena_data'),s.replace('if not kandidat["text"].strip():','if kandidat["text"].strip() == "":'),
                 s.replace('model','stav_formulare')]
        self.variants(1,wrong,correct)

    def test_worker_queue_and_gui_refusal_uncertainty_and_manual_retry(self):
        s=self.source(2)
        wrong=[s.replace('odesli_do_zachytu(zprava, host, port, timeout)','odesli_do_zachytu(zprava, host, port, 2)'),
               s.replace('fronta.put("prijato")','fronta.put("chyba")'),s.replace('fronta.put("odmitnuto")','fronta.put("prijato")'),
               s.replace('fronta.put("nejiste")','fronta.put("odmitnuto")'),s.replace('fronta.put("chyba")','raise'),
               s.replace('if model["nutna_kontrola"]:\n            stav.configure','if False:\n            stav.configure'),
               s.replace('model["busy"] = False','model["busy"] = False\n        telo.delete("1.0", "end")'),
               s.replace('threading.Thread(target=predat_zpravu,\n                         args=(zprava, nastaveni["host"], nastaveni["port"], nastaveni["timeout"], vysledky),\n                         daemon=True).start()',
                         'predat_zpravu(zprava, nastaveni["host"], nastaveni["port"], nastaveni["timeout"], vysledky)')]
        correct=[s.replace('fronta.put(','fronta.put_nowait('),s.replace('queue.Queue()','queue.SimpleQueue()'),
                 s.replace('model','stav_formulare')]
        self.variants(2,wrong,correct)

    def test_json_version_types_atomic_replace_and_gui_preservation(self):
        s=self.source(3)
        wrong=[s.replace('"verze": 1','"verze": 2'),s.replace('ensure_ascii=False','ensure_ascii=True'),
               s.replace('type(dokument.get("verze")) is not int or ',' '),
               s.replace('return over_ulozitelny_koncept(dokument.get("koncept"))','return dokument.get("koncept")'),
               s.replace('os.replace(docasny, cil)','cil.write_text(obsah, encoding="utf-8")'),
               s.replace('docasny.unlink(missing_ok=True)','pass'),
               s.replace('predmet.insert(0, kandidat["predmet"])','predmet.insert(0, kandidat["predmet"].strip())'),
               s.replace('if not cesta:\n            stav.configure(text="Načítání zrušeno.")','if not cesta:\n            telo.delete("1.0", "end")\n            stav.configure(text="Načítání zrušeno.")')]
        correct=[s.replace('indent=2','indent=4'),s.replace('kandidat','overena_data'),
                 s.replace('type(dokument.get("verze")) is not int','(not isinstance(dokument.get("verze"), int) or isinstance(dokument.get("verze"), bool))')]
        self.variants(3,wrong,correct)

    def test_metadata_and_all_eighteen_dependency_copies(self):
        course=json.loads((BASE.parent/'course.json').read_text('utf-8'))
        self.assertEqual(course['modules'][5]['lessons'],IDS)
        pairs={ 'koncept.py':IDS[0]+'/solution.py','zpravy.py':'17-emailmessage-a-nahled/solution.py',
                'prilohy.py':'19-prilohy-a-vyber-souboru/solution.py','priprava.py':IDS[1]+'/solution.py',
                'odesilani.py':'18-smtp-a-mistni-zachyt/solution.py','nastaveni.py':'20-nastaveni-smtp-a-chyby/solution.py',
                'prenos.py':IDS[2]+'/solution.py'}
        copies=0
        for i,lid in enumerate(IDS):
            folder=BASE/lid
            self.assertEqual(json.loads((folder/'lesson.json').read_text('utf-8'))['kind'],'gui')
            self.assertEqual(len(json.loads((folder/'quiz.json').read_text('utf-8'))),3)
            for name,source in pairs.items():
                if (folder/'files'/name).exists():
                    self.assertEqual((folder/'files'/name).read_bytes(),(BASE/source).read_bytes());copies+=1
            if i>=2:
                self.assertEqual((folder/'files/cvicna_posta.py').read_bytes(),(BASE.parent/'shared/cvicna_posta.py').read_bytes());copies+=1
        self.assertEqual(copies,18)

    def test_failed_save_preserves_target_and_incomplete_draft_roundtrips(self):
        self.isolated(3,r'''
import json
from pathlib import Path
from unittest.mock import patch
import student_model as m
assert not hasattr(m,'okno')
model={'prijemce':'jan@','predmet':'  Žofie  ','text':' A\nB\n','priloha':str(Path('neexistuje.bin').resolve())}
original=dict(model);target=Path('moje-prace.json')
m.uloz_koncept(target,model)
assert m.nacti_koncept(target)==model and model==original
before=target.read_bytes()
with patch.object(m.os,'replace',side_effect=OSError('Zkouška selhání')):
    try:m.uloz_koncept(target,dict(model,text='Změněno'))
    except OSError:pass
    else:raise AssertionError('Zápis nesmí ohlásit úspěch')
assert target.read_bytes()==before and not list(Path('.').glob('.koncept-*.tmp'))
for wrong in [dict(model,text=None),dict(model,priloha='relativni.txt')]:
    try:m.uloz_koncept(target,wrong)
    except ValueError:pass
    else:raise AssertionError('Neplatný model')
assert target.read_bytes()==before
''')

    def test_real_smtp_uses_frozen_content_and_retry_is_explicit(self):
        self.isolated(2,r'''
from pathlib import Path
from email.parser import BytesParser
from email.policy import default
import queue
import student_model as m
path=Path('česká příloha.txt');path.write_bytes('Žofie\n'.encode('utf-8'))
concept=m.vytvor_koncept('jan@example.test','Původní snímek','První text\n',str(path))
message=m.sestav_zpravu(concept)
concept['predmet']='Novější práce';concept['text']='Nový text';path.write_bytes(b'jine bajty')
with m.cvicna_posta() as capture:
    q=queue.Queue();m.predat_zpravu(message,capture.host,capture.port,2,q)
    assert q.get_nowait()=='prijato' and len(capture.zpravy)==1
    record=capture.zpravy[0];parsed=BytesParser(policy=default).parsebytes(record.data)
    assert str(parsed['Subject'])=='Původní snímek' and record.prijemci==('jan@example.test',)
    assert parsed.get_body(preferencelist=('plain',)).get_content().replace('\r\n','\n')=='První text\n'
    assert list(parsed.iter_attachments())[0].get_payload(decode=True)=='Žofie\n'.encode('utf-8')
    capture.nastav_rezim('odmitnout');m.predat_zpravu(message,capture.host,capture.port,2,q)
    assert q.get_nowait()=='odmitnuto' and len(capture.zpravy)==1
    capture.nastav_rezim('pomalu');m.predat_zpravu(message,capture.host,capture.port,.05,q)
    assert q.get_nowait()=='nejiste' and len(capture.zpravy)==2
''')


if __name__=='__main__':unittest.main()
