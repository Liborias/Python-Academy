"""Pandas 21–25: indexy, klíče, odmítnutí nejednoznačnosti a časové hranice."""
import ast
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'lib'))
from server.checker import run_check
from server.content import lesson_view, solution_view
BASE=ROOT/'courses/pandas/lessons'
IDS=['21-zarovnani-a-concat','22-spojovani-pomoci-merge','23-klice-a-kontrola-spojeni','24-casovy-index-a-obdobi','25-resample-a-casove-souhrny']


class PandasJoinsTest(unittest.TestCase):
    def variants(self,lesson,variants):
        for task,(wrong,correct) in enumerate(variants,1):
            d=BASE/IDS[lesson] if task==1 else BASE/IDS[lesson]/'tasks'/f'task-{task}'
            source=(d/'solution.py').read_text('utf-8')
            function=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef))
            for expected,bodies in [(False,wrong),(True,correct)]:
                for body in bodies:
                    lines=source.splitlines();lines[function.body[0].lineno-1:function.end_lineno]=['    '+line for line in body.splitlines()]
                    code='\n'.join(lines)+'\n';self.assertNotEqual(code,source)
                    with self.subTest(lesson=lesson+21,task=task,expected=expected,body=body),tempfile.TemporaryDirectory() as temp:
                        result=run_check(d,code,ROOT/'lib',Path(temp))
                        self.assertNotIn('error',result,result);self.assertEqual(result['ok'],expected,result)

    def test_concat_alignment_shapes_duplicates_and_empty_intersection(self):
        self.variants(0,[
            (['return serie.loc[popisky]','return serie.reindex(popisky).fillna(0)'],
             ['return pd.Series([serie.loc[k] if k in serie.index else float("nan") for k in popisky],index=popisky,name=serie.name,dtype="float64")']),
            (['return pd.concat([prvni,druha])','return pd.concat([prvni,druha],ignore_index=True).drop_duplicates().reset_index(drop=True)'],
             ['return pd.concat(objs=[prvni,druha],axis=0,ignore_index=True)']),
            (['return pd.concat([prvni.reset_index(drop=True),druha.reset_index(drop=True)],axis=1)'],
             ['return prvni.join(druha,how="outer").sort_index()']),
            (['return pd.concat([prvni,druha],ignore_index=True,join="outer")'],
             ['sloupce = [k for k in prvni.columns if k in druha.columns]\nif not sloupce:\n    return pd.DataFrame(index=range(len(prvni)+len(druha)))\nreturn pd.concat([prvni[sloupce],druha[sloupce]],ignore_index=True)']),
            (['return pd.concat([prvni,druha],ignore_index=True)'],
             ['return pd.concat(objs=[prvni,druha],axis="index")']),
        ])

    def test_merge_left_inner_dynamic_different_and_composite_keys(self):
        self.variants(1,[
            (['return prodeje.merge(cenik,on="produkt",how="inner")'],
             ['return pd.merge(prodeje,cenik,how="left",on="produkt",sort=False)']),
            (['return prodeje.merge(cenik,on="produkt",how="left")'],
             ['return pd.merge(prodeje,cenik,how="inner",on="produkt",sort=False)']),
            (['return leva.merge(prava,on=klic,how="outer",sort=True)'],
             ['return leva.join(prava.set_index(klic),on=klic,how="left").reset_index(drop=True)']),
            (['return objednavky.merge(produkty.rename(columns={"id":"kod"}),on="kod",how="left")'],
             ['return pd.merge(objednavky,produkty,how="left",left_on="kod",right_on="id",sort=False)']),
            (['return prodeje.merge(cenik,on="produkt",how="left")'],
             ['return pd.merge(prodeje,cenik,how="left",on=["den","produkt"],sort=False)']),
        ])

    def test_validate_checks_whole_lookup_both_sides_indicator_and_suffixes(self):
        self.variants(2,[
            (['return prodeje.merge(cenik,on="produkt",how="left")',
              'return prodeje.merge(cenik.drop_duplicates("produkt"),on="produkt",how="left")',
              'return prodeje.merge(cenik,on="produkt",how="left",validate="one_to_many")'],
             ['return pd.merge(prodeje,cenik,on="produkt",how="left",sort=False,validate="m:1")']),
            (['return leva.merge(prava,on=klic,how="outer",sort=True,validate="many_to_one")',
              'return leva.merge(prava,on=klic,how="left",sort=False,validate="one_to_one")'],
             ['return pd.merge(leva,prava,on=klic,how="outer",sort=True,validate="1:1")']),
            (['return leva.merge(prava,on=klic,how="outer",sort=True)',
              'return leva.merge(prava,on=klic,how="left",indicator=True)'],
             ['return leva.merge(prava,on=klic,how="outer",sort=True,indicator="_merge")']),
            (['v = prodeje.merge(cenik,on="produkt",how="left")\nreturn v.loc[v["cena"].isna(),prodeje.columns].reset_index(drop=True)'],
             ['return prodeje.loc[~prodeje["produkt"].isin(cenik["produkt"])].reset_index(drop=True)']),
            (['return leva.merge(prava,on=klic,how="left")'],
             ['return leva.rename(columns={"stav":"stav_objednavka"}).merge(prava.rename(columns={"stav":"stav_sklad"}),on=klic,how="left",sort=False)']),
        ])

    def test_time_index_stability_inclusive_instants_full_day_and_grid(self):
        self.variants(3,[
            (['return tabulka.set_index(sloupec)','return tabulka.set_index(sloupec).sort_index()'],
             ['return tabulka.sort_values(sloupec,kind="stable").set_index(sloupec)']),
            (['return tabulka.loc[(tabulka.index > pd.Timestamp(od)) & (tabulka.index < pd.Timestamp(do))]'],
             ['return tabulka.loc[(tabulka.index >= pd.Timestamp(od)) & (tabulka.index <= pd.Timestamp(do))]']),
            (['return tabulka.loc[(tabulka.index >= pd.Timestamp(den)) & (tabulka.index <= pd.Timestamp(den)+pd.Timedelta(hours=23,minutes=59,seconds=59))]',
              'return tabulka.loc[(tabulka.index >= pd.Timestamp(den)) & (tabulka.index <= pd.Timestamp(den)+pd.Timedelta(days=1))]'],
             ['return tabulka.loc[den:den]']),
            (['index = pd.date_range(zacatek,konec,freq="D",name=serie.index.name).as_unit("us")\nreturn serie.reindex(index,method="ffill")'],
             ['index = pd.DatetimeIndex(pd.date_range(zacatek,konec,freq="D").as_unit("us").to_numpy(),name=serie.index.name)\nreturn serie.reindex(index)']),
            (['return tabulka.reset_index(drop=True)'], ['return tabulka.reset_index(drop=False)']),
        ])

    def test_resample_nan_zeros_midnights_records_means_and_calendar_months(self):
        self.variants(4,[
            (['return serie.resample("D").sum()',
              'return serie.resample("D",closed="right",label="left").sum(min_count=1)'],
             ['return serie.resample(rule="D",label="left",closed="left").sum(min_count=1)']),
            (['return serie.resample("D").count()'],
             ['return serie.resample("D").apply(lambda s: len(s)).astype("int64")']),
            (['return serie.resample("D").sum(min_count=1)'], ['return serie.resample("D").agg("mean")']),
            (['return serie.resample("30D").sum(min_count=1)'],
             ['return serie.resample(pd.offsets.MonthBegin(),closed="left",label="left").sum(min_count=1)']),
            (['return tabulka.resample("D").agg(radky=(sloupec,"count"),dostupne=(sloupec,"count"),prumer=(sloupec,"mean"))'],
             ['return tabulka.resample("D")[sloupec].agg(["size","count","mean"]).rename(columns={"size":"radky","count":"dostupne","mean":"prumer"})']),
        ])

    def test_metadata_and_all_twenty_five_references(self):
        course=json.loads((BASE.parent/'course.json').read_text('utf-8'))
        self.assertEqual(course['modules'][4]['lessons'],IDS)
        for lid in IDS:
            view=lesson_view(ROOT/'courses','pandas',lid)
            self.assertEqual((len(view['examples']),len(view['tasks']),len(view['quiz'])),(2,4,3))
            for task in range(1,6):
                d=BASE/lid if task==1 else BASE/lid/'tasks'/f'task-{task}'
                self.assertIn('# %%',(d/'exercise.py').read_text('utf-8'))
                self.assertEqual(solution_view(ROOT/'courses','pandas',lid,f'task-{task}')['code'],(d/'solution.py').read_text('utf-8'))

    def test_all_twenty_five_demos_run_as_scripts(self):
        for lid in IDS:
            for task in range(1,6):
                d=BASE/lid if task==1 else BASE/lid/'tasks'/f'task-{task}'
                with self.subTest(lesson=lid,task=task),tempfile.TemporaryDirectory() as temp:
                    result=subprocess.run([sys.executable,'-X','utf8',str(d/'solution.py')],cwd=temp,capture_output=True,text=True,timeout=15)
                    self.assertEqual(result.returncode,0,result.stdout+result.stderr);self.assertTrue(result.stdout.strip())

    def test_join_to_time_aggregation_preserves_sources_and_unknowns(self):
        import pandas as pd
        from pandas.testing import assert_frame_equal,assert_series_equal
        def function(lesson,name):
            namespace={'__name__':'student'};exec((BASE/IDS[lesson]/'solution.py').read_text('utf-8'),namespace);return namespace[name]
        prodeje=pd.DataFrame({'produkt':['A','B','A','C'],'kusy':[2,1,0,1]})
        cenik=pd.DataFrame({'produkt':['B','A','C'],'cena':[20.0,10.0,None]})
        original=prodeje.copy();lookup=cenik.copy()
        joined=function(2,'overene_ceny')(prodeje,cenik)
        joined['cas']=pd.array(['2026-02-01 08:00','2026-02-01 12:00','2026-02-03 00:00','2026-02-04 08:00'],dtype='datetime64[us]')
        joined['trzba']=joined['kusy']*joined['cena']
        timed=function(3,'nastav_casovy_index')(joined,'cas')
        result=function(4,'denni_soucty')(timed['trzba'])
        expected=pd.Series([40.0,None,0.0,None],index=pd.date_range('2026-02-01','2026-02-04',freq='D',name='cas').as_unit('us'),name='trzba')
        assert_series_equal(result,expected);assert_frame_equal(prodeje,original);assert_frame_equal(cenik,lookup)

    def test_output_frequency_and_empty_column_metadata_are_not_data_changes(self):
        import pandas as pd
        from dilna_check.pandas_tools import equivalent
        s=pd.Series([1.0,2.0],index=pd.date_range('2026-02-01','2026-02-02',freq='D',name='cas').as_unit('us'),name='X')
        other=s.copy();other.index=pd.DatetimeIndex(s.index.to_numpy(),name='cas')
        self.assertIsNone(other.index.freq)
        self.assertTrue(equivalent(other,s));self.assertFalse(equivalent(other,s,exact=True))
        wrong=other.copy();wrong.iloc[0]=9.0;self.assertFalse(equivalent(wrong,s))
        wrong=other.rename_axis('jiny_cas');self.assertFalse(equivalent(wrong,s))
        a=pd.DataFrame(index=range(3));b=pd.DataFrame(index=range(3),columns=pd.Index([],dtype='str'))
        self.assertTrue(equivalent(a,b));self.assertFalse(equivalent(a,b,exact=True))
        self.assertFalse(equivalent(a.head(2),b))

    def test_all_five_teaching_snippets_execute_with_declared_context(self):
        import pandas as pd
        count=0
        for lid in IDS:
            for code in re.findall(r'```python\n(.*?)```',(BASE/lid/'lesson.md').read_text('utf-8'),re.S):
                namespace={'pd':pd,'prvni':pd.DataFrame({'A':[1.0]}),'druha':pd.DataFrame({'A':[2.0]}),
                    'prodeje':pd.DataFrame({'produkt':['A'],'kusy':[2]}),'cenik':pd.DataFrame({'produkt':['A'],'cena':[10.0]}),
                    'tabulka':pd.DataFrame({'cas':pd.array(['2026-02-02','2026-02-01'],dtype='datetime64[us]'),'hodnota':[2.0,1.0]}),
                    'serie':pd.Series([1.0],index=pd.DatetimeIndex(['2026-02-01'],name='cas').as_unit('us'),dtype='float64')}
                with self.subTest(lesson=lid,code=code):exec(code,namespace);count+=1
        self.assertEqual(count,5)


if __name__=='__main__':unittest.main()
