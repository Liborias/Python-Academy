import copy
import io
import os
import sys
import unittest
sys.path.insert(0, os.getcwd())
from doprava import OsobniOdber, Kuryr
from expedice import Expedice
from dilna_check import check

c = check()
c.defines_class('TestExpedice')
ns = c.load()

def run_tests(cls):
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(cls)
    return unittest.TextTestRunner(stream=io.StringIO()).run(suite)

try:
    cls = ns['TestExpedice']
    c.add('Testovací třída používá unittest', isinstance(cls, type) and issubclass(cls, unittest.TestCase), 'Odvoďte TestExpedice z unittest.TestCase.')
    result = run_tests(cls)
    valid = result.wasSuccessful() and result.testsRun >= 4 and not result.skipped and not result.expectedFailures
    c.add('Alespoň čtyři vlastní testy projdou správným modelem', valid, 'Doplňte všechny čtyři scénáře, používejte vlastní objekty a testy nepřeskakujte.')
    original_init = Expedice.__init__
    original_change = Expedice.zmen_dopravu
    original_price = Kuryr.cena
    def early_change(self, nova):
        self._doprava = nova
        return nova.cena(self.balik)
    def ignored_change(self, nova):
        return nova.cena(self.balik)
    def missing_return(self, nova):
        original_change(self, nova)
    def cloned_parcel(self, balik, doprava):
        original_init(self, copy.copy(balik), doprava)
    def boundary_price(self, balik):
        if balik.hmotnost_g > self.limit_g:
            raise ValueError('Nad limitem')
        return 99 if balik.hmotnost_g < 5000 else 149
    def shifted_price(self, balik):
        if balik.hmotnost_g > self.limit_g:
            raise ValueError('Nad limitem')
        return 99 if balik.hmotnost_g <= 5001 else 149
    def rejected_limit(self, balik):
        if balik.hmotnost_g >= self.limit_g:
            raise ValueError('Na limitu chybně odmítnuto')
        return original_price(self, balik)
    mutants = [
        (OsobniOdber, 'cena', lambda self, balik: 10, 'chybný poplatek za osobní odběr'),
        (Kuryr, 'cena', boundary_price, 'chybnou cenu přesně při 5000 g'),
        (Kuryr, 'cena', shifted_price, 'chybnou cenu při 5001 g'),
        (Kuryr, 'cena', rejected_limit, 'odmítnutí přesně povoleného limitu 10000 g'),
        (Expedice, '__init__', cloned_parcel, 'kopii balíku místo původního objektu'),
        (Expedice, 'zmen_dopravu', ignored_change, 'neuloženou novou dopravu'),
        (Expedice, 'zmen_dopravu', missing_return, 'chybějící návratovou cenu po změně'),
        (Expedice, 'zmen_dopravu', early_change, 'změnu dopravy před neúspěšnou kontrolou'),
    ]
    if valid:
        for owner, name, replacement, label in mutants:
            original = getattr(owner, name)
            try:
                setattr(owner, name, replacement)
                result = run_tests(cls)
                c.add('Testy odhalí ' + label, bool(result.failures or result.errors), 'Doplňte ověření uvedeného scénáře přes veřejné rozhraní, včetně výsledku a zachovaného stavu.')
            finally:
                setattr(owner, name, original)
except BaseException as exc:
    c.add('Testovací sadu lze ověřit', False, f'{type(exc).__name__}: {exc}')
r = c.run()
if c.no_error(r):
    c.add('Hlavní blok spustí unittest', 'Ran ' in r.err + r.out and 'OK' in r.err + r.out, 'Ponechte unittest.main v hlavním bloku a proveďte své testy.')
c.done()
