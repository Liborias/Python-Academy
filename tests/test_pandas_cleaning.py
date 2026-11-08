"""Pandas 11–15: význam chybějících údajů, převody, kalendář, klíče a texty."""
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
IDS = ['11-chybejici-hodnoty', '12-cisla-a-datove-typy', '13-datumy-a-cas',
       '14-duplicity-a-jedinecne-hodnoty', '15-cisteni-textovych-sloupcu']


class PandasCleaningTest(unittest.TestCase):
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
                    with self.subTest(lesson=lesson+11, task=task, expected=expected, body=body), tempfile.TemporaryDirectory() as temp:
                        result = run_check(directory, code, ROOT/'lib', Path(temp))
                        self.assertNotIn('error', result, result)
                        self.assertEqual(result['ok'], expected, result)

    def test_missing_values_zeros_blanks_subsets_and_forward_order(self):
        self.variants(0, [
            (['return tabulka.count()', 'return tabulka.isna().sum(axis=1)'],
             ['return tabulka.isnull().sum(axis=0).astype("int64")']),
            (['return tabulka.fillna(0)', 'tabulka.fillna(vyplne, inplace=True)\nreturn tabulka'],
             ['v = tabulka.copy()\nfor k, hodnota in vyplne.items():\n    v[k] = v[k].fillna(hodnota)\nreturn v']),
            (['return tabulka.dropna()', 'return tabulka.dropna(subset=sloupce).reset_index(drop=True)'],
             ['return tabulka.loc[tabulka[sloupce].notna().all(axis=1)]']),
            (['return tabulka[sloupce].isna().all(axis=1)'],
             ['return tabulka[sloupce].isna().sum(axis=1) > 0']),
            (['return serie.bfill()', 'return serie.sort_index().ffill()'],
             ['v = serie.copy()\nposledni = None\nfor i in range(len(v)):\n    if pd.notna(v.iloc[i]):\n        posledni = v.iloc[i]\n    elif posledni is not None:\n        v.iloc[i] = posledni\nreturn v']),
        ])

    def test_numeric_coercion_comma_nullable_integer_and_invalid_mask(self):
        self.variants(1, [
            (['return serie.astype("float64")', 'return pd.to_numeric(serie, errors="coerce").fillna(0).astype("float64")'],
             ['return pd.to_numeric(serie, errors="coerce").astype(float)']),
            (['return pd.to_numeric(serie, errors="coerce").astype("float64")'],
             ['return pd.to_numeric(serie.str.replace(",", ".", regex=True), errors="coerce").astype(float)']),
            (['return serie.fillna(0).astype("int64")'],
             ['return pd.Series(pd.array(serie, dtype="Int64"), index=serie.index, name=serie.name)']),
            (['return tabulka.apply(pd.to_numeric, errors="coerce")',
              'for k, typ in typy.items():\n    tabulka[k] = tabulka[k].astype(typ)\nreturn tabulka'],
             ['v = tabulka.copy()\nfor k, typ in typy.items():\n    v[k] = v[k].astype(typ)\nreturn v']),
            (['return pd.to_numeric(serie, errors="coerce").isna()'],
             ['return pd.to_numeric(serie, errors="coerce").isna() & ~serie.isna()']),
        ])

    def test_dates_format_leap_year_time_unit_nat_year_and_inclusive_period(self):
        self.variants(2, [
            (['return pd.to_datetime(serie, format="%m.%d.%Y", errors="coerce").astype("datetime64[us]")',
              'return pd.to_datetime(serie, format="%d.%m.%Y").astype("datetime64[us]")'],
             ['return pd.Series(pd.to_datetime(serie, format="%d.%m.%Y", errors="coerce"), dtype="datetime64[us]", index=serie.index, name=serie.name)']),
            (['return pd.to_datetime(serie, format="%Y-%m-%d", errors="coerce").astype("datetime64[us]")'],
             ['return pd.Series(pd.to_datetime(serie, format="%Y-%m-%d %H:%M", errors="coerce"), dtype="datetime64[us]", index=serie.index, name=serie.name)']),
            (['return serie.dt.month.astype("Int64")'],
             ['return pd.Series(serie.dt.year, dtype="Int64", index=serie.index, name=serie.name)']),
            (['return tabulka.loc[(tabulka[sloupec] > pd.Timestamp(od)) & (tabulka[sloupec] < pd.Timestamp(do))]'],
             ['return tabulka.loc[tabulka[sloupec].between(pd.Timestamp(od), pd.Timestamp(do), inclusive="both")]']),
            (['return pd.to_datetime(serie, format="%d.%m.%Y", errors="coerce").isna()'],
             ['return serie.notna() & pd.to_datetime(serie, format="%d.%m.%Y", errors="coerce").isna()']),
        ])

    def test_duplicates_whole_rows_keys_positions_all_members_and_counts(self):
        self.variants(3, [
            (['return tabulka.drop_duplicates(subset=[tabulka.columns[0]])', 'return tabulka.drop_duplicates(keep="last")'],
             ['return tabulka.loc[~tabulka.duplicated(keep="first")]']),
            (['return tabulka.drop_duplicates(subset=klice, keep="first")',
              'return tabulka.sort_index().drop_duplicates(subset=klice, keep="last")'],
             ['return tabulka.loc[~tabulka.duplicated(subset=klice, keep="last")]']),
            (['return tabulka.duplicated(subset=klice)'],
             ['return tabulka.duplicated(klice, keep="first") | tabulka.duplicated(klice, keep="last")']),
            (['return sorted(set(serie))', 'return set(serie)'], ['return serie.unique().tolist()']),
            (['return serie.value_counts()'],
             ['return serie.groupby(serie, dropna=False, sort=False).size().rename("count")']),
        ])

    def test_text_whitespace_case_suffix_empty_missing_and_selected_column(self):
        self.variants(4, [
            (['return serie.str.strip()', 'return serie.str.strip().str.casefold()',
              'return serie.str.replace(" ", "", regex=False).str.lower()'],
             ['return serie.str.lower().str.strip()']),
            (['return serie.str.strip()', r'return serie.str.strip().str.replace(r"\s+", " ", regex=False)'],
             [r'return serie.str.replace(r"\s+", " ", regex=True).str.strip()']),
            (['return serie.str.strip().str.replace(pripona, "", regex=False).str.strip()',
              'return serie.str.strip().str.strip(pripona).str.strip()'],
             [r'import re'+'\n'+r'return serie.str.strip().str.replace(re.escape(pripona) + r"$", "", regex=True).str.strip()']),
            (['return serie.str.strip().fillna("")', 'return serie.str.strip().str.lower().replace("", float("nan"))'],
             ['v = serie.str.strip()\nreturn v.mask(v.eq(""), float("nan"))']),
            (['tabulka[sloupec] = tabulka[sloupec].str.strip().str.lower()\nreturn tabulka',
              'return tabulka.apply(lambda s: s.str.strip().str.lower() if s.dtype == "str" else s)'],
             ['return tabulka.assign(**{sloupec: tabulka[sloupec].str.lower().str.strip()})']),
        ])

    def test_metadata_and_all_selected_reference_sources(self):
        course = json.loads((BASE.parent/'course.json').read_text('utf-8'))
        self.assertEqual(course['modules'][2]['lessons'], IDS)
        self.assertGreaterEqual(sum(len(m['lessons']) for m in course['modules']), 15)
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
                with self.subTest(lesson=lid, task=task), tempfile.TemporaryDirectory() as temp:
                    result = subprocess.run([sys.executable, '-X', 'utf8', str(d/'solution.py')], cwd=temp,
                                            capture_output=True, text=True, timeout=15)
                    self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
                    self.assertTrue(result.stdout.strip())

    def test_cleaning_composition_preserves_source_and_classifies_real_errors(self):
        import pandas as pd
        from pandas.testing import assert_frame_equal, assert_series_equal
        def function(lesson, name, task=1):
            d = BASE/IDS[lesson]
            if task > 1:
                d = d/'tasks'/f'task-{task}'
            namespace = {'__name__':'student'}
            exec((d/'solution.py').read_text('utf-8'), namespace)
            return namespace[name]
        raw = pd.DataFrame({'misto':[' PRAHA ','Brno','  '], 'cena':['12,5','chyba',None],
                            'datum':['01.02.2026','31.02.2026',None]}, index=['C','A','B'])
        before = raw.copy()
        cleaned = raw.copy()
        cleaned['misto'] = function(4,'vycisti_text')(raw['misto'])
        cleaned['misto'] = function(4,'prazdne_na_chybejici',4)(cleaned['misto'])
        cleaned['cena'] = function(1,'preved_desetinnou_carku',2)(raw['cena'])
        cleaned['datum'] = function(2,'preved_data')(raw['datum'])
        assert_frame_equal(raw, before)
        assert_series_equal(cleaned['cena'], pd.Series([12.5,None,None],index=raw.index,name='cena'))
        self.assertEqual(cleaned.loc['C','datum'], pd.Timestamp('2026-02-01'))
        self.assertEqual(cleaned.loc['C','misto'], 'praha')
        self.assertTrue(pd.isna(cleaned.loc['B','misto']))
        counts = function(0,'chybejici_pocty')(cleaned)
        self.assertEqual(counts.to_dict(), {'misto':1,'cena':2,'datum':2})
        bad_dates = function(2,'chybne_datumy',5)(raw['datum'])
        self.assertEqual(bad_dates.tolist(), [False,True,False])


if __name__ == '__main__':
    unittest.main()
