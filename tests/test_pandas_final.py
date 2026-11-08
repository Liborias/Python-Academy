"""Analytická dílna: audit, klíče, interpretace, notebook a skutečně oddělený projekt."""
import ast
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'lib'))
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'workspace/_run/_matplotlib'))
from server.checker import run_check
from server.content import lesson_view,solution_view
BASE=ROOT/'courses/pandas/lessons'
IDS=['36-projekt-otazka-a-zdroje','37-projekt-cisteni-s-auditem','38-projekt-spojeni-a-souhrny','39-projekt-graf-a-zprava','40-projekt-testy-vysledku','41-projekt-volitelny-notebook','42-projekt-predani-a-spusteni']


class PandasFinalTest(unittest.TestCase):
    def body(self,stage,name):
        source=(BASE/IDS[stage]/'solution.py').read_text();fn=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name==name)
        return '\n'.join(line[4:] for line in source.splitlines()[fn.body[0].lineno-1:fn.end_lineno])

    def variants(self,stage,name,wrong,correct):
        d=BASE/IDS[stage];source=(d/'solution.py').read_text();fn=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name==name)
        for expected,bodies in [(False,wrong),(True,correct)]:
            for body in bodies:
                lines=source.splitlines();lines[fn.body[0].lineno-1:fn.end_lineno]=['    '+line for line in body.splitlines()]
                code='\n'.join(lines)+'\n';self.assertNotEqual(code,source)
                with self.subTest(function=name,expected=expected,body=body),tempfile.TemporaryDirectory() as temp:
                    report=run_check(d,code,ROOT/'lib',Path(temp))
                    self.assertNotIn('error',report,report);self.assertEqual(report['ok'],expected,report)

    def test_schema_presence_not_values_or_row_count(self):
        self.variants(0,'over_schema',[
            'return len(tabulka)>0','return isinstance(tabulka,pd.DataFrame) and set(povinne).issubset(tabulka.columns)',
            'return isinstance(tabulka,pd.DataFrame) and list(tabulka.columns)==povinne'],
            ['if not isinstance(tabulka,pd.DataFrame):\n    return False\nreturn not tabulka.columns.duplicated().any() and all(k in tabulka.columns for k in povinne)'])

    def test_clean_original_text_priority_finite_zeroes_negatives_and_duplicates(self):
        body=self.body(1,'vycisti_mereni')
        self.variants(1,'vycisti_mereni',[
            body.replace('~np.isfinite(data["teplota"])','data["teplota"].isna()'),
            body.replace('cista = data.loc[duvod.eq("")].reset_index(drop=True)','cista = data.loc[duvod.eq("")].drop_duplicates(["den","kod","teplota"]).reset_index(drop=True)'),
            body.replace('duvod.eq("") & data["den"].isna()','data["den"].isna()'),
            body.replace('original.assign(duvod=duvod)','data.assign(duvod=duvod)'),
            body.replace('cista = data.loc[duvod.eq("")]','cista = data.loc[duvod.eq("") & data["teplota"].gt(0)]')],
            ['import math\n'+body.replace('np.isfinite(data["teplota"])','data["teplota"].map(math.isfinite)')])

    def test_join_catalog_validation_unknowns_identity_and_real_group_means(self):
        body=self.body(2,'spoj_a_shrn')
        self.variants(2,'spoj_a_shrn',[
            body.replace('how="left"','how="inner"'),
            body.replace('validate="many_to_one", ',''),
            body.replace('mista[["kod", "nazev", "oblast"]]','mista[["kod", "nazev", "oblast"]].drop_duplicates("kod")'),
            body.replace('prumer=("teplota", "mean")','prumer=("teplota", "sum")')],
            [body.replace('validate="many_to_one"','validate="m:1"')])

    def test_report_weighted_mean_and_all_exports_include_negative_temperatures(self):
        report=self.body(3,'napis_zpravu');export=self.body(3,'vytvor_vystupy')
        self.variants(3,'napis_zpravu',[
            report.replace("mereni['teplota'].mean()","prehled['podle_mist']['prumer'].mean()"),
            report.replace('neurčen (žádná spárovaná měření)','0,00')],
            [report.replace('"# Analytická dílna\\n\\n"','"# Analytická dílna\\n\\nVýsledek opakovatelného postupu.\\n"')])
        self.variants(3,'vytvor_vystupy',[
            export.replace('stanice["prumer"]','stanice["pocet"]'),
            export.replace('fig = Figure(', 'excel.write_text("není XLSX")\nfig = Figure('),
            export.replace('fig.savefig(graf, dpi=120)','ax.set_ylim(bottom=0)\nfig.savefig(graf, dpi=120)'),
            export.replace('    cisteni["odmitnuta"].to_excel(zapis, sheet_name="Odmítnutá", index=False)','    pass')],
            [export.replace('ax.bar(stanice["kod"], stanice["prumer"])','ax.bar(stanice["kod"], stanice["prumer"], color="purple", width=0.6)')])

    def test_comparison_rejects_broken_results_and_accepts_float_tolerance(self):
        self.variants(4,'over_prehled',['return True','return prehled.keys()==ocekavane.keys()',
            'return all(prehled[k].equals(ocekavane[k]) for k in ocekavane)'],
            ['if set(prehled)!=set(ocekavane):\n    return False\ntry:\n    for key,value in ocekavane.items():\n        pd.testing.assert_frame_equal(value,prehled[key],rtol=1e-12,atol=1e-12,check_exact=False)\nexcept (AssertionError,TypeError,ValueError):\n    return False\nreturn True'])

    def test_notebook_source_order_ids_no_stale_execution_and_string_sources(self):
        body=self.body(5,'vytvor_notebook')
        self.variants(5,'vytvor_notebook',[
            body.replace('enumerate(BUNKY, 1)','enumerate(reversed(BUNKY), 1)'),
            body.replace('"execution_count": None','"execution_count": 7'),
            body.replace('f"krok-{i}"','"uvod"'),
            body.replace('"nbformat": 4','"nbformat": np.int64(4)'),
            body.replace('"nbformat": 4','"nbformat": 4.0'),
            body.replace('"cells": cells','"cells": []'),
            body.replace('"metadata": {}, ',''),
            body.replace('"display_name": "Python 3 (projektová .venv)"','"display_name": ""')],
            [body.replace('source.splitlines(keepends=True)','source')])

    def test_handover_actual_inputs_and_detached_cli_and_tests(self):
        body=self.body(6,'spust_dilnu')
        self.variants(6,'spust_dilnu',[
            body.replace('pd.read_csv(mereni_cesta,','pd.read_csv("mereni.csv",'),
            body.replace('shutil.copy2(mista_cesta, slozka / "mista.csv")','shutil.copy2(mereni_cesta, slozka / "mista.csv")'),
            body.replace('shutil.copytree("projekt", slozka, dirs_exist_ok=True)','slozka.mkdir(parents=True,exist_ok=True)')],
            [body.replace('shutil.copy2(','shutil.copyfile(')])

    def test_scope_helpers_and_every_possible_solution_match_snapshot(self):
        modules=json.loads((BASE.parent/'course.json').read_text())['modules'];self.assertEqual(modules[-1]['lessons'],IDS)
        previous={}
        for i,lid in enumerate(IDS):
            d=BASE/lid;view=lesson_view(ROOT/'courses','pandas',lid)
            self.assertEqual((len(view['examples']),len(view['tasks']),len(view['quiz'])),(0,0,3))
            self.assertTrue(view['download_files']);self.assertEqual(view['preview_images'],i>=3)
            self.assertEqual(solution_view(ROOT/'courses','pandas',lid)['code'],(d/'solution.py').read_text())
            functions={n.name:ast.dump(n,include_attributes=False) for n in ast.parse((d/'solution.py').read_text()).body if isinstance(n,ast.FunctionDef)}
            if i:
                helper={n.name:ast.dump(n,include_attributes=False) for n in ast.parse((d/'files/predchozi.py').read_text()).body if isinstance(n,ast.FunctionDef)}
                self.assertEqual(helper,previous)
            previous.update(functions)
        packaged={n.name:ast.dump(n,include_attributes=False) for n in ast.parse((BASE/IDS[-1]/'files/projekt/predchozi.py').read_text()).body if isinstance(n,ast.FunctionDef)}
        previous.pop('spust_dilnu');self.assertEqual(packaged,previous)

    def test_seven_demos_and_seven_teaching_snippets_with_their_own_sources(self):
        for lid in IDS:
            d=BASE/lid
            for code in [(d/'solution.py').read_text(),*re.findall(r'```python\n(.*?)```',(d/'lesson.md').read_text(),re.S)]:
                with self.subTest(lesson=lid),tempfile.TemporaryDirectory() as temp:
                    work=Path(temp);shutil.copytree(d/'files',work,dirs_exist_ok=True)
                    before={p.relative_to(work):p.read_bytes() for p in work.rglob('*') if p.is_file()}
                    (work/'main.py').write_text(code)
                    result=subprocess.run([sys.executable,'-X','utf8','main.py'],cwd=work,env=dict(os.environ,MPLBACKEND='Agg',PYTHONPATH=str(work)),capture_output=True,text=True,timeout=25)
                    self.assertEqual(result.returncode,0,result.stdout+result.stderr)
                    for name,data in before.items():self.assertEqual((work/name).read_bytes(),data)

    def test_fixture_partition_means_raw_audit_and_public_suite(self):
        from dilna_check.pandas_final import RAW,SITES,clean_oracle,report_oracle
        clean=clean_oracle(RAW);report=report_oracle(clean['cista'],SITES)
        self.assertEqual((len(RAW),len(clean['cista']),len(clean['odmitnuta']),len(report['spojena']),len(report['nesparovana'])),(11,7,4,6,1))
        self.assertEqual(clean['odmitnuta']['radek'].tolist(),[7,8,9,10])
        self.assertEqual(clean['odmitnuta']['duvod'].tolist(),['neplatne_datum','chybi_kod','neplatna_teplota','neplatna_teplota'])
        self.assertEqual(report['podle_mist']['pocet'].tolist(),[3,2,1]);self.assertAlmostEqual(report['spojena']['teplota'].mean(),28/6)
        self.assertNotAlmostEqual(report['podle_mist']['prumer'].mean(),28/6)


if __name__=='__main__':unittest.main()
