"""Pandas 1–5: odlišné správné postupy, typické chyby, mutace a vlastní CSV."""
import ast
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT/'lib'))
from server.checker import run_check
from server.content import lesson_view, solution_view
from tools.setup_env import wanted

BASE = ROOT/'courses/pandas/lessons'
IDS = ['01-series-a-popisky', '02-vypocty-se-series', '03-vyber-loc-a-iloc',
       '04-prvni-dataframe', '05-csv-a-prvni-pruzkum']


class PandasIntroTest(unittest.TestCase):
    def variants(self, lesson, variants):
        for task, (wrong, correct) in enumerate(variants, 1):
            directory = BASE/IDS[lesson]
            if task > 1:
                directory = directory/'tasks'/f'task-{task}'
            source = (directory/'solution.py').read_text('utf-8')
            function = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef))
            for expected, bodies in [(False, wrong), (True, correct)]:
                for body in bodies:
                    lines = source.splitlines()
                    lines[function.body[0].lineno-1:function.end_lineno] = ['    '+line for line in body.splitlines()]
                    code = '\n'.join(lines)+'\n'
                    self.assertNotEqual(code, source)
                    with self.subTest(lesson=lesson+1, task=task, expected=expected, body=body), tempfile.TemporaryDirectory() as temp:
                        result = run_check(directory, code, ROOT/'lib', Path(temp))
                        self.assertNotIn('error', result, result)
                        self.assertEqual(result['ok'], expected, result)

    def test_series_labels_names_missing_and_input_mutation(self):
        self.variants(0, [
            (['return pd.Series(hodnoty, name=nazev, dtype="float64")',
              'return pd.Series(hodnoty, index=mista, name="teplota", dtype="float64")'],
             ['return pd.Series(data=hodnoty, dtype=float, name=nazev, index=mista)']),
            (['return pd.Series(list(data.values()), name=nazev, dtype="float64")'],
             ['return pd.Series(list(data.values()), index=list(data), name=nazev, dtype=float)']),
            (['serie.name = nazev\nreturn serie'],
             ['vysledek = serie.copy()\nvysledek.name = nazev\nreturn vysledek']),
            (['return list(serie.index)'], ['return list(serie)']),
            (['return serie.count()', 'return True'], ['return serie.size']),
        ])

    def test_arithmetic_alignment_missing_and_float_precision(self):
        self.variants(1, [
            (['return ceny_kc * kurz', 'return (ceny_kc / kurz).round(2)'],
             ['return ceny_kc.div(kurz)']),
            (['return pd.Series(ceny.to_numpy() * pocty.to_numpy(), index=ceny.index, name="trzba").sort_index()'],
             ['return ceny.mul(pocty).rename("trzba").sort_index()']),
            (['return {"soucet": serie.sum(), "prumer": serie.sum() / len(serie) if len(serie) else 0}'],
             ['return {"prumer": serie.mean(skipna=True), "soucet": serie.sum(skipna=True)}']),
            (['return serie - serie.median()'], ['return serie.sub(serie.mean())']),
            (['return serie * bonus'], ['return serie.add(bonus)']),
        ])

    def test_loc_iloc_order_repeated_labels_and_empty_selection(self):
        self.variants(2, [
            (['return serie.iloc[popisky]', 'return serie.loc[popisky].sort_index()'],
             ['return serie.reindex(popisky)']),
            (['return serie.loc[zacatek:konec]'], ['return serie.iloc[slice(zacatek, konec)]']),
            (['return serie.loc[pozice]'], ['return serie.take(pozice)']),
            (['return serie.rename(index=zmeny).sort_index()'],
             ['vysledek = serie.copy()\nvysledek.index = [zmeny.get(k, k) for k in serie.index]\nreturn vysledek']),
            (['return serie.sort_values()'], ['return serie.loc[sorted(serie.index)]']),
        ])

    def test_dataframe_columns_records_empty_shapes_and_input_mutation(self):
        self.variants(3, [
            (['return pd.DataFrame(data).T'], ['return pd.DataFrame.from_dict(data)']),
            (['return pd.DataFrame(zaznamy)'], ['return pd.DataFrame.from_records(zaznamy, columns=sloupce)']),
            (['return pd.DataFrame(data)'], ['return pd.DataFrame(data).set_axis(popisky, axis=0)']),
            (['return tabulka.head()', 'tabulka.drop(tabulka.index[pocet:], inplace=True)\nreturn tabulka'],
             ['return tabulka.iloc[:pocet]']),
            (['return (tabulka.shape[1], tabulka.shape[0])'], ['return (len(tabulka.index), len(tabulka.columns))']),
        ])

    def test_csv_format_codes_multiline_and_readonly_sources(self):
        self.variants(4, [
            (['return pd.read_csv(cesta, sep=";", encoding="utf-8")',
              'df = pd.read_csv(cesta, sep=";", decimal=",", encoding="utf-8")\nfrom pathlib import Path\nPath(cesta).write_text("přepsáno", encoding="utf-8")\nreturn df'],
             ['return pd.read_csv(cesta, delimiter=";", decimal=",", encoding="utf8")']),
            (['return pd.read_csv(cesta, sep=";", encoding="utf-8")'],
             ['return pd.read_csv(cesta, encoding="utf8", decimal=".")']),
            (['return pd.read_csv(cesta, sep=";", decimal=",", encoding="utf-8")'],
             ['return pd.read_csv(cesta, delimiter=";", decimal=",", encoding="utf8", names=["misto", "hodnota"], header=None)']),
            (['return pd.read_csv(cesta, sep=";", encoding="utf-8")'],
             ['return pd.read_csv(cesta, delimiter=";", encoding="utf8", dtype={"kod": str})']),
            (['from pathlib import Path\nreturn len(Path(cesta).read_text(encoding="utf-8").splitlines()) - 1'],
             ['return pd.read_csv(cesta, sep=";", decimal=",", encoding="utf8").shape[0]']),
        ])

    def test_pandas_comparison_contract(self):
        import pandas as pd
        from dilna_check.pandas_tools import equivalent
        expected = pd.Series([1.0, None], index=['A', 'B'], name='mereni')
        self.assertTrue(equivalent(expected.copy(), expected))
        self.assertTrue(equivalent(pd.Series([], index=[], dtype=float), pd.Series({}, dtype=float)))
        for wrong in [expected.rename('jine'), expected.reset_index(drop=True), expected.astype('Float64'), expected.iloc[::-1]]:
            self.assertFalse(equivalent(wrong, expected))
        self.assertFalse(equivalent(True, 1))
        self.assertFalse(equivalent([1.0], (1.0,)))
        self.assertTrue(equivalent([float('nan'), 1.0+1e-14], [float('nan'), 1.0]))
        self.assertFalse(equivalent([1.0+1e-14], [1.0], exact=True))

    def test_metadata_solutions_and_independent_csv_resources(self):
        course = json.loads((BASE.parent/'course.json').read_text('utf-8'))
        self.assertEqual(course['modules'][0]['lessons'], IDS)
        self.assertEqual(course['requires_packages'], wanted('pandas'))
        for lid in IDS:
            view = lesson_view(ROOT/'courses', 'pandas', lid)
            self.assertTrue(view['has_solution'])
            self.assertEqual(len(view['examples']), 2)
            self.assertEqual(len(view['tasks']), 4)
            for task in range(1, 6):
                d = BASE/lid if task == 1 else BASE/lid/'tasks'/f'task-{task}'
                self.assertIn('# %%', (d/'exercise.py').read_text('utf-8'))
                self.assertEqual(solution_view(ROOT/'courses', 'pandas', lid, f'task-{task}')['code'],
                                 (d/'solution.py').read_text('utf-8'))
        for task, file in [(2,'cenik.csv'), (3,'bez-hlavicky.csv'), (4,'identifikatory.csv'), (5,'mereni.csv')]:
            d = BASE/IDS[4]
            self.assertEqual((d/'files'/file).read_bytes(), (d/'tasks'/f'task-{task}'/'files'/file).read_bytes())

    def test_all_twenty_five_solution_demos_run_with_own_files(self):
        for lid in IDS:
            for task in range(1, 6):
                d = BASE/lid if task == 1 else BASE/lid/'tasks'/f'task-{task}'
                with self.subTest(lesson=lid, task=task), tempfile.TemporaryDirectory() as folder:
                    target = Path(folder)
                    if (d/'files').exists():
                        shutil.copytree(d/'files', target, dirs_exist_ok=True)
                    code = target/'reseni.py'
                    shutil.copyfile(d/'solution.py', code)
                    result = subprocess.run([sys.executable, '-X', 'utf8', str(code)], cwd=target,
                                            capture_output=True, text=True, timeout=15)
                    self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
                    self.assertTrue(result.stdout.strip())


if __name__ == '__main__':
    unittest.main()
