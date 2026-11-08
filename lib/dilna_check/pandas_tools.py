"""Volitelné kontroly pandas. Importují se jen v lekcích, které pandas potřebují."""
from copy import deepcopy
import math
import numbers
from pathlib import Path
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal


def equivalent(actual, expected, *, exact=False):
    """Porovná i popisky, názvy, dtype a NaN; běžná aritmetika má malou toleranci."""
    try:
        if isinstance(expected, pd.DataFrame):
            assert_frame_equal(actual, expected, check_exact=exact, rtol=1e-12, atol=1e-12,
                               check_index_type=True if exact or len(expected.index) else False)
            return True
        if isinstance(expected, pd.Series):
            # U prázdného výsledku bez popisků mohou konstruktor slovníku a seznamu
            # odvodit různé typy prázdného indexu. Dtype hodnot a jména se kontrolují.
            assert_series_equal(actual, expected, check_exact=exact, rtol=1e-12, atol=1e-12,
                                check_index_type=True if exact or len(expected.index) else False)
            return True
    except (AssertionError, TypeError, ValueError):
        return False
    if isinstance(expected, (list, tuple)):
        return type(actual) is type(expected) and len(actual) == len(expected) and all(
            equivalent(a, b, exact=exact) for a, b in zip(actual, expected))
    if isinstance(expected, dict):
        return isinstance(actual, dict) and actual.keys() == expected.keys() and all(
            equivalent(actual[k], expected[k], exact=exact) for k in expected)
    if isinstance(expected, numbers.Integral) and not isinstance(expected, (bool, np.bool_)):
        return isinstance(actual, numbers.Integral) and not isinstance(actual, (bool, np.bool_)) and actual == expected
    if isinstance(expected, numbers.Real) and not isinstance(expected, (bool, np.bool_)):
        if not isinstance(actual, numbers.Real) or isinstance(actual, (bool, np.bool_)):
            return False
        if math.isnan(expected):
            return math.isnan(actual)
        return actual == expected if exact else math.isclose(actual, expected, rel_tol=1e-12, abs_tol=1e-12)
    if expected is pd.NA:
        return actual is pd.NA
    return type(actual) is type(expected) and actual == expected


def check_cases(checker, namespace, function, cases, *, readonly_files=()):
    """Ověří výsledky na čerstvých vstupech a jejich přesné zachování při volání."""
    files = {Path(path): Path(path).read_bytes() for path in readonly_files}
    for index, (args, expected) in enumerate(cases, 1):
        values = deepcopy(args)
        before = deepcopy(values)
        ok, actual = checker.call(namespace, function, values)
        hint = ('Vraťte výsledek podle zadání včetně typu, popisků, názvu a pořadí. '
                'Vstupní data neměňte.')
        if not ok:
            hint = f'Volání skončilo chybou {type(actual).__name__}: {actual}'
        checker.add(f'{function}: výsledek {index}', ok and equivalent(actual, expected), hint)
        checker.add(f'{function}: původní vstup {index}', equivalent(values, before, exact=True),
                    'Operace má vrátit výsledek bez změny předaného seznamu, slovníku, Series nebo DataFrame.')
    for path, before in files.items():
        try:
            unchanged = path.read_bytes() == before
        except OSError:
            unchanged = False
        checker.add(f'Původní soubor {path.name}', unchanged, 'Načtení CSV nesmí soubor přepsat ani odstranit.')
