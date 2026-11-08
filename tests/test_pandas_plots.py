"""Pandas 26–30: skuteční artists, jiná řešení, nepozměněná data a exporty."""
import ast
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'lib'))
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'workspace/_run/_matplotlib'))
from server.checker import run_check
from server.content import lesson_view, solution_view
BASE=ROOT/'courses/pandas/lessons'
IDS=['26-figure-axes-a-popisky','27-carove-a-sloupcove-grafy','28-bodovy-graf-a-souvislosti','29-histogram-a-rozlozeni','30-ulozeni-grafu-do-png']


class PandasPlotsTest(unittest.TestCase):
    def variants(self, lesson, variants):
        for task,(wrong,correct) in enumerate(variants,1):
            d=BASE/IDS[lesson] if task==1 else BASE/IDS[lesson]/'tasks'/f'task-{task}'
            source=(d/'solution.py').read_text();fn=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef))
            for expected,bodies in [(False,wrong),(True,correct)]:
                for body in bodies:
                    lines=source.splitlines();lines[fn.body[0].lineno-1:fn.end_lineno]=['    '+line for line in body.splitlines()]
                    code='\n'.join(lines)+'\n';self.assertNotEqual(code,source)
                    with self.subTest(lesson=lesson+26,task=task,expected=expected,body=body),tempfile.TemporaryDirectory() as temp:
                        result=run_check(d,code,ROOT/'lib',Path(temp))
                        self.assertNotIn('error',result,result);self.assertEqual(result['ok'],expected,result)

    def test_figure_axes_titles_identity_ranges_and_row(self):
        self.variants(0,[
            (['return Figure(figsize=(6,4))','fig=Figure(figsize=(6,4));ax=fig.subplots();ax.set(title=titulek,xlabel=y_popisek,ylabel=x_popisek);return fig'],
             ['fig=Figure(figsize=(6,4));ax=fig.add_subplot(111);ax.set(title=titulek,xlabel=x_popisek,ylabel=y_popisek);return fig']),
            (['ax.clear();ax.set(title=titulek,xlabel=x_popisek,ylabel=y_popisek);return ax'],
             ['ax.set(title=titulek,xlabel=x_popisek,ylabel=y_popisek);return ax']),
            (['ax.legend(["Ráno","Večer"]);return ax','return ax','ax.lines[0].set_ydata([0,0]);ax.legend();return ax'],
             ['handles,labels=ax.get_legend_handles_labels();ax.legend(handles=handles,labels=labels);return ax']),
            (['ax.set_ylim(0,100);return ax','ax.set_xlim(minimum,maximum);return ax'],
             ['ax.set(ylim=(minimum,maximum));return ax']),
            (['fig=Figure(figsize=(8,3));fig.subplots(2,1);fig.suptitle(titulek);return fig'],
             ['fig=Figure(figsize=(8,3));fig.add_subplot(121);fig.add_subplot(122);fig.suptitle(titulek);return fig']),
        ])

    def test_lines_gaps_categories_zero_baselines_and_order(self):
        def base(body,title,x,y):
            return 'fig=Figure();ax=fig.subplots()\n'+body+'\n'+f'ax.set(title={title!r},xlabel={x!r},ylabel={y!r});return fig'
        self.variants(1,[
            ([base('ax.plot(range(len(dny)),hodnoty,marker="o")','Vývoj měření','Den','Hodnota'),base('ax.plot(dny,[0 if v!=v else v for v in hodnoty],marker="o")','Vývoj měření','Den','Hodnota')],
             [base('ax.plot(dny,hodnoty,color="purple",marker="o")','Vývoj měření','Den','Hodnota')]),
            ([base('ax.bar(nazvy,pocty);ax.set_ylim(bottom=1)','Porovnání kategorií','Kategorie','Počet')],
             [base('ax.bar(nazvy,pocty,width=0.6,color="orange");ax.set_ylim(bottom=0)','Porovnání kategorií','Kategorie','Počet')]),
            ([base('ax.plot(dny,prvni,marker="o",label="Ráno");ax.plot(dny,druha,marker="s",label="Večer")','Dvě měření','Den','Teplota (°C)')],
             [base('ax.plot(dny,prvni,label="Ráno",marker="o",color="black");ax.plot(dny,druha,label="Večer",marker="s",color="orange");ax.legend()','Dvě měření','Den','Teplota (°C)')]),
            ([base('ax.barh(nazvy,hodnoty);ax.set_xlim(left=0)','Kategorie shora','Počet','Kategorie')],
             [base('ax.barh(nazvy,hodnoty,height=0.6);ax.set_ylim(ax.get_ylim()[::-1]);ax.set_xlim(left=0)','Kategorie shora','Počet','Kategorie')]),
            ([base('ax.plot(tabulka["den"],tabulka["hodnota"],marker="o")','Seřazený vývoj','Den','Hodnota'),base('data=tabulka.sort_values("den");ax.plot(data["den"],data["hodnota"],marker="o")','Seřazený vývoj','Den','Hodnota'),base('tabulka.sort_values("den",inplace=True);ax.plot(tabulka["den"],tabulka["hodnota"],marker="o")','Seřazený vývoj','Den','Hodnota')],
             [base('data=tabulka.sort_values(by="den",kind="mergesort");ax.plot(data["den"],data["hodnota"],marker="o")','Seřazený vývoj','Den','Hodnota')]),
        ])

    def test_scatter_pairs_groups_aspect_and_area(self):
        self.variants(2,[
            (['fig=Figure();ax=fig.subplots();ax.plot(x,y);ax.set(title="Cvičná měření",xlabel="Doba učení (h)",ylabel="Body v kvízu");return fig'],
             ['fig=Figure();ax=fig.subplots();ax.scatter(x=x,y=y,marker="s",color="purple");ax.set(title="Cvičná měření",xlabel="Doba učení (h)",ylabel="Body v kvízu");return fig']),
            (['return tabulka.dropna()[["x","y"]]','return tabulka[["x","y"]].fillna(0)'],
             ['return tabulka.loc[tabulka["x"].notna() & tabulka["y"].notna(),["x","y"]].copy()']),
            (['fig=Figure();ax=fig.subplots();ax.scatter(list(prvni["x"])+list(druha["x"]),list(prvni["y"])+list(druha["y"]));ax.set(title="Dvě skupiny",xlabel="x",ylabel="y");return fig'],
             ['fig=Figure();ax=fig.subplots();ax.scatter(prvni["x"],prvni["y"],label="Skupina A",marker="s");ax.scatter(druha["x"],druha["y"],label="Skupina B",marker="x");ax.legend();ax.set(title="Dvě skupiny",xlabel="x",ylabel="y");return fig']),
            (['fig=Figure();ax=fig.subplots();ax.scatter(x,y);ax.set(xlim=(minimum,maximum),ylim=(minimum,maximum),title="Stejné měřítko",xlabel="Východ (m)",ylabel="Sever (m)");return fig'],
             ['fig=Figure();ax=fig.subplots();ax.scatter(x,y);ax.set(xlim=(minimum,maximum),ylim=(minimum,maximum),aspect=1,title="Stejné měřítko",xlabel="Východ (m)",ylabel="Sever (m)");return fig']),
            (['fig=Figure();ax=fig.subplots();ax.scatter(x,y,s=[v*v for v in velikosti]);ax.set(title="Velikost značky jako údaj",xlabel="Čas (min)",ylabel="Výkon (body)");return fig'],
             ['fig=Figure();ax=fig.subplots();ax.scatter(x=x,y=y,s=velikosti,marker="s");ax.set(title="Velikost značky jako údaj",xlabel="Čas (min)",ylabel="Výkon (body)");return fig']),
        ])

    def test_histogram_edges_counts_density_and_common_scale(self):
        self.variants(3,[
            (['fig=Figure();ax=fig.subplots();ax.hist(hodnoty,bins=len(hranice)-1);ax.set(title="Rozložení dob",xlabel="Doba (min)",ylabel="Četnost");return fig'],
             ['fig=Figure();ax=fig.subplots();ax.hist(x=hodnoty,bins=hranice,color="orange");ax.set(title="Rozložení dob",xlabel="Doba (min)",ylabel="Četnost");return fig']),
            (['return [sum(lo<=v<hi for v in hodnoty) for lo,hi in zip(hranice,hranice[1:])]'],
             ['return [sum(lo<=v and (v<hi or (i==len(hranice)-2 and v==hi)) for v in hodnoty) for i,(lo,hi) in enumerate(zip(hranice,hranice[1:]))]']),
            (['return serie.fillna(0)','return serie[serie.notna() & (serie!=0)]'],
             ['return serie.loc[serie.notna()].copy()']),
            (['fig=Figure();ax=fig.subplots();ax.hist(hodnoty,bins=hranice);ax.set(title="Hustota dob",xlabel="Doba (min)",ylabel="Hustota (1/min)");return fig'],
             ['import numpy as np\ncounts,edges=np.histogram(hodnoty,bins=hranice);width=np.diff(edges);fig=Figure();ax=fig.subplots();ax.bar(edges[:-1],counts/(counts.sum()*width),width=width,align="edge");ax.set(title="Hustota dob",xlabel="Doba (min)",ylabel="Hustota (1/min)");return fig']),
            (['fig=Figure();axes=fig.subplots(1,2);axes[0].hist(prvni,bins=hranice);axes[1].hist(druha,bins=hranice);axes[0].set(title="Ráno",xlabel="Doba (min)",ylabel="Četnost");axes[1].set(title="Večer",xlabel="Doba (min)",ylabel="Četnost");fig.suptitle("Dvě rozložení");return fig'],
             ['fig=Figure();a,b=fig.subplots(1,2,sharey=True);a.hist(prvni,bins=hranice,color="orange");b.hist(druha,bins=hranice,color="purple");a.set(title="Ráno",xlabel="Doba (min)",ylabel="Četnost");b.set(title="Večer",xlabel="Doba (min)",ylabel="Četnost");fig.suptitle("Dvě rozložení");return fig']),
        ])

    def test_actual_exports_target_figure_dimensions_alpha_tight_and_paths(self):
        self.variants(4,[
            (['from matplotlib import pyplot as plt\nplt.savefig(cesta,dpi=dpi);return Path(cesta)','fig.set_dpi(dpi);fig.savefig(cesta,format="png");return Path(cesta)'],
             ['fig.canvas.print_figure(cesta,format="png",dpi=dpi);return Path(cesta)']),
            (['fig.set_dpi(sirka);return fig'],
             ['fig.set_figwidth(sirka);fig.set_figheight(vyska);return fig']),
            (['fig.savefig(cesta,format="png",dpi=100);return Path(cesta)'],
             ['fig.savefig(fname=cesta,dpi=100,format="png",transparent=True);return Path(cesta)']),
            (['fig.savefig(cesta,format="png",dpi=100);return Path(cesta)'],
             ['fig.canvas.print_figure(cesta,format="png",dpi=100,bbox_inches="tight",pad_inches=0.1);return Path(cesta)']),
            (['slozka=Path(slozka);slozka.mkdir(parents=True,exist_ok=True);a=slozka/"nahled.png";b=slozka/"tisk.png";fig.savefig(a,dpi=100);fig.savefig(b,dpi=100);return a,b'],
             ['p=Path(slozka);p.mkdir(exist_ok=True,parents=True);files=(p/"nahled.png",p/"tisk.png")\nfor name,dpi in zip(files,[100,200]):\n    fig.savefig(name,dpi=dpi,format="png")\nreturn files']),
        ])

    def test_metadata_and_all_solutions(self):
        c=json.loads((BASE.parent/'course.json').read_text())
        self.assertEqual(c['modules'][5]['lessons'],IDS)
        for lid in IDS:
            view=lesson_view(ROOT/'courses','pandas',lid)
            self.assertEqual((len(view['examples']),len(view['tasks']),len(view['quiz'])),(2,4,3))
            self.assertTrue(view['preview_images'])
            for task in range(1,6):
                d=BASE/lid if task==1 else BASE/lid/'tasks'/f'task-{task}'
                self.assertEqual(solution_view(ROOT/'courses','pandas',lid,f'task-{task}')['code'],(d/'solution.py').read_text())

    def test_every_reference_demo_creates_real_png_as_standalone_script(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as cache:
            env=dict(os.environ,MPLBACKEND='Agg',MPLCONFIGDIR=cache)
            for lid in IDS:
                for task in range(1,6):
                    d=BASE/lid if task==1 else BASE/lid/'tasks'/f'task-{task}'
                    with self.subTest(lesson=lid,task=task),tempfile.TemporaryDirectory() as temp:
                        result=subprocess.run([sys.executable,'-X','utf8',str(d/'solution.py')],cwd=temp,env=env,capture_output=True,text=True,timeout=15)
                        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
                        files=list(Path(temp).rglob('*.png'));self.assertTrue(files)
                        for path in files:
                            with Image.open(path) as image:
                                image.load();self.assertEqual(image.format,'PNG');self.assertGreater(image.width,100)

    def test_all_five_teaching_snippets_render_and_histogram_numbers_match(self):
        from PIL import Image
        old=Path.cwd()
        try:
            with tempfile.TemporaryDirectory() as temp:
                os.chdir(temp);count=0
                for lid in IDS:
                    for code in re.findall(r'```python\n(.*?)```',(BASE/lid/'lesson.md').read_text(),re.S):
                        namespace={};exec(code,namespace);count+=1
                        files=list(Path(temp).glob('*.png'));self.assertTrue(files)
                        if lid==IDS[3]:self.assertEqual(namespace['pocty'].tolist(),[2.,3.,2.])
                        for path in files:
                            with Image.open(path) as image:self.assertEqual(image.format,'PNG')
                            path.unlink()
                self.assertEqual(count,5)
        finally:os.chdir(old)

    def test_data_preparation_then_plot_preserves_real_pairs_and_nan_gaps(self):
        import pandas as pd
        from dilna_check.matplotlib_tools import near
        def function(lesson,task,name):
            d=BASE/IDS[lesson] if task==1 else BASE/IDS[lesson]/'tasks'/f'task-{task}'
            ns={'__name__':'student'};exec((d/'solution.py').read_text(),ns);return ns[name]
        data=pd.DataFrame({'x':[3.,None,1.,0.],'y':[8.,2.,4.,0.]},index=['a','b','c','d']);before=data.copy()
        pairs=function(2,2,'vyber_dvojice')(data)
        fig=function(2,1,'bodovy_graf')(pairs['x'].tolist(),pairs['y'].tolist())
        self.assertTrue(near(fig.axes[0].collections[0].get_offsets(),[[3,8],[1,4],[0,0]]))
        pd.testing.assert_frame_equal(data,before)
        line=function(1,1,'vyvoj')([1,3,7],[8,float('nan'),9]).axes[0].lines[0]
        self.assertTrue(near(line.get_xdata(),[1,3,7]));self.assertTrue(near(line.get_ydata(),[8,float('nan'),9]))


if __name__=='__main__':unittest.main()
