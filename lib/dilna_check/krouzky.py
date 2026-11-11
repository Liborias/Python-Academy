"""Skutečný SQLite model, chování formulářů a účinnost vlastních testů 11–15."""
from contextlib import closing
import io
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch
from .sqlite_intro import ProbeConnection, bindings, require


def trvale(cesta, sql, parametry, ocekavane):
    # Pozdější čtecí metoda modelu nesmí zamaskovat chybějící commit zápisu.
    with closing(sqlite3.connect(cesta, autocommit=True)) as jine:
        require(jine.execute(sql, parametry).fetchall() == ocekavane,
                'Každá úspěšná operace musí být ihned potvrzená i pro jiné spojení.')


def _over_model(Model, stage):
    with tempfile.TemporaryDirectory() as temp:
        cesta = Path(temp) / 'Český klub s mezerou.sqlite3'
        with closing(Model(cesta)) as m:
            require(m.con.autocommit is False and m.con.execute('PRAGMA foreign_keys').fetchone() == (1,),
                    'Model vlastní transakční spojení s vynucenými vazbami.')
            require(m.seznam() == [], 'Nový projekt začíná prázdný.')
            m.con.events.clear()
            ident = m.pridej("  Kroužek O'Neil  ", 2)
            bindings(m.con, ["Kroužek O'Neil", 2])
            trvale(cesta, 'SELECT nazev,kapacita FROM krouzky WHERE id=?', (ident,), [("Kroužek O'Neil", 2)])
            require(m.seznam() == [(ident, "Kroužek O'Neil", 2)], 'Ořízněte krajní mezery, zachovejte apostrof a vraťte skutečné id.')
            for kapacita in [0, -1, True, 2.0, '2']:
                try:
                    m.pridej('Chybná', kapacita)
                except ValueError:
                    pass
                else:
                    require(False, 'API vyžaduje kladný přesný int bez bool.')
            try:
                m.pridej('   ', 2)
            except ValueError:
                pass
            else:
                require(False, 'Prázdný název není kroužek.')
            try:
                m.pridej("Kroužek O'Neil", 3)
            except sqlite3.IntegrityError:
                pass
            else:
                require(False, 'Duplicitní název předá IntegrityError.')
            if stage == 0:
                dalsi = m.pridej('Abecedně první', 1)
                require(m.seznam() == [(ident, "Kroužek O'Neil", 2), (dalsi, 'Abecedně první', 1)],
                        'Seznam má výslovné pořadí id, nikoli názvů.')
            if stage >= 2:
                # Index v okně není klíč tabulky; id jsou záměrně nesouvislá.
                with m.con:
                    m.con.execute('INSERT INTO krouzky VALUES(20,?,3)', ('Druhý',))
                    m.con.execute('INSERT INTO krouzky VALUES(37,?,4)', ('Třetí',))
                require(m.uprav(37, "  Nový O'Neil  ", 3) is True,
                        'Úprava existujícího kroužku vrací True.')
                trvale(cesta, 'SELECT nazev,kapacita FROM krouzky WHERE id=?', (37,), [("Nový O'Neil", 3)])
                require(m.uprav(999, 'Nic', 2) is False,
                        'Upravte podle skutečného id, chybějící řádek vrací False.')
                require(m.smaz(20) is True and m.smaz(20) is False, 'Mazání je podle id a lze opakovat.')
                trvale(cesta, 'SELECT id FROM krouzky WHERE id=?', (20,), [])
                require(m.seznam() == [(ident, "Kroužek O'Neil", 2), (37, "Nový O'Neil", 3)], 'Ostatní kroužky zůstanou.')
                with m.con:
                    m.con.execute('INSERT INTO prihlasky VALUES(42,37,?)', ('Ada',))
                    m.con.execute('INSERT INTO prihlasky VALUES(55,37,?)', ('Žofie',))
                try:
                    m.uprav(37, 'Neuložit', 1)
                except ValueError:
                    pass
                else:
                    require(False, 'Kapacita nesmí klesnout pod již přihlášené; název se také nezmění.')
                require(m.seznam()[-1] == (37, "Nový O'Neil", 3), 'Chyba změny zachová celý původní řádek.')
                try:
                    m.smaz(37)
                except sqlite3.IntegrityError:
                    pass
                else:
                    require(False, 'Přihlášky chrání kroužek před smazáním.')
            if stage >= 3:
                prvni = m.prihlas(ident, "  Žofie O'Neil  ")
                trvale(cesta, 'SELECT krouzek_id,clen FROM prihlasky WHERE id=?', (prvni,), [(ident, "Žofie O'Neil")])
                try:
                    m.prihlas(ident, "Žofie O'Neil")
                except sqlite3.IntegrityError:
                    pass
                else:
                    require(False, 'Tentýž člen se do stejného kroužku nepřihlásí dvakrát.')
                druhy = m.prihlas(ident, 'Ada')
                try:
                    m.prihlas(ident, 'Navíc')
                except ValueError:
                    pass
                else:
                    require(False, 'Plný kroužek odmítne dalšího člena.')
                require(m.prihlasky(ident) == [(prvni, "Žofie O'Neil"), (druhy, 'Ada')], 'Přihlášky vracejí vlastní id, jméno a pořadí.')
                require(m.prihlasky(999) == [], 'Neexistující kroužek nemá přihlášky.')
                try:
                    m.prihlas(999, 'Ada')
                except ValueError:
                    pass
                else:
                    require(False, 'Neexistující kroužek vyvolá ValueError.')
                require(m.odhlas(prvni) is True and m.odhlas(prvni) is False and m.odhlas(999) is False,
                        'Odhlaste id přihlášky právě jednou, nikoli index nebo id kroužku.')
                trvale(cesta, 'SELECT id FROM prihlasky WHERE id=?', (prvni,), [])
                m.prihlas(ident, 'Nový člen')
                m.prihlas(37, 'Nový člen')  # Stejné jméno v jiném kroužku je dovoleno.
                prazdny = m.pridej('Prázdný', 1)
                require(m.souhrn() == [(ident, "Kroužek O'Neil", 2, 2), (37, "Nový O'Neil", 3, 3), (prazdny, 'Prázdný', 1, 0)],
                        'Souhrn zachová prázdné kroužky s nulou, pořadí id i správné počty.')
            with closing(sqlite3.connect(cesta, autocommit=True)) as other:
                require(other.execute('SELECT nazev FROM krouzky WHERE id=?', (ident,)).fetchone() == ("Kroužek O'Neil",),
                        'Úspěch je potvrzený i pro další spojení.')
        m.close()
        with closing(Model(cesta)) as znovu:
            require(znovu.seznam()[0] == (ident, "Kroužek O'Neil", 2), 'Po novém spuštění data zůstanou.')
        try:
            m.seznam()
        except sqlite3.ProgrammingError:
            pass
        else:
            require(False, 'Po close model neotevírá spojení automaticky.')



def over_model(Model, stage):
    original = sqlite3.connect
    opened = []
    def tracked(*args, **kwargs):
        kwargs.setdefault('factory', ProbeConnection)
        con = original(*args, **kwargs)
        opened.append(con)
        return con
    try:
        with patch.object(sqlite3, 'connect', side_effect=tracked):
            _over_model(Model, stage)
        require(opened and all(c.was_closed for c in opened), 'Každé vlastní spojení musí být zavřené.')
    finally:
        for con in opened:
            con.close()

def named(r, name, index=-1):
    return next((w for w in r.widgets(index=index) if w.get('name') == name), {})


def fill(name, value):
    return {'action': 'fill', 'name': name, 'value': value}


def click(text):
    return {'action': 'click', 'text': text}


def select(index, name='krouzky'):
    return {'action': 'select', 'name': name, 'index': index}


def over_formular(c, stage):
    actions = [fill('nazev', '  Robotika  '), fill('kapacita', '4'), click('Přidat kroužek'),
               fill('nazev', '  Keramika  '), fill('kapacita', '1.5'), click('Přidat kroužek'),
               fill('kapacita', '2'), click('Přidat kroužek')]
    r = c.tk_run(actions)
    if c.tk_no_error(r):
        c.add('Jedno viditelné okno a jedna smyčka', len(r.widgets('root')) == 1 and r.widgets('root')[0]['visible'] and r.mainloops == 1)
        c.add('Duplicitní název nezmění seznam ani formulář',
              len(named(r, 'krouzky', 3).get('items', [])) == 2 and named(r, 'nazev', 3).get('value') == '  Robotika  '
              and named(r, 'stav', 3).get('text') == 'Název kroužku už existuje.')
        c.add('Chybná kapacita zachová rozpracovaná pole', named(r, 'nazev', 6).get('value') == '  Keramika  '
              and named(r, 'kapacita', 6).get('value') == '1.5' and len(named(r, 'krouzky', 6).get('items', [])) == 2)
        c.add('Opravený formulář uloží skutečný nový řádek', named(r, 'krouzky').get('items') ==
              ['1: Robotika (kapacita 2)', '2: Šachy (kapacita 3)', '3: Keramika (kapacita 2)']
              and named(r, 'nazev').get('value') == '' and named(r, 'kapacita').get('value') == '10')
    if stage >= 2:
        actions = [click('Uložit změny'), select(0), click('Smazat kroužek'), select(0),
                   fill('nazev', '  Šachy nové  '), fill('kapacita', '4'), click('Uložit změny'),
                   fill('nazev', 'Další'), fill('kapacita', '2'), click('Přidat kroužek'),
                   select(1), click('Smazat kroužek')]
        r = c.tk_run(actions)
        if c.tk_no_error(r, 'Výběr a změny po smazání'):
            c.add('Chybějící výběr je vysvětlený', named(r, 'stav', 1).get('text') == 'Nejprve vyberte kroužek.')
            c.add('Vybraná položka naplní formulář', named(r, 'nazev', 4).get('value') == 'Šachy' and named(r, 'kapacita', 4).get('value') == '3')
            c.add('Po mezeře v id se mění správný kroužek', named(r, 'krouzky', 7).get('items') == ['2: Šachy nové (kapacita 4)'])
            c.add('Mazání používá mapu dat, nikoli pořadí jako id', named(r, 'krouzky').get('items') == ['2: Šachy nové (kapacita 4)'])
    if stage >= 3:
        actions = [click('Přihlásit člena'), select(0), fill('clen', '  Žofie  '), click('Přihlásit člena'),
                   fill('clen', 'Žofie'), click('Přihlásit člena'), fill('clen', 'Ada'), click('Přihlásit člena'),
                   fill('clen', 'Navíc'), click('Přihlásit člena'), fill('kapacita', '1'), click('Uložit změny'),
                   click('Smazat kroužek'), select(0, 'prihlasky'), click('Odhlásit člena'),
                   click('Odhlásit člena'), fill('clen', "  O'Neil  "), click('Přihlásit člena'),
                   select(1, 'prihlasky'), click('Odhlásit člena')]
        r = c.tk_run(actions)
        if c.tk_no_error(r, 'Přihlášky a kapacita formuláře'):
            c.add('Bez výběru se nepřihlašuje', named(r, 'stav', 1).get('text') == 'Nejprve vyberte kroužek.')
            c.add('Duplicitní přihláška zachová jméno', named(r, 'clen', 6).get('value') == 'Žofie' and len(named(r, 'prihlasky', 6).get('items', [])) == 1)
            c.add('Plný kroužek zachová formulář i přihlášky', named(r, 'stav', 10).get('text') == 'Kroužek je plný.' and named(r, 'clen', 10).get('value') == 'Navíc')
            c.add('Nelze zmenšit pod obsazenost ani smazat přihlášky', named(r, 'stav', 12).get('text') == 'Kapacita nesmí být menší než počet přihlášek.'
                  and named(r, 'stav', 13).get('text') == 'Kroužek nelze smazat: odhlaste členy.')
            c.add('Odhlášení vyžaduje nový výběr', named(r, 'stav', 16).get('text') == 'Nejprve vyberte přihlášku.')
            c.add('Uvolněné místo lze znovu obsadit', named(r, 'prihlasky', 18).get('items') == ['2: Ada', "3: O'Neil"]
                  and named(r, 'obsazenost', 18).get('text') == 'Obsazeno 2 / 2' and named(r, 'clen').get('value') == '')
            c.add('Po mezeře v id se odhlásí správný člen', named(r, 'prihlasky').get('items') == ['2: Ada']
                  and named(r, 'obsazenost').get('text') == 'Obsazeno 1 / 2')


def over_sadu(c, ns):
    from prihlasky import Model
    require(ns is not None, 'Nejprve opravte načtení programu.')
    def run(cls):
        suite = ns['vytvor_sadu'](cls)
        require(isinstance(suite, unittest.TestSuite) and suite.countTestCases() >= 6, 'Vraťte TestSuite s alespoň šesti testy.')
        vystup = io.StringIO()
        result = unittest.TextTestRunner(stream=vystup).run(suite)
        return result, vystup.getvalue()
    result, vystup = run(Model)
    require(result.wasSuccessful() and not result.skipped, 'Testy správného modelu musí projít bez přeskočení.\n' + vystup[-1500:])
    class BezPotvrzeni(Model):
        def pridej(self, nazev, kapacita):
            return self.con.execute('INSERT INTO krouzky(nazev,kapacita) VALUES(?,?)', (nazev.strip(), kapacita)).lastrowid
    class BezJedinecnosti(Model):
        def pridej(self, nazev, kapacita):
            nalezeny = self.con.execute('SELECT id FROM krouzky WHERE nazev=?', (nazev.strip(),)).fetchone()
            return nalezeny[0] if nalezeny else super().pridej(nazev, kapacita)
    class BezKapacity(Model):
        def prihlas(self, ident, clen):
            with self.con:
                return self.con.execute('INSERT INTO prihlasky(krouzek_id,clen) VALUES(?,?)', (ident, clen)).lastrowid
    class BezDuplicity(Model):
        def prihlas(self, ident, clen):
            nalezeny = self.con.execute('SELECT id FROM prihlasky WHERE krouzek_id=? AND clen=?', (ident, clen.strip())).fetchone()
            return nalezeny[0] if nalezeny else super().prihlas(ident, clen)
    class BezMeze(Model):
        def uprav(self, ident, nazev, kapacita):
            with self.con:
                return self.con.execute('UPDATE krouzky SET nazev=?,kapacita=? WHERE id=?', (nazev, kapacita, ident)).rowcount == 1
    class BezOchrany(Model):
        def smaz(self, ident):
            with self.con:
                self.con.execute('DELETE FROM prihlasky WHERE krouzek_id=?', (ident,))
                return super().smaz(ident)
    for cls, popis in [(BezPotvrzeni, 'trvalé uložení'), (BezJedinecnosti, 'jedinečnost názvu'),
                       (BezKapacity, 'plná kapacita'), (BezDuplicity, 'duplicitní člen'),
                       (BezMeze, 'zmenšení kapacity'), (BezOchrany, 'ochrana přihlášek')]:
        result, _ = run(cls)
        require(not result.wasSuccessful(), f'Vaše testy zatím neodhalí poruchu: {popis}.')
    return True


def over(c, stage):
    # Import nesmí otevřít databázi ani okno. Vlastní běh je až pod __main__.
    with patch.object(sqlite3, 'connect', side_effect=RuntimeError('Import nesmí otevřít databázi.')):
        ns = c.load()
    if stage in (0, 2, 3):
        def probe():
            require(ns is not None, 'Opravte načtení programu.')
            over_model(ns['EvidenceKrouzku' if stage == 0 else 'Model'], stage)
            return True
        ok, value = c.call({'probe': probe}, 'probe')
        c.add('Pravidla skutečné databáze', ok and value is True, '' if ok and value is True else str(value))
    if stage in (1, 2, 3):
        over_formular(c, stage)
    if stage == 4:
        ok, value = c.call({'probe': lambda: over_sadu(c, ns)}, 'probe')
        c.add('Vlastní testy ověřují chování', ok and value is True, '' if ok and value is True else str(value))
    if stage in (0, 4):
        c.no_error(c.run())
