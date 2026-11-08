"""Závěr 25–28: vlastní ověřování, argumenty balení, cesty a skutečný místní souhrn."""
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from server.checker import run_check
BASE=ROOT/'courses/tkinter-api/lessons'
IDS=['25-vlastni-testy-dilny','26-volitelne-baleni-aplikace','27-cesty-a-klavesove-zkratky','28-predani-a-zaverecne-overeni']


class TkinterFinishTest(unittest.TestCase):
    def source(self,index):return (BASE/IDS[index]/'solution.py').read_text('utf-8')
    def variants(self,index,wrong,correct):
        for expected,codes in [(False,wrong),(True,correct)]:
            for code in codes:
                self.assertNotEqual(code,self.source(index))
                with self.subTest(expected=expected,code=code),tempfile.TemporaryDirectory() as folder:
                    result=run_check(BASE/IDS[index],code,ROOT/'lib',Path(folder))
                    self.assertNotIn('error',result,result)
                    self.assertEqual(result.get('ok'),expected,result)

    def test_student_tests_detect_all_injected_failures(self):
        s=self.source(0)
        wrong=[s.replace('self.assertEqual(dilna.nacti_koncept(cesta), model)','self.assertTrue(True)'),
               s.replace('"priloha": str(Path(folder) / "chybi.txt")','"priloha": ""'),
               s.replace('with self.assertRaises(ValueError):\n                        dilna.nacti_koncept(cesta)','self.assertTrue(True)'),
               s.replace('self.assertEqual(cesta.read_text(encoding="utf-8"), "Původní práce")','self.assertTrue(True)'),
               s.replace('self.assertEqual(fronta.get_nowait(), stav)','fronta.get_nowait()'),
               s.replace('odesli.assert_called_once_with(zprava, "127.0.0.1", 43210, 0.2)','self.assertTrue(True)'),
               s.replace('self.assertEqual(zprava.get_body(preferencelist=("plain",)).get_content(), " A\\nB\\n")','self.assertTrue(True)'),
               s.replace('    def test_zprava_je_samostatny_snimek(self):','    @unittest.skip("Vynecháno")\n    def test_zprava_je_samostatny_snimek(self):')]
        correct=[re.sub(r'\bmodel\b','koncept',s),s.replace('test_neuplny_koncept_se_zachova','test_ulozeni_rozpracovaneho_textu'),
                 s.replace('verbosity=2','verbosity=1')]
        self.variants(0,wrong,correct)

    def test_build_plan_is_only_an_argument_list_and_keeps_spaced_paths(self):
        s=self.source(1)
        wrong=[s.replace('return prikaz','return " ".join(prikaz)'),s.replace('"--onedir"','"--onefile"'),
               s.replace('str(vystup / "dist")','str(vystup / "build")'),s.replace('prikaz.append(str(skript))','prikaz.append(skript.name)'),
               s.replace('if data.is_dir():','if False:'),s.replace('"--name", jmeno','"--name", "KorespondencniDilna"'),
               s.replace('    skript = Path(skript).resolve()','    Path(vystup).mkdir(parents=True, exist_ok=True)\n    skript = Path(skript).resolve()'),
               s.replace('if not skript.is_file() or skript.suffix.lower() != ".py":','if False:')]
        correct=[s.replace('"--noconfirm", "--clean", "--onedir", "--console"','"--console", "--onedir", "--clean", "--noconfirm"'),
                 re.sub(r'\bprikaz\b','argumenty',s),s.replace('.resolve()','.resolve(strict=False)')]
        self.variants(1,wrong,correct)

    def test_resource_paths_keyboard_and_busy_callbacks(self):
        s=self.source(2)
        wrong=[s.replace('Path(soubor).resolve().parent / "data"','Path.cwd() / "data"'),
               s.replace('Path(domov).expanduser().resolve()','Path.cwd()'),
               s.replace('widget.bind("<Control-s>", klavesa_ulozit)','widget.bind("<Control-s>", klavesa_nacist)'),
               s.replace('widget.bind("<Control-Return>", klavesa_overit)','widget.bind("<Control-Return>", klavesa_nacist)'),
               s.replace('for widget in (okno, prijemce, predmet, telo, nahled):','for widget in (okno, prijemce, predmet, nahled):'),
               s.replace('if model["busy"]:','if False:'),
               s.replace('predmet.insert(0, kandidat["predmet"])','predmet.insert(0, "Pevný předmět")'),
               s.replace('stav.configure(text="Ukázkový koncept není dostupný. Zkontrolujte složku data.")','telo.delete("1.0", "end")\n            stav.configure(text="Ukázkový koncept není dostupný. Zkontrolujte složku data.")')]
        correct=[re.sub(r'\bcesty\b','umisteni',s),s.replace('.resolve()','.resolve(strict=False)'),s.replace('queue.Queue()','queue.SimpleQueue()')]
        self.variants(2,wrong,correct)

    def test_handoff_reports_received_data_and_rejects_unconfirmed_transfer(self):
        s=self.source(3)
        wrong=[s.replace('if stav != "prijato":','if False:'),s.replace('if len(zachycene) != 1:','if False:'),
               s.replace('"prijemce": zaznam.prijemci[0]','"prijemce": str(zprava["To"])'),
               s.replace('str(prijata["Subject"])','str(zprava["Subject"])'),s.replace('"text": telo','"text": koncept["text"]'),
               s.replace('"prilohy": prilohy','"prilohy": []'),s.replace('len(p.get_payload(decode=True))','0'),
               s.replace('predat_zpravu(zprava, posta.host, posta.port, 2, fronta)','predat_zpravu(zprava, posta.host, posta.port, 2, fronta)\n        predat_zpravu(zprava, posta.host, posta.port, 2, fronta)')]
        correct=[re.sub(r'\bzaznam\b','prijaty_zaznam',s),s.replace('queue.Queue()','queue.SimpleQueue()'),s.replace('str(prijata["Subject"])','str(prijata["subject"])')]
        self.variants(3,wrong,correct)

    def test_metadata_and_thirty_nine_exact_helper_copies(self):
        course=json.loads((BASE.parent/'course.json').read_text('utf-8'))
        self.assertEqual(course['modules'][6]['lessons'],IDS)
        self.assertEqual(sum(len(m['lessons']) for m in course['modules']),28)
        self.assertNotIn('pyinstaller',course['requires_packages'])
        pairs={'dilna.py':'24-projekt-korespondencni-dilna/solution.py','koncept.py':'21-koncept-a-formular/solution.py',
               'zpravy.py':'17-emailmessage-a-nahled/solution.py','prilohy.py':'19-prilohy-a-vyber-souboru/solution.py',
               'priprava.py':'22-overeni-zpravy-a-prilohy/solution.py','prenos.py':'23-predani-snimku-na-pozadi/solution.py',
               'odesilani.py':'18-smtp-a-mistni-zachyt/solution.py','nastaveni.py':'20-nastaveni-smtp-a-chyby/solution.py'}
        copies=0
        for i,lid in enumerate(IDS):
            folder=BASE/lid
            self.assertEqual(json.loads((folder/'lesson.json').read_text('utf-8'))['kind'],'gui' if i==2 else 'console')
            self.assertEqual(len(json.loads((folder/'quiz.json').read_text('utf-8'))),10 if i==3 else 3)
            for name,source in pairs.items():
                self.assertEqual((folder/'files'/name).read_bytes(),(BASE/source).read_bytes());copies+=1
            self.assertEqual((folder/'files/cvicna_posta.py').read_bytes(),(BASE.parent/'shared/cvicna_posta.py').read_bytes());copies+=1
        final=BASE/IDS[3]/'files'
        for name,index in [('aplikace.py',2),('baleni.py',1),('test_projekt.py',0)]:
            self.assertEqual((final/name).read_bytes(),(BASE/IDS[index]/'solution.py').read_bytes());copies+=1
        self.assertEqual(copies,39)
        self.assertEqual((final/'data/vychozi-koncept.json').read_bytes(),(BASE/IDS[2]/'files/data/vychozi-koncept.json').read_bytes())
        self.assertIn('6.22.3',(final/'requirements-build.txt').read_text('utf-8'))
        self.assertTrue((final/'README.md').exists() and (final/'SCENARE.md').exists())

    def test_shipped_tests_run_without_window_from_another_directory(self):
        with tempfile.TemporaryDirectory() as folder:
            target=Path(folder)/'projekt s mezerou'
            shutil.copytree(BASE/IDS[3]/'files',target,ignore=shutil.ignore_patterns('__pycache__'))
            r=subprocess.run([sys.executable,'-X','utf8',str(target/'test_projekt.py')],cwd=folder,capture_output=True,text=True,timeout=15)
            self.assertEqual(r.returncode,0,r.stdout+r.stderr)
            self.assertIn('Ran 5 tests',r.stderr)
            self.assertIn('OK',r.stderr)

    def test_final_console_works_from_foreign_cwd_without_changing_resources(self):
        with tempfile.TemporaryDirectory() as folder:
            target=Path(folder)/'projekt'
            shutil.copytree(BASE/IDS[3]/'files',target,ignore=shutil.ignore_patterns('__pycache__'))
            (target/'reseni.py').write_text(self.source(3),encoding='utf-8')
            before=(target/'data/vychozi-koncept.json').read_bytes()
            r=subprocess.run([sys.executable,'-X','utf8',str(target/'reseni.py')],cwd=folder,capture_output=True,text=True,timeout=15)
            self.assertEqual(r.returncode,0,r.stdout+r.stderr)
            report=json.loads(r.stdout.split('\n',1)[1])
            self.assertEqual(report['zachyceno'],1)
            self.assertEqual(report['predmet'],'Pozdrav z dokončené dílny')
            self.assertEqual((target/'data/vychozi-koncept.json').read_bytes(),before)


if __name__=='__main__':unittest.main()
