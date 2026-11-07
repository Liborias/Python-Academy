import io
import os
import sys
import unittest
sys.path.insert(0, os.getcwd())
from dilna_check import check
import test_centrum

c = check()
ns = c.load()
try:
    center = ns['vytvor_demo']()
    def command(text, expected):
        ok, value = c.call(ns, 'proved_prikaz', (center, text))
        c.add('Příkaz ' + text, ok and value == expected and c.last_output == '', 'Vraťte dohodnutý text, použijte předané centrum a nic sami nevypisujte.')
    command('', '')
    command('  stav  ', 'Sklad: KNIHA=5, OBAL=2')
    for text in ('nova X 0 0 800', 'nova X -1 0 800', 'nova X 1 0 0', 'nova X 1.5 0 800', 'nova X True 0 800', 'nova X 1 3 800', 'nova X 1 0', 'neznámý', 'storno CHYBÍ', 'prehled CHYBÍ', 'poznamka X', 'doprava X jiné', 'stav navíc'):
        before = center.sklad.prehled()
        c.raises(ns, 'proved_prikaz', (center, text), ValueError)
        c.add('Chybný vstup nemění zásoby', center.sklad.prehled() == before, 'Ověřte celý vstup před přijetím a nechte model odmítnout neplatnou operaci.')
    command('nova A 2 1 1200', 'Přijato: A')
    command('stav', 'Sklad: KNIHA=3, OBAL=1')
    command('doprava A kuryr', 'Doprava: 99 Kč')
    command('doprava A kolo', 'Doprava: 59 Kč')
    command('poznamka A  Nezvonit   prosím  ', 'Poznámek: 1')
    command('prehled A', 'A: rezervovana\nZboží: 530 Kč | Doprava: 59 Kč | Nabídka: 589 Kč\nBalík: B-A | Adresa: Javorová 1, 60200 Brno\nPoznámky: Nezvonit prosím')
    for text in ('nova A 1 0 1000', 'nova B 4 0 800', 'doprava A letadlo', 'doprava A', 'storno A navíc'):
        before = center.souhrn('A'), center.sklad.prehled()
        c.raises(ns, 'proved_prikaz', (center, text), ValueError)
        c.add('Odmítnutí zachová přijaté objednávky', (center.souhrn('A'), center.sklad.prehled()) == before, 'Nepřepisujte přijaté číslo ani neprovádějte částečnou rezervaci.')
    command('nova T 1 0 2001', 'Přijato: T')
    before = center.souhrn('T')
    c.raises(ns, 'proved_prikaz', (center, 'doprava T kolo'), ValueError)
    c.add('Nadlimitní kolo nemění volbu', center.souhrn('T') == before, 'Předávejte výjimku z centra a zachovejte původní dopravu.')
    command('storno A', 'Stornováno: A')
    c.raises(ns, 'proved_prikaz', (center, 'storno A'), ValueError)
    c.raises(ns, 'proved_prikaz', (center, 'poznamka A Pozdě'), ValueError)
    command('nova B 4 0 800', 'Přijato: B')
    command('doprava B odber', 'Doprava: 0 Kč')
    command('stav', 'Sklad: KNIHA=0, OBAL=2')
    independent = ns['vytvor_demo']()
    c.add('Nové spuštění má vlastní cvičný sklad', independent.sklad.prehled() == {'KNIHA': 5, 'OBAL': 2}, 'Nové centrum vytvářejte při spuštění, ne při každém příkazu.')
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_centrum)
    result = unittest.TextTestRunner(stream=io.StringIO()).run(suite)
    c.add('Přiložené testy projektu projdou', result.wasSuccessful() and result.testsRun == 4 and not result.skipped, 'Ponechte funkční moduly projektu a testy z připravené složky.')
except BaseException as exc:
    c.add('Ovladač lze ověřit', False, f'{type(exc).__name__}: {exc}')
r = c.run(stdin='stav\nnova A 2 1 1200\ndoprava A kolo\nprehled A\nnova B 4 0 800\nstorno A\nstorno A\nnova B 4 0 800\nstav\nkonec\n')
if c.no_error(r):
    for text in ('Přijato: A', 'Doprava: 59 Kč', 'Nabídka: 589 Kč', 'Odmítnuto:', 'Stornováno: A', 'Přijato: B', 'Sklad: KNIHA=1, OBAL=2', 'Na shledanou.'):
        c.output_contains(r, text)
c.done()
