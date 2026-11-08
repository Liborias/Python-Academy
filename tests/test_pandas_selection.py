"""Pandas 6–10: tvar výběru, masky, stabilní řazení, CoW a zachování vstupu."""
import ast
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.checker import run_check
from server.content import lesson_view, solution_view

BASE = ROOT/'courses/pandas/lessons'
IDS = ['06-sloupce-series-a-dataframe', '07-vyber-radku-a-sloupcu',
       '08-filtrovani-pomoci-masek', '09-razeni-podle-hodnot',
       '10-nove-sloupce-a-zmeny-pres-loc']


class PandasSelectionTest(unittest.TestCase):
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
                    with self.subTest(lesson=lesson+6, task=task, expected=expected, body=body), tempfile.TemporaryDirectory() as temp:
                        result = run_check(directory, code, ROOT/'lib', Path(temp))
                        self.assertNotIn('error', result, result)
                        self.assertEqual(result['ok'], expected, result)

    def test_columns_shape_order_names_and_empty_selection(self):
        self.variants(0, [
            (['return tabulka[[sloupec]]', 'return tabulka[sloupec].reset_index(drop=True)'],
             ['return tabulka.loc[:, sloupec]']),
            (['return tabulka[sorted(sloupce)]'], ['return tabulka.loc[:, sloupce]']),
            (['return tabulka[sloupec]'], ['return tabulka.loc[:, [sloupec]]']),
            (['return tabulka.rename(index=zmeny)', 'tabulka.rename(columns=zmeny, inplace=True)\nreturn tabulka'],
             ['v = tabulka.copy()\nv.columns = [zmeny.get(k, k) for k in v.columns]\nreturn v']),
            (['return tabulka.index.tolist()'], ['return list(tabulka)']),
        ])

    def test_two_axes_integer_labels_slices_row_series_and_scalar(self):
        self.variants(1, [
            (['return tabulka.iloc[radky, sloupce]'], ['return tabulka.reindex(index=radky, columns=sloupce)']),
            (['return tabulka.loc[radky_od:radky_do, sloupce_od:sloupce_do]'],
             ['return tabulka.iloc[slice(radky_od, radky_do), slice(sloupce_od, sloupce_do)]']),
            (['return tabulka.loc[[popisek]]'], ['return tabulka.T[popisek]']),
            (['return tabulka.loc[pozice]'], ['return tabulka.take(pozice, axis=0)']),
            (['return tabulka.loc[[radek], [sloupec]]', 'return float(tabulka.loc[radek, sloupec])'],
             ['return tabulka.at[radek, sloupec]']),
        ])

    def test_masks_boundaries_or_membership_alignment_and_readonly_mask(self):
        self.variants(2, [
            (['return tabulka.loc[tabulka[sloupec] > minimum]'],
             ['return tabulka.loc[tabulka[sloupec].ge(minimum)]']),
            (['return tabulka.loc[(tabulka[sloupec] > dolni) & (tabulka[sloupec] < horni)]'],
             ['return tabulka.loc[tabulka[sloupec].between(dolni, horni, inclusive="both")]']),
            (['return tabulka.loc[(tabulka[sloupec_a] >= limit_a) & (tabulka[sloupec_b] >= limit_b)]'],
             ['a = tabulka[sloupec_a].ge(limit_a)\nb = tabulka[sloupec_b].ge(limit_b)\nreturn tabulka[a | b]']),
            (['return tabulka.loc[tabulka[sloupec] == povolene[0]]'],
             ['return tabulka.loc[tabulka[sloupec].isin(set(povolene))]']),
            (['return tabulka.loc[maska.tolist()]', 'maska.sort_index(inplace=True)\nreturn tabulka.loc[maska]'],
             ['return tabulka.loc[maska.reindex(tabulka.index)]']),
        ])

    def test_sorting_stability_nan_directions_keys_head_and_index(self):
        self.variants(3, [
            (['return tabulka.sort_index(ascending=vzestupne)',
              'return tabulka.sort_values(sloupec, ascending=True, kind="stable", na_position="last")',
              'return tabulka.sort_values(sloupec, ascending=vzestupne, kind="stable", na_position="first")',
              'return tabulka.sort_values(sloupec, ascending=vzestupne, na_position="last")'],
             ['return tabulka.sort_values(sloupec, ascending=vzestupne, kind="mergesort", na_position="last")']),
            (['return tabulka.sort_values([prvni, druhy], ascending=[True, True])'],
             ['return tabulka.sort_values([prvni, druhy], ascending=[True, False])']),
            (['return tabulka.head(pocet).sort_values("cena", kind="stable")',
              'return tabulka.dropna(subset=["cena"]).sort_values("cena", kind="stable").head(pocet)'],
             ['return tabulka.sort_values("cena", kind="mergesort", na_position="last").iloc[:pocet]']),
            (['return tabulka.reset_index()'],
             ['v = tabulka.copy()\nv.index = pd.RangeIndex(len(v))\nreturn v']),
            (['return serie.sort_values(ascending=vzestupne, kind="stable", na_position="last")',
              'return serie.sort_values(ascending=vzestupne, na_position="first")'],
             ['return serie.sort_values(ascending=vzestupne, kind="mergesort", na_position="first")']),
        ])

    def test_new_columns_loc_mutation_rounding_chaining_and_series_alignment(self):
        self.variants(4, [
            (['tabulka["trzba"] = tabulka["cena"] * tabulka["kusy"]\nreturn tabulka',
              'return tabulka.assign(trzba=tabulka["cena"] + tabulka["kusy"])'],
             ['return tabulka.assign(trzba=tabulka.cena * tabulka.kusy)']),
            (['v = tabulka.copy()\nv[cil] = (v[zdroj] / kurz).round(2)\nreturn v'],
             ['return tabulka.assign(**{cil: tabulka[zdroj].div(kurz)})']),
            (['tabulka.loc[radek, sloupec] = nova_hodnota\nreturn tabulka',
              'v = tabulka.copy()\nv[sloupec] = nova_hodnota\nreturn v'],
             ['v = tabulka.copy()\nv.at[radek, sloupec] = nova_hodnota\nreturn v']),
            (['v = tabulka.copy()\nv[sloupec] = v[sloupec] + bonus\nreturn v',
              'v = tabulka.copy()\nm = v[sloupec] > minimum\nv.loc[m, sloupec] = v.loc[m, sloupec] + bonus\nreturn v',
              'v = tabulka.copy()\nm = v[sloupec] >= minimum\nv[sloupec][m] = v[sloupec][m] + bonus\nreturn v'],
             ['v = tabulka.copy()\nv[sloupec] = v[sloupec].mask(v[sloupec].ge(minimum), v[sloupec] + bonus)\nreturn v']),
            (['v = tabulka.copy()\nv[sloupec] = hodnoty.tolist()\nreturn v'],
             ['return tabulka.assign(**{sloupec: hodnoty.reindex(tabulka.index)})']),
        ])

    def test_metadata_and_all_selected_reference_sources(self):
        course = json.loads((BASE.parent/'course.json').read_text('utf-8'))
        self.assertEqual(course['modules'][1]['lessons'], IDS)
        self.assertGreaterEqual(sum(len(m['lessons']) for m in course['modules']), 10)
        for lid in IDS:
            view = lesson_view(ROOT/'courses', 'pandas', lid)
            self.assertEqual(view['kind'], 'console')
            self.assertEqual(len(view['examples']), 2)
            self.assertEqual(len(view['tasks']), 4)
            self.assertEqual(len(view['quiz']), 3)
            for task in range(1,6):
                d = BASE/lid if task == 1 else BASE/lid/'tasks'/f'task-{task}'
                self.assertIn('# %%', (d/'exercise.py').read_text('utf-8'))
                self.assertEqual(solution_view(ROOT/'courses', 'pandas', lid, f'task-{task}')['code'],
                                 (d/'solution.py').read_text('utf-8'))

    def test_all_twenty_five_solution_demos_run_as_scripts(self):
        for lid in IDS:
            for task in range(1,6):
                d = BASE/lid if task == 1 else BASE/lid/'tasks'/f'task-{task}'
                with self.subTest(lesson=lid,task=task), tempfile.TemporaryDirectory() as temp:
                    result = subprocess.run([sys.executable, '-X', 'utf8', str(d/'solution.py')], cwd=temp,
                                            capture_output=True, text=True, timeout=15)
                    self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
                    self.assertTrue(result.stdout.strip())

    def test_real_pandas_copy_on_write_keeps_selection_and_original_independent(self):
        import pandas as pd
        from pandas.testing import assert_frame_equal
        namespace = {'__name__':'student'}
        exec((BASE/IDS[0]/'solution.py').read_text('utf-8'), namespace)
        df = pd.DataFrame({'cena':[10.0,20.0]}, index=['B','A'])
        original = df.copy()
        selected = namespace['vyber_sloupec'](df, 'cena')
        selected.loc['B'] = 999.0
        assert_frame_equal(df, original)
        # Ověří i skutečné chování samotné odvozené Series z ukázky 10.
        derived = df['cena']
        derived.loc['A'] = 111.0
        assert_frame_equal(df, original)
        df.loc['B', 'cena'] = 5.0
        self.assertEqual(derived.loc['B'], 10.0)


if __name__ == '__main__':
    unittest.main()
