"""Veřejné testy porovnání; lze použít dodanou funkci i python -m unittest."""
from copy import deepcopy
import importlib
import os
import unittest
import pandas as pd
POROVNEJ = None
DEFAULT_MODUL = "reseni"

def vzor():
    return {"stanice":pd.DataFrame({"kod":["001","NA"],"pocet":[2,1],"prumer":[1.5,-2.0]})}

class TestOvereni(unittest.TestCase):
    def porovnej(self,a,b):
        function = POROVNEJ or getattr(importlib.import_module(os.environ.get("DILNA_MODUL",DEFAULT_MODUL)),"over_prehled")
        before_a,before_b=deepcopy(a),deepcopy(b)
        result=function(a,b)
        for key in before_a:pd.testing.assert_frame_equal(a[key],before_a[key])
        for key in before_b:pd.testing.assert_frame_equal(b[key],before_b[key])
        return result
    def test_shoda(self):self.assertTrue(self.porovnej(vzor(),vzor()))
    def test_cislo(self):
        a=vzor();b=vzor();b["stanice"].loc[0,"prumer"]+=0.01
        self.assertFalse(self.porovnej(a,b))
    def test_klic(self):self.assertFalse(self.porovnej(vzor(),{}))
    def test_popisky(self):
        a=vzor();b=vzor();b["stanice"]["kod"]=["NA","001"]
        self.assertFalse(self.porovnej(a,b))
    def test_typ(self):
        a=vzor();b=vzor();b["stanice"]["pocet"]=b["stanice"]["pocet"].astype("float64")
        self.assertFalse(self.porovnej(a,b))
    def test_poradi(self):
        a=vzor();b={"stanice":vzor()["stanice"][["prumer","pocet","kod"]]}
        self.assertFalse(self.porovnej(a,b))
    def test_prazdne(self):self.assertTrue(self.porovnej({"x":vzor()["stanice"].head(0)},{"x":vzor()["stanice"].head(0)}))
    def test_tolerance(self):
        a=vzor();b=vzor();b["stanice"].loc[0,"prumer"]+=1e-13
        self.assertTrue(self.porovnej(a,b))

def spust_testy(function):
    global POROVNEJ
    before=POROVNEJ;POROVNEJ=function
    try:return unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(TestOvereni)).wasSuccessful()
    finally:POROVNEJ=before
