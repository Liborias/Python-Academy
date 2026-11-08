"""Pandas 31–35: skutečné soubory, jiné postupy, zachované kódy a měsíční projekt."""
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
IDS=['31-excel-a-textove-kody','32-export-csv-a-overeni','33-export-excel-a-vice-listu','34-opakovatelny-analyticky-postup','35-projekt-mesicni-prehled']


class PandasFilesTest(unittest.TestCase):
    def variants(self,lesson,variants):
        for task,(wrong,correct) in enumerate(variants,1):
            d=BASE/IDS[lesson] if task==1 else BASE/IDS[lesson]/'tasks'/f'task-{task}'
            source=(d/'solution.py').read_text();name=next(n.name for n in ast.parse(source).body if isinstance(n,ast.FunctionDef))
            self.try_bodies(d,name,wrong,correct)

    def try_bodies(self,d,name,wrong,correct):
        source=(d/'solution.py').read_text();fn=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name==name)
        for expected,bodies in [(False,wrong),(True,correct)]:
            for body in bodies:
                lines=source.splitlines();lines[fn.body[0].lineno-1:fn.end_lineno]=['    '+line for line in body.splitlines()]
                code='\n'.join(lines)+'\n';self.assertNotEqual(code,source)
                with self.subTest(function=name,body=body,expected=expected),tempfile.TemporaryDirectory() as temp:
                    report=run_check(d,code,ROOT/'lib',Path(temp))
                    self.assertNotIn('error',report,report);self.assertEqual(report['ok'],expected,report)

    def test_read_excel_sheets_headers_types_zeroes_na_and_empty(self):
        dtype='{"kod":"str","nazev":"str","cena":"float64"}'
        self.variants(0,[
            ([f'return pd.read_excel(cesta,engine="openpyxl",keep_default_na=False,dtype={dtype})',f'return pd.read_excel(cesta,sheet_name=list,engine="openpyxl",dtype={dtype})'],
             [f'return pd.read_excel(io=cesta,engine="openpyxl",sheet_name=list,keep_default_na=False,dtype={dtype})']),
            (['with pd.ExcelFile(cesta,engine="openpyxl") as x:\n    return sorted(x.sheet_names)'],
             ['with pd.ExcelFile(cesta,engine="openpyxl") as x:\n    return list(x.sheet_names)']),
            (['return pd.read_excel(cesta,sheet_name=list,engine="openpyxl",usecols=["kod","nazev"],keep_default_na=False,dtype="str")'],
             ['return pd.read_excel(cesta,sheet_name=list,engine="openpyxl",keep_default_na=False,dtype={"kod":"str","nazev":"str"}).loc[:,["kod","nazev"]]']),
            (['return pd.read_excel(cesta,sheet_name=list,engine="openpyxl",keep_default_na=False,dtype={"kod":"str","cena":"float64"})'],
             ['return pd.read_excel(cesta,sheet_name=list,header=1,engine="openpyxl",keep_default_na=False,dtype={"kod":"str","cena":"float64"})']),
            (['return {"cenik":pd.read_excel(cesta,sheet_name="Ceník"),"prodeje":pd.read_excel(cesta,sheet_name="Prodeje")}'],
             [f'return {{"cenik":pd.read_excel(cesta,sheet_name="Ceník",engine="openpyxl",keep_default_na=False,dtype={dtype}),"prodeje":pd.read_excel(cesta,sheet_name="Prodeje",engine="openpyxl",keep_default_na=False,dtype={{"kod":"str","kusy":"int64"}})}}']),
        ])

    def test_csv_bytes_quoting_column_order_bom_and_round_trip(self):
        self.variants(1,[
            (['tabulka.to_csv(cesta,sep=";",decimal=",",encoding="utf-8");return Path(cesta)','tabulka.to_csv(cesta,sep=";",encoding="utf-8",index=False);return Path(cesta)'],
             ['tabulka.to_csv(path_or_buf=cesta,encoding="utf-8",sep=";",decimal=",",index=False);return Path(cesta)']),
            (['return ";".join(tabulka.columns)+"\n"+"\n".join(";".join(map(str,row)) for row in tabulka.itertuples(index=False,name=None))'],
             ['return tabulka.to_csv(None,sep=";",decimal=",",index=False,quoting=1)']),
            (['tabulka.to_csv(cesta,sep=";",decimal=",",encoding="utf-8",index=False);return Path(cesta)'],
             ['tabulka.loc[:,sloupce].to_csv(cesta,index=False,sep=";",decimal=",",encoding="utf-8");return Path(cesta)']),
            (['tabulka.to_csv(cesta,index=False,sep=";",decimal=",",encoding="utf-8");return Path(cesta)'],
             ['Path(cesta).write_bytes(tabulka.to_csv(sep=";",decimal=",",index=False).encode("utf-8-sig"));return Path(cesta)']),
            (['return Path(cesta).exists()'],
             ['try:\n    loaded=pd.read_csv(cesta,sep=";",decimal=",",encoding="utf-8",keep_default_na=False,dtype={"kod":"str","nazev":"str","hodnota":"float64"})\n    pd.testing.assert_frame_equal(loaded,tabulka.reset_index(drop=True),rtol=1e-12,atol=1e-12,check_exact=False)\nexcept (AssertionError,ValueError):\n    return False\nreturn True']),
        ])

    def test_excel_exports_sheet_order_native_cell_types_and_verification(self):
        self.variants(2,[
            (['tabulka.to_excel(cesta,sheet_name=list,engine="openpyxl");return Path(cesta)','tabulka.to_csv(cesta,index=False);return Path(cesta)'],
             ['with pd.ExcelWriter(cesta,engine="openpyxl") as out:\n    tabulka.to_excel(out,index=False,sheet_name=list)\nreturn Path(cesta)']),
            (['cenik.to_excel(cesta,sheet_name="Ceník",index=False);prodeje.to_excel(cesta,sheet_name="Prodeje",index=False);return Path(cesta)'],
             ['with pd.ExcelWriter(cesta,engine="openpyxl") as x:\n    for name,data in [("Ceník",cenik),("Prodeje",prodeje)]:\n        data.to_excel(x,sheet_name=name,index=False)\nreturn Path(cesta)']),
            (['with pd.ExcelWriter(cesta,engine="openpyxl") as x:\n    for name in sorted(tabulky):\n        tabulky[name].to_excel(x,sheet_name=name,index=False)\nreturn Path(cesta)'],
             ['with pd.ExcelWriter(cesta,engine="openpyxl") as x:\n    for name in tabulky:\n        tabulky[name].to_excel(x,index=False,sheet_name=name)\nreturn Path(cesta)']),
            (['data=tabulka.copy();data["kod"]=data["kod"].replace("NA","0").astype(int);data.to_excel(cesta,sheet_name="Data",index=False);return Path(cesta)'],
             ['with pd.ExcelWriter(cesta,engine="openpyxl") as x:\n    tabulka.to_excel(x,index=False,sheet_name="Data")\nreturn Path(cesta)']),
            (['return Path(cesta).exists()'],
             ['try:\n    with pd.ExcelFile(cesta,engine="openpyxl") as x:\n        data=pd.read_excel(x,sheet_name=list,keep_default_na=False,dtype={"kod":"str","nazev":"str","cena":"float64"})\n    pd.testing.assert_frame_equal(data,tabulka.reset_index(drop=True),rtol=1e-12,atol=1e-12,check_exact=False)\nexcept (AssertionError,ValueError):\n    return False\nreturn True']),
        ])

    def test_pipeline_rules_multiple_files_duplicates_zeroes_and_real_export(self):
        self.variants(3,[
            (['data=pd.read_csv(cesta,sep=";",dtype="str");data=data[["misto","hodnota"]].copy();data["misto"]=data["misto"].str.strip().replace("",pd.NA);data["hodnota"]=pd.to_numeric(data["hodnota"].str.strip().str.replace(",",".",regex=False),errors="coerce");return data.dropna().reset_index(drop=True)'],
             ['data=pd.read_csv(cesta,sep=";",dtype="str",encoding="utf-8",keep_default_na=False);data=data.loc[:,["misto","hodnota"]].copy();data["misto"]=data["misto"].str.strip();data["hodnota"]=pd.to_numeric(data["hodnota"].str.strip().str.replace(",",".",regex=False),errors="coerce").astype("float64");return data.loc[(data["misto"]!="") & data["hodnota"].notna()].reset_index(drop=True)']),
            (['return tabulka.drop_duplicates().groupby("misto",as_index=False,sort=True).agg(pocet=("hodnota","size"),prumer=("hodnota","mean"))'],
             ['return tabulka.groupby(by="misto",sort=True).agg(pocet=("hodnota","count"),prumer=("hodnota","mean")).reset_index()']),
            (['return pd.concat([zpracuj_mereni(p) for p in cesty],ignore_index=True).drop_duplicates().reset_index(drop=True)'],
             ['frames=[]\nfor p in cesty:\n    frames.append(zpracuj_mereni(p))\nif len(frames)==0:\n    return pd.DataFrame({"misto":pd.Series(dtype="str"),"hodnota":pd.Series(dtype="float64")})\nreturn pd.concat(frames,ignore_index=True)']),
            (['return Path(cesta)'],
             ['Path(cesta).write_text(tabulka.to_csv(index=False,sep=";",decimal=","),encoding="utf-8");return Path(cesta)']),
            (['return souhrn_mist(zpracuj_mereni(vstup))'],
             ['report=souhrn_mist(zpracuj_mereni(vstup));Path(vystup).write_text(report.to_csv(index=False,sep=";",decimal=","),encoding="utf-8");return report']),
        ])

    def test_project_calendar_month_independent_sums_and_real_three_outputs(self):
        d=BASE/IDS[4]
        self.try_bodies(d,'vyber_mesic',[
            'start=pd.Timestamp(mesic+"-01");end=start+pd.Timedelta(days=30);return tabulka.loc[(tabulka["den"]>=start)&(tabulka["den"]<end)].copy()',
            'start=pd.Timestamp(mesic+"-01");end=start+pd.offsets.MonthBegin(1);return tabulka.loc[(tabulka["den"]>=start)&(tabulka["den"]<=end)].copy()'],
            ['return tabulka.loc[tabulka["den"].dt.strftime("%Y-%m")==mesic].copy()'])
        self.try_bodies(d,'prehled_mesice',[
            'data=vyber_mesic(tabulka,mesic).drop_duplicates();data["den"]=data["den"].dt.strftime("%Y-%m-%d").astype("str");return prehled_kavarny(data)'],
            ['data=vyber_mesic(tabulka,mesic);data=data.assign(den=data["den"].dt.strftime("%Y-%m-%d").astype("str"));return prehled_kavarny(data)'])
        source=(d/'solution.py').read_text();fn=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='uloz_report');body='\n'.join(line[4:] for line in source.splitlines()[fn.body[0].lineno-1:fn.end_lineno])
        self.try_bodies(d,'uloz_report',[body.replace('index=False','index=True'),body.replace('produkty["trzba"]','produkty["kusy"]')],
                        [body.replace('ax.bar(produkty["produkt"], produkty["trzba"])','ax.bar(produkty["produkt"], produkty["trzba"], color="purple", width=0.6)')])

    def test_metadata_scope_and_lazy_solutions(self):
        course=json.loads((BASE.parent/'course.json').read_text());self.assertEqual(course['modules'][6]['lessons'],IDS)
        for i,lid in enumerate(IDS):
            view=lesson_view(ROOT/'courses','pandas',lid)
            self.assertEqual((len(view['examples']),len(view['tasks']),len(view['quiz'])),(2,4,3) if i<4 else (0,0,5))
            self.assertTrue(view['download_files']);self.assertEqual(view['preview_images'],i==4)
            for n in range(1,6 if i<4 else 2):
                d=BASE/lid if n==1 else BASE/lid/'tasks'/f'task-{n}'
                self.assertEqual(solution_view(ROOT/'courses','pandas',lid,f'task-{n}')['code'],(d/'solution.py').read_text())

    def test_all_twenty_one_reference_demos_run_with_their_own_files(self):
        for i,lid in enumerate(IDS):
            for n in range(1,6 if i<4 else 2):
                d=BASE/lid if n==1 else BASE/lid/'tasks'/f'task-{n}'
                with self.subTest(lesson=lid,task=n),tempfile.TemporaryDirectory() as temp:
                    work=Path(temp);shutil.copytree(d/'files',work,dirs_exist_ok=True)
                    before={f.relative_to(work):f.read_bytes() for f in work.rglob('*') if f.is_file()}
                    result=subprocess.run([sys.executable,'-X','utf8',str(d/'solution.py')],cwd=work,env=dict(os.environ,PYTHONPATH=str(work),MPLBACKEND='Agg'),capture_output=True,text=True,timeout=20)
                    self.assertEqual(result.returncode,0,result.stdout+result.stderr);self.assertTrue(result.stdout.strip())
                    for path,value in before.items():self.assertEqual((work/path).read_bytes(),value)
                    if i==4:
                        self.assertIn('563.0',result.stdout);self.assertTrue((work/'vystupy/prehled.xlsx').exists())

    def test_all_five_teaching_snippets_execute_with_their_source_files(self):
        old=Path.cwd()
        try:
            for lid in IDS:
                with tempfile.TemporaryDirectory() as temp:
                    work=Path(temp);shutil.copytree(BASE/lid/'files',work,dirs_exist_ok=True);os.chdir(work)
                    snippets=re.findall(r'```python\n(.*?)```',(BASE/lid/'lesson.md').read_text(),re.S)
                    self.assertEqual(len(snippets),1)
                    for code in snippets:exec(code,{})
        finally:os.chdir(old)

    def test_provided_helpers_exactly_match_prior_function_bodies(self):
        def bodies(path):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(path.read_text()).body if isinstance(n,ast.FunctionDef)}
        helper=bodies(BASE/IDS[3]/'files/cisteni.py')
        self.assertEqual(helper['zpracuj_mereni'],bodies(BASE/IDS[3]/'solution.py')['zpracuj_mereni'])
        self.assertEqual(helper['souhrn_mist'],bodies(BASE/IDS[3]/'tasks/task-2/solution.py')['souhrn_mist'])
        for d in [BASE/IDS[3],*sorted((BASE/IDS[3]/'tasks').glob('task-*'))]:self.assertEqual((d/'files/cisteni.py').read_bytes(),(BASE/IDS[3]/'files/cisteni.py').read_bytes())
        old=bodies(BASE/'20-projekt-prehled-kavarny/solution.py');new=bodies(BASE/IDS[4]/'files/kavarna.py')
        self.assertEqual(new,old)

    def test_project_real_fixture_totals_and_two_different_months(self):
        import pandas as pd
        old=Path.cwd();module_path=str(BASE/IDS[4]/'files');sys.path.insert(0,module_path)
        try:
            with tempfile.TemporaryDirectory() as temp:
                work=Path(temp);shutil.copytree(BASE/IDS[4]/'files',work,dirs_exist_ok=True);os.chdir(work)
                namespace={'__name__':'student'};exec((BASE/IDS[4]/'solution.py').read_text(),namespace)
                df=pd.read_csv('prodeje.csv',sep=';',decimal=',',keep_default_na=False,dtype={'den':'str','produkt':'str','kusy':'int64','cena':'float64'});df['den']=pd.to_datetime(df['den']).astype('datetime64[us]');before=df.copy()
                feb=namespace['prehled_mesice'](df,'2026-02');march=namespace['prehled_mesice'](df,'2026-03')
                self.assertEqual(feb['celkem'],{'radky':6,'kusy':10,'trzba':563.0});self.assertEqual(feb['podle_dnu']['trzba'].tolist(),[270.,45.,248.])
                self.assertEqual(feb['podle_produktu']['trzba'].tolist(),[0.,135.,428.]);self.assertEqual(march['celkem'],{'radky':1,'kusy':1,'trzba':10.0})
                paths=namespace['uloz_report'](feb,Path('výstup/únor'));self.assertEqual(set(paths),{'csv','excel','graf'})
                pd.testing.assert_frame_equal(df,before)
        finally:os.chdir(old);sys.path.remove(module_path);sys.modules.pop('kavarna',None)


if __name__=='__main__':unittest.main()
