"""Pandas 16–20: známé hodnoty, klíče, agregace, statistika a skutečný přehled CSV."""
import ast
from contextlib import redirect_stdout
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from server.checker import run_check
from server.content import lesson_view, solution_view
BASE=ROOT/'courses/pandas/lessons'
IDS=['16-souhrny-a-osa-vypoctu','17-seskupovani-pomoci-groupby','18-vice-agregaci-a-nazvy','19-prumer-median-a-rozpeti','20-projekt-prehled-kavarny']


class PandasSummaryTest(unittest.TestCase):
    def verify(self,directory,code,expected):
        with tempfile.TemporaryDirectory() as temp:
            result=run_check(directory,code,ROOT/'lib',Path(temp))
        self.assertNotIn('error',result,result)
        self.assertEqual(result['ok'],expected,result)

    def variants(self,lesson,variants):
        for task,(wrong,correct) in enumerate(variants,1):
            d=BASE/IDS[lesson] if task==1 else BASE/IDS[lesson]/'tasks'/f'task-{task}'
            source=(d/'solution.py').read_text('utf-8')
            function=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef))
            for expected,bodies in [(False,wrong),(True,correct)]:
                for body in bodies:
                    lines=source.splitlines()
                    lines[function.body[0].lineno-1:function.end_lineno]=['    '+line for line in body.splitlines()]
                    code='\n'.join(lines)+'\n'
                    self.assertNotEqual(code,source)
                    with self.subTest(lesson=lesson+16,task=task,expected=expected,body=body):
                        self.verify(d,code,expected)

    def test_axis_min_count_and_three_different_counts(self):
        self.variants(0,[
            (['return tabulka[sloupce].sum().astype("float64")','return tabulka[sloupce].sum(axis=1, min_count=1).astype("float64")'],
             ['return tabulka.loc[:, sloupce].sum(min_count=1).astype(float)']),
            (['return tabulka[sloupce].sum(axis=1).astype("float64")'],
             ['return tabulka.loc[:, sloupce].sum(axis="columns", min_count=1).astype(float)']),
            (['return tabulka[sloupce].isna().sum().astype("int64")'],
             ['return tabulka[sloupce].notna().sum().astype("int64")']),
            (['return {"radky":len(tabulka),"bunky":int(tabulka.count().sum())}'],
             ['return {"bunky":tabulka.shape[0]*tabulka.shape[1],"radky":tabulka.shape[0]}']),
            (['return {"zaznamy":len(serie),"dostupne":int(serie.count()),"soucet":serie.sum(),"prumer":serie.mean()}'],
             ['return {"zaznamy":serie.size,"dostupne":int(serie.notna().sum()),"soucet":serie.sum(min_count=1),"prumer":serie.mean(skipna=True)}']),
        ])

    def test_groupby_missing_keys_all_unknown_values_counts_names_and_shape(self):
        self.variants(1,[
            (['return tabulka.groupby(klic)[hodnota].sum(min_count=1)',
              'return tabulka.groupby(klic,dropna=False,sort=True)[hodnota].sum()'],
             ['return tabulka.groupby(by=klic,sort=True,dropna=False)[hodnota].sum(min_count=1)']),
            (['return tabulka.groupby(klic,dropna=False)["hodnota"].count()'],
             ['return tabulka.groupby(klic,dropna=False,sort=True).agg("size")']),
            (['return tabulka.groupby(klic,dropna=False).size().rename(hodnota)'],
             ['return tabulka.groupby(klic,sort=True,dropna=False)[hodnota].agg("count")']),
            (['return tabulka.groupby(klic,dropna=False)[hodnota].sum(min_count=1)'],
             ['return tabulka.groupby(klic,sort=True,dropna=False)[hodnota].agg("mean")']),
            (['return tabulka.groupby(klic,dropna=False)[hodnota].sum(min_count=1)'],
             ['return tabulka.groupby(klic,dropna=False,sort=True)[hodnota].sum(min_count=1).reset_index()']),
        ])

    def test_named_aggregations_sources_multiple_keys_and_output_sort(self):
        self.variants(2,[
            (['return tabulka.groupby(klic,dropna=False)[hodnota].agg(["mean","count","min","max"])'],
             ['return tabulka.groupby(klic,sort=True,dropna=False)[hodnota].aggregate(["count","mean","min","max"])']),
            (['return tabulka.groupby(klic,as_index=False,dropna=False).agg(radky=(hodnota,"count"),dostupne=(hodnota,"size"),prumer=(hodnota,"mean"))'],
             ['return tabulka.groupby(klic,as_index=False,sort=True,dropna=False).aggregate(radky=(hodnota,"size"),dostupne=(hodnota,"count"),prumer=(hodnota,"mean"))']),
            (['return tabulka.groupby(klic,as_index=False,dropna=False).agg(prumer=(prvni,"mean"),maximum=(prvni,"max"))'],
             ['return tabulka.groupby(klic,as_index=False,sort=True,dropna=False).aggregate(prumer=(prvni,"mean"),maximum=(druha,"max"))']),
            (['return tabulka.groupby(prvni_klic,as_index=False,dropna=False).agg(radky=(hodnota,"size"),prumer=(hodnota,"mean"))'],
             ['return tabulka.groupby([prvni_klic,druhy_klic],dropna=False,sort=True).agg(radky=(hodnota,"size"),prumer=(hodnota,"mean")).reset_index()']),
            (['return tabulka.sort_values("prumer",ascending=False,na_position="last").reset_index(drop=True)'],
             ['return tabulka.sort_values(by=["prumer","skupina"],ascending=[False,True],na_position="last",ignore_index=True)']),
        ])

    def test_statistics_outlier_median_missing_and_strict_above_mean(self):
        self.variants(3,[
            (['return {"dostupne":int(serie.count()),"minimum":serie.min(),"maximum":serie.max(),"prumer":serie.mean(),"median":serie.mean()}'],
             ['return {"dostupne":int(serie.notna().sum()),"minimum":serie.min(),"maximum":serie.max(),"prumer":serie.mean(),"median":serie.quantile(0.5)}']),
            (['return serie.max()','return (serie.max()-serie.min()) if serie.count() else 0.0'],
             ['return serie.agg("max")-serie.agg("min")']),
            (['return serie.loc[serie >= serie.mean()]'],
             ['return serie[serie.gt(serie.mean())]']),
            (['return tabulka[sloupce].mean().astype("float64")'],
             ['return tabulka.loc[:,sloupce].quantile(0.5).astype(float).rename(None)']),
            (['return tabulka.groupby(klic,as_index=False,dropna=False).agg(dostupne=(hodnota,"size"),prumer=(hodnota,"mean"),median=(hodnota,"median"))'],
             ['return tabulka.groupby(klic,as_index=False,sort=True,dropna=False).aggregate(dostupne=(hodnota,"count"),prumer=(hodnota,"mean"),median=(hodnota,"median"))']),
        ])

    def test_project_rejects_wrong_revenue_deduplication_mutation_and_weak_controls(self):
        d=BASE/IDS[4];source=(d/'solution.py').read_text('utf-8')
        wrong=[source.replace('data["kusy"] * data["cena"]','data["cena"]'),
               source.replace('data["kusy"] * data["cena"]','data["kusy"] * data["cena"].mean()'),
               source.replace('data = tabulka.copy()','data = tabulka.drop_duplicates()'),
               source.replace('data = tabulka.copy()','data = tabulka.loc[tabulka["kusy"] > 0].copy()'),
               source.replace('data = tabulka.copy()','data = tabulka'),
               source.replace('"radky": len(data)','"radky": len(podle_dnu)'),
               source.replace('sort=True','sort=False'),
               source.replace('for nazev in ("podle_dnu", "podle_produktu"):','for nazev in ("podle_dnu",):'),
               source.replace('for pole in ("radky", "kusy"):','for pole in ("radky",):'),
               source.replace('for pole in ("radky", "kusy"):','for pole in ("kusy",):'),
               source.replace('if not math.isclose(float(tabulka["trzba"].sum()), prehled["celkem"]["trzba"], rel_tol=1e-12, abs_tol=1e-9):','if float(tabulka["trzba"].sum()) != prehled["celkem"]["trzba"]:'),
               source.replace('abs_tol=1e-9','abs_tol=2'),
               source.replace('if not math.isclose(float(tabulka["trzba"].sum()), prehled["celkem"]["trzba"], rel_tol=1e-12, abs_tol=1e-9):','if round(float(tabulka["trzba"].sum())) != round(prehled["celkem"]["trzba"]):')]
        function=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='over_soucty')
        def body(code):
            lines=source.splitlines();lines[function.body[0].lineno-1:function.end_lineno]=['    '+line for line in code.splitlines()]
            return '\n'.join(lines)+'\n'
        wrong += [body('return True'),body('return False'),body('return 1')]
        correct=[source.replace('"size"','"count"'),source.replace('sort=True','sort=True, dropna=False')]
        correct.append(body('vysledky = []\nfor nazev in ("podle_dnu","podle_produktu"):\n    t = prehled[nazev]\n    vysledky.extend([t["radky"].sum() == prehled["celkem"]["radky"], t["kusy"].sum() == prehled["celkem"]["kusy"]])\n    vysledky.append(math.isclose(float(t["trzba"].sum()), prehled["celkem"]["trzba"], rel_tol=1e-12, abs_tol=1e-9))\nreturn pd.Series(vysledky,dtype=bool).all()'))
        for expected,codes in [(False,wrong),(True,correct)]:
            for code in codes:
                self.assertNotEqual(code,source)
                with self.subTest(expected=expected,code=code):self.verify(d,code,expected)

    def test_metadata_references_and_project_as_one_coherent_task(self):
        course=json.loads((BASE.parent/'course.json').read_text('utf-8'))
        self.assertEqual(course['modules'][3]['lessons'],IDS)
        for i,lid in enumerate(IDS):
            view=lesson_view(ROOT/'courses','pandas',lid)
            self.assertEqual((len(view['examples']),len(view['tasks']),len(view['quiz'])),(2,4,3) if i<4 else (0,0,5))
            for task in range(1,6 if i<4 else 2):
                d=BASE/lid if task==1 else BASE/lid/'tasks'/f'task-{task}'
                self.assertIn('# %%',(d/'exercise.py').read_text('utf-8'))
                self.assertEqual(solution_view(ROOT/'courses','pandas',lid,f'task-{task}')['code'],(d/'solution.py').read_text('utf-8'))

    def test_all_twenty_one_solution_demos_run_with_own_files(self):
        for i,lid in enumerate(IDS):
            for task in range(1,6 if i<4 else 2):
                d=BASE/lid if task==1 else BASE/lid/'tasks'/f'task-{task}'
                with self.subTest(lesson=lid,task=task),tempfile.TemporaryDirectory() as temp:
                    folder=Path(temp)
                    if (d/'files').exists():shutil.copytree(d/'files',folder,dirs_exist_ok=True)
                    before={p.name:p.read_bytes() for p in folder.iterdir()}
                    shutil.copyfile(d/'solution.py',folder/'reseni.py')
                    result=subprocess.run([sys.executable,'-X','utf8',str(folder/'reseni.py')],cwd=folder,capture_output=True,text=True,timeout=15)
                    self.assertEqual(result.returncode,0,result.stdout+result.stderr)
                    self.assertTrue(result.stdout.strip())
                    self.assertEqual({name:(folder/name).read_bytes() for name in before},before)

    def test_real_csv_totals_and_limit_of_balancing_check(self):
        import pandas as pd
        from pandas.testing import assert_frame_equal
        d=BASE/IDS[4];namespace={'__name__':'student'}
        exec((d/'solution.py').read_text('utf-8'),namespace)
        data=pd.read_csv(d/'files/prodeje.csv',sep=';',decimal=',',encoding='utf-8',dtype={'den':'str','produkt':'str','kusy':'int64','cena':'float64'})
        before=data.copy();report=namespace['prehled_kavarny'](data)
        self.assertEqual(report['celkem'],{'radky':7,'kusy':15,'trzba':687.0})
        self.assertEqual(report['podle_dnu']['trzba'].tolist(),[270.0,148.0,269.0])
        self.assertEqual(report['podle_produktu']['trzba'].tolist(),[282.0,305.0,100.0])
        self.assertTrue(namespace['over_soucty'](report));assert_frame_equal(data,before)
        report['podle_produktu'].loc[0,'trzba']+=1.0
        self.assertFalse(namespace['over_soucty'](report))
        report['podle_produktu'].loc[1,'trzba']-=1.0
        self.assertTrue(namespace['over_soucty'](report),'Samotný kontrolní součet nezaručuje správné rozdělení částek do skupin.')

    def test_teaching_snippets_and_mean_of_means_facts(self):
        import pandas as pd
        table=pd.DataFrame({'rano':[1.0,2.0,None],'vecer':[10.0,20.0,None],
                            'produkt':['A','A','B'],'trzba':[10.0,20.0,30.0],
                            'skupina':['A','A','B'],'hodnota':[1.0,2.0,3.0]})
        count=0
        for lid in IDS:
            for code in re.findall(r'```python\n(.*?)```',(BASE/lid/'lesson.md').read_text('utf-8'),re.S):
                with self.subTest(lesson=lid,code=code):
                    namespace={'pd':pd,'tabulka':table.copy()}
                    exec(code,namespace);count+=1
        self.assertEqual(count,4)
        example=json.loads((BASE/IDS[3]/'examples.json').read_text('utf-8'))[1]['code']
        output=io.StringIO()
        with redirect_stdout(output):exec(example,{'__name__':'__main__'})
        self.assertIn('Prostý průměr skupinových průměrů: 180.0',output.getvalue())
        self.assertIn('Průměr všech původních hodnot: 260.0',output.getvalue())


if __name__=='__main__':unittest.main()
