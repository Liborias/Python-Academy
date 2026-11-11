"""Pygame 2: kontrola scénářů, studentových testů, výsledků a předání."""
import copy
import io
import json
import math
import os
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch

def require(ok, text):
    if not ok:
        raise AssertionError(text)

def close(a, b):
    return math.isclose(a, b, abs_tol=1e-8, rel_tol=1e-9)

def scenario(ns, task):
    import model_hry as model
    from scenare import snimek
    if task in (0, 4):
        for seed in [17, 31, None]:
            steps = [((0, 0), 0.05)] * 19 + [((1, -1), 0.025)] * 11
            # None není opakovatelný seed; ověříme stav před prvním losem.
            if seed is None:
                steps = [((1, 0), 0.05)] * 2
            k = model.Kolo(seed)
            expected = [snimek(k)]
            for direction, dt in steps:
                k.update(direction, dt)
                expected.append(snimek(k))
            if task == 0:
                got = ns['prehraj'](seed, iter(steps))
                traces = [got]
            else:
                traces = ns['dvojice_behu'](seed, iter(steps))
                require(isinstance(traces, tuple) and len(traces) == 2, 'Vraťte dvojici stop.')
                require(traces[0] is not traces[1], 'Dva pokusy musí mít vlastní seznamy.')
            for got in traces:
                require(got == expected, 'Stopa obsahuje začátek i každý krok skutečného Kolo, s předaným seedem/časem/směrem.')
                require(all(a is not b for a, b in zip(got, got[1:])), 'Každý snímek je nový záznam.')
            if task == 4:
                traces[0][0]['skore'] = 99
                require(traces[1][0]['skore'] == 0, 'Dvojice nesdílí ani slovníky snímků.')
        return
    if task == 1:
        f = ns['rozdel_cas']
        for total, step in [(0, .05), (.12, .05), (1.03, .03), (.007, .02), (.3, .05)]:
            got = f(total, step)
            require(isinstance(got, list) and all(0 < x <= step for x in got), 'Vraťte kladné kroky do zadaného maxima.')
            require(close(math.fsum(got), total), 'Kroky musí pokrýt celý čas, včetně posledního zbytku.')
            require(all(close(x, step) for x in got[:-1]), 'Všechny kroky kromě posledního jsou plné.')
        for args in [(-1,), (math.nan,), (math.inf,), (1, 0), (1, .06), (1, math.inf)]:
            try: f(*args)
            except ValueError: pass
            else: require(False, 'Neplatný čas nebo krok odmítněte ValueError.')
    if task == 2:
        f = ns['naplanuj_vstup']
        changes = {1: [1, 0], 4: [0, -1]}
        before = copy.deepcopy(changes)
        got = f(6, changes)
        require(got == [(0, 0), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1)], 'Před změnou je nula, nový směr platí i v dalších snímcích.')
        require(changes == before and f(0, {}) == [], 'Vstupní mapu neměňte, nula snímků je platná.')
        changes[1][0] = 99
        require(got[1] == (1, 0), 'Stopa drží hodnoty směru, ne cizí seznamy.')
        for count in [-1, True, 1.5]:
            try: f(count, {})
            except ValueError: pass
            else: require(False, 'Počet musí být nezáporné celé číslo, bool není počet.')
    if task == 3:
        f = ns['souhrn_stopy']
        trace = [
            {'pozice': (0, 0), 'cas': 0, 'droni': (), 'konec': False},
            {'pozice': (3, 4), 'cas': .05, 'droni': (1, 2), 'konec': False},
            {'pozice': (0, 0), 'cas': .1, 'droni': (1,), 'konec': True},
            {'pozice': (0, 0), 'cas': .1, 'droni': (), 'konec': True},
        ]
        before = copy.deepcopy(trace)
        got = f(trace)
        require(got == {'kroky': 3, 'draha': 10.0, 'maximum_dronu': 2, 'konec_v_case': .1}, 'Počítejte celou dráhu, maximum v průběhu a první konec.')
        require(trace == before and f([]) == {'kroky': 0, 'draha': 0.0, 'maximum_dronu': 0, 'konec_v_case': None}, 'Souhrn nemění stopu a zvládne prázdný seznam.')

def test_mutants(task, model):
    """Každá vada mění veřejné chování, ne zdroj studentských testů."""
    if task == 0:
        update = model.Hrac.update
        def wrong_time(self, direction, dt): return update(self, direction, dt * 2)
        def diagonal(self, direction, dt):
            factor = math.sqrt(2) if all(direction) else 1
            return update(self, direction, dt * factor)
        def no_bounds(self, direction, dt):
            import pygame
            v = pygame.Vector2(direction)
            if v.length_squared(): v = v.normalize()
            self.pozice += v * self.rychlost * dt
            self.rect.center = tuple(round(x) for x in self.pozice)
        return [(model.Hrac, 'update', wrong_time, 'chybnou délku kroku'),
                (model.Hrac, 'update', diagonal, 'rychlejší diagonálu'),
                (model.Hrac, 'update', no_bounds, 'únik obrázku mimo arénu')]
    if task == 1:
        update = model.StitZakladny.update
        def partial(self, dt, inside):
            old = self.energie
            result = update(self, dt, inside)
            return True if inside and old > 0 else result
        def refill(self, dt, inside):
            result = update(self, dt, inside)
            if inside: self.energie = self.kapacita
            return result
        def no_cap(self, dt, inside):
            old = self.energie
            result = update(self, dt, inside)
            if not inside: self.energie = old + dt * self.obnova
            return result
        return [(model.StitZakladny, 'update', partial, 'ochranu s nedostatečnou energií'),
                (model.StitZakladny, 'update', refill, 'dobití uvnitř přístavu'),
                (model.StitZakladny, 'update', no_cap, 'překročení kapacity')]
    if task == 2:
        update = model.Kolo.update
        def double(self, direction, dt):
            old = self.zivoty
            update(self, direction, dt)
            if self.zivoty < old: self.zivoty -= 1
        def after_death(self, direction, dt):
            update(self, direction, dt)
            if self.konec and self.duvod == 'zivoty': self.seber_data()
        def reset(self, direction, dt):
            old = self.vlny.cislo
            update(self, direction, dt)
            if self.vlny.cislo != old: self.zivoty = 3
        return [(model.Kolo, 'update', double, 'dvojí účtování kontaktu'),
                (model.Kolo, 'update', after_death, 'sběr po smrtelném zásahu'),
                (model.Kolo, 'update', reset, 'obnovu životů při nové vlně')]
    if task == 3:
        update, event, new = model.Hra.update, model.Hra.zpracuj, model.Hra.novy_let
        def pause(self, direction, dt):
            if self.stav == 'pauza': self.kolo.update(direction, dt)
            else: update(self, direction, dt)
        def reuse(self):
            if self.kolo is None: new(self)
        def quit_ignored(self, e):
            import pygame
            if e.type != pygame.QUIT: event(self, e)
        return [(model.Hra, 'update', pause, 'čas běžící v pauze'),
                (model.Hra, 'novy_let', reuse, 'restart se starým modelem'),
                (model.Hra, 'zpracuj', quit_ignored, 'ignorované zavření')]
    init, wave, target, update = model.Vlny.__init__, model.Vlny.zahaj, model.HlidacBodu.cil, model.Kolo.update
    def seed(self, seed=23, interval=.75): init(self, 23, interval)
    def group(self):
        import pygame
        wave(self)
        self.drony = pygame.sprite.Group()
    def anchor(self, player):
        import pygame
        if (player.pozice - self.pozice).length() <= self.dosah: return pygame.Vector2(player.pozice)
        return self.kotva.copy()
    def frozen(self, direction, dt):
        if self.konec: self.cas += dt
        else: update(self, direction, dt)
    return [(model.Vlny, '__init__', seed, 'ignorovaný seed'),
            (model.Vlny, 'zahaj', group, 'záměnu původní skupiny'),
            (model.HlidacBodu, 'cil', anchor, 'dosah měřený od drona'),
            (model.Kolo, 'update', frozen, 'změnu světa po konci')]

def students_tests(c, task):
    import model_hry as model
    def run_suite():
        ns = {'__name__': 'studentske_testy', '__file__': str(c.student)}
        with __import__('contextlib').redirect_stdout(io.StringIO()):
            exec(compile(c.code, str(c.student), 'exec'), ns)
        suite = ns.get('sestav_sadu', lambda: None)()
        require(isinstance(suite, unittest.TestSuite), 'sestav_sadu vrací novou unittest.TestSuite.')
        result = unittest.TextTestRunner(stream=io.StringIO()).run(suite)
        require(result.testsRun > 0 and not result.skipped, 'Testy se skutečně provádějí bez přeskočení.')
        return result
    result = run_suite()
    require(result.wasSuccessful(), 'Na správném modelu musí testy projít; porovnávejte skutečné výsledky s očekáváním.')
    for owner, name, replacement, label in test_mutants(task, model):
        with patch.object(owner, name, replacement):
            result = run_suite()
        require(bool(result.failures or result.errors), 'Vaše testy mají odhalit ' + label + '.')

def records(ns, task):
    valid = {'jmeno': '  Žofie ', 'body': 7, 'uspech': True}
    if task == 0:
        f = ns['platny_vysledek']
        require(f(valid) is True, 'Platný výsledek je slovník se jménem, nezáporným celým počtem a bool úspěchem.')
        bad = [None, [], {}, {**valid, 'jmeno': ' '}, {**valid, 'jmeno': 'A' * 25},
               {**valid, 'body': True}, {**valid, 'body': -1}, {**valid, 'body': 7.0},
               {**valid, 'uspech': 1}]
        require(all(f(x) is False for x in bad), 'Odmítněte neúplná data, špatné typy, záporné body a prázdná/dlouhá jména.')
        return
    if task == 1:
        source = [valid.copy(), {'jmeno': '', 'body': 2, 'uspech': False}, {**valid, 'navic': 'ignorovat'}]
        before = copy.deepcopy(source)
        got = ns['vyber_vysledky'](source)
        require(got == [{'jmeno': 'Žofie', 'body': 7, 'uspech': True}] * 2 and source == before, 'Vyberte platné záznamy, ořízněte jména a zachovejte vstup.')
        require(got[0] is not source[0] and got[0] is not got[1] and ns['vyber_vysledky']({}) == [], 'Vraťte vlastní slovníky, ne odkazy ani neplatný kořen.')
        require(ns['vyber_vysledky'](None)==[] and ns['vyber_vysledky']((valid,))==[], 'Kořenem musí být list, ani n-tice platných záznamů nestačí.')
        return
    if task == 2:
        data = [{'jmeno': '  Bea', 'body': 7, 'uspech': True}, {'jmeno': 'Ada', 'body': 9, 'uspech': False},
                {'jmeno': 'bea', 'body': 7, 'uspech': True}, {'jmeno': 'Ada', 'body': 7, 'uspech': True},
                {'jmeno': 'Jan', 'body': 8, 'uspech': True}, {'body': 99}]
        before = copy.deepcopy(data)
        got = ns['serad_vysledky'](data, 4)
        require([x['jmeno'] for x in got] == ['Jan', 'Ada', 'Bea', 'bea'], 'Řaďte úspěch, body sestupně a jméno bez velikosti písmen; shody stabilně.')
        require(data == before and ns['serad_vysledky'](data, 0) == [], 'Řazení nemění vstup a respektuje limit nula.')
        for limit in [-1, True, 1.5]:
            try: ns['serad_vysledky'](data, limit)
            except ValueError: pass
            else: require(False, 'Neplatný limit odmítněte ValueError.')
        return
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        path = root / 'české výsledky.json'
        if task == 3:
            f = ns['nacti_vysledky']
            require(f(path) == [] and not path.exists(), 'Chybějící soubor vrací prázdný seznam bez zápisu.')
            for raw in [b'{broken', b'\xff', b'[]', b'{"verze":true,"vysledky":[]}', b'{"verze":2}', b'{"verze":1,"vysledky":{}}']:
                path.write_bytes(raw)
                require(f(str(path)) == [] and path.read_bytes() == raw, 'Chybný JSON, typ/verze a kódování vrací [], původní bajty se nemění.')
            for version in [True,2]:
                path.write_text(json.dumps({'verze':version,'vysledky':[valid]}),encoding='utf-8')
                require(f(path)==[], 'Neplatná verze nesmí propustit ani jinak platné záznamy.')
            path.write_text(json.dumps({'verze': 1, 'vysledky': [valid, {'body': True}]}), encoding='utf-8')
            require(f(path) == [{'jmeno': 'Žofie', 'body': 7, 'uspech': True}], 'Přijměte verzi1 a vyberte platné řádky.')
            try: f(root)
            except OSError: pass
            else: require(False, 'Přístupovou chybu nezaměňujte za prázdný JSON; předávejte OSError.')
        else:
            f = ns['uloz_vysledky']
            path = root / 'data' / path.name
            source = [valid, {'body': -1}]
            before = copy.deepcopy(source)
            require(f(path, source) == 1 and source == before, 'Uložte čisté záznamy, vraťte jejich počet, vstup neměňte.')
            require(json.loads(path.read_text(encoding='utf-8')) == {'verze': 1, 'vysledky': [{'jmeno': 'Žofie', 'body': 7, 'uspech': True}]}, 'Soubor má verzi1, UTF-8 a data.')
            previous = path.read_bytes()
            with patch('os.replace', side_effect=OSError('Cvičné selhání nahrazení')):
                try: f(path, [])
                except OSError: pass
                else: require(False, 'Chybu zápisu předejte volajícímu.')
            require(path.read_bytes() == previous and list(path.parent.iterdir()) == [path], 'Při chybě zachovejte původní soubor a odstraňte dočasný.')

def delivery(ns, task):
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp) / 'Česká hra s mezerou'
        root.mkdir()
        script = root / 'moje hra.PY'
        script.write_text('# hra\n', encoding='utf-8')
        exe = root / 'program.exe'
        python = 'C:/Můj Python/python.exe'
        if task == 0:
            f = ns['koren_aplikace']
            require(f(script, exe) == script.resolve().parent and f(script, root / 'dist/hra.exe', True) == (root / 'dist').resolve(), 'Zdrojový program vychází z __file__, zabalený z executable; oba vrací absolutní adresář.')
        if task == 1:
            sub = root / 'NAVOD.md'
            sub.mkdir()
            names = ['z.py', 'moje hra.PY', 'NAVOD.md', 'requirements.txt']
            require(ns['chybejici_soubory'](str(root), names) == ['NAVOD.md', 'requirements.txt', 'z.py'], 'Vraťte seřazené chybějící soubory, adresář stejného jména nestačí.')
            require(names == ['z.py', 'moje hra.PY', 'NAVOD.md', 'requirements.txt'] and len(list(root.iterdir())) == 2, 'Kontrola nevytváří soubory ani nemění seznam.')
        if task in (2, 3, 4):
            f = ns[['prikaz_spusteni', 'prikaz_baleni', 'prikaz_testu'][task-2]]
            if task == 2:
                require(f(python, script) == [python, '-X', 'utf8', str(script.resolve())], 'Vracíme seznam, cesty s mezerami zůstávají jedním argumentem.')
            if task == 3:
                out = root / 'stavební složka'
                got = f(python, script, out, 'Moje_Hra-2')
                expected = [python, '-m', 'PyInstaller', '--onedir', '--console', '--clean', '--noconfirm',
                            '--name', 'Moje_Hra-2', '--distpath', str(out.resolve()/'dist'),
                            '--workpath', str(out.resolve()/'build'), '--specpath', str(out.resolve()/'spec'), str(script.resolve())]
                require(got == expected and not out.exists(), 'Vraťte přesné argumenty včetně výstupních cest; nic nespouštějte ani nevytvářejte.')
                for name in ['', '../hra', 'Žofie', '2hra', 'A'*41]:
                    try: f(python, script, out, name)
                    except ValueError: pass
                    else: require(False, 'Jméno aplikace má 1–40 ASCII znaků, začíná písmenem a dovolí _ a -.')
            if task == 4:
                testdir = root / 'testy'
                testdir.mkdir()
                require(f(python, root) == [python, '-m', 'unittest', 'discover', '-s', str(testdir.resolve()), '-p', 'test_*.py'], 'Unittest discover dostane skutečnou složku testy a vzor názvů.')
            for invalid in [None, '', '  ']:
                args = (invalid, script) if task==2 else ((invalid, script, root) if task==3 else (invalid, root))
                try: f(*args)
                except ValueError: pass
                else: require(False, 'Prázdný nebo netextový interpreter odmítněte ValueError.')
            if task in (2,3):
                for bad in [root/'chybi.py', root, root/'NAVOD.md']:
                    args = (python, bad) if task==2 else (python, bad, root)
                    try: f(*args)
                    except ValueError: pass
                    else: require(False, 'Skript musí být existující Python soubor.')
            else:
                try: f(python, root/'chybi')
                except ValueError: pass
                else: require(False, 'Složka testy musí existovat.')

def final_game(ns):
    import pygame
    cls = ns['HraSPoradim']
    with tempfile.TemporaryDirectory() as temp:
        path = Path(temp)/'data'/'vysledky.json'
        h = cls(path, '  Žofie ', 275, 17)
        require(h.jmeno=='Žofie' and h.rychlost==275 and h.seed==17 and h.vysledky==[] and not path.exists(), 'Konstruktor přijme profil/seed/cestu, načte data bez zápisu a ořízne jméno.')
        h.novy_let()
        require(h.kolo.hrac.rychlost==275, 'Nový let používá vybranou rychlost.')
        h.kolo.konec,h.kolo.duvod,h.kolo.skore=True,'uspech',8
        h.update((0,0),0)
        expected=[{'jmeno':'Žofie','body':8,'uspech':True}]
        require(h.stav=='vysledek' and h.vysledky==expected and h.zapsane_kolo is h.kolo and h.zprava=='Výsledek uložen.', 'Právě dokončenou misi jednou zapište a zobrazte stav.')
        require(json.loads(path.read_text(encoding='utf-8'))=={'verze':1,'vysledky':expected}, 'Výsledek se skutečně uloží do předané cesty.')
        # Opakovaný update výsledku nesmí znovu sahat na disk.
        path.write_text('značka',encoding='utf-8')
        h.update((0,0),0)
        require(path.read_text(encoding='utf-8')=='značka', 'Stejné kolo se nezapisuje podruhé.')
        h.novy_let()
        h.kolo.konec,h.kolo.duvod,h.kolo.skore=True,'data',12
        h.update((0,0),0)
        require(len(h.vysledky)==2 and h.vysledky[0]['uspech'] is True, 'Další pokus má vlastní výsledek; úspěch má přednost před vyšším neúspěšným skóre.')
        loaded=cls(path)
        require(loaded.vysledky==h.vysledky, 'Nová instance načte dříve uložené pořadí.')
        old=list(h.vysledky)
        h.novy_let()
        h.kolo.konec,h.kolo.duvod,h.kolo.skore=True,'zivoty',2
        with patch('os.replace',side_effect=OSError('Disk')):
            h.update((0,0),0)
        require(h.vysledky==old and h.zprava=='Výsledek se nepodařilo uložit.' and h.zapsane_kolo is h.kolo, 'Chyba zápisu ponechá hru i předchozí tabulku a neopakuje se každý snímek.')
        # Nečitelná cesta je chyba přístupu, nepovažujeme ji za úspěšné načtení.
        inaccessible=cls(Path(temp))
        require(inaccessible.vysledky==[] and inaccessible.zprava=='Výsledky nejsou dostupné.', 'Chybu čtení oznamte, hra může pokračovat.')
        for score in range(9,15):
            h.novy_let()
            h.kolo.konec,h.kolo.duvod,h.kolo.skore=True,'uspech',score
            h.update((0,0),0)
        require(len(h.vysledky)==5 and [z['body'] for z in h.vysledky]==[14,13,12,11,10], 'Tabulka zachová jen nejlepších pět pokusů.')
        for name,speed in [('',260),('A'*25,260),('Ada',0),('Ada',math.inf)]:
            try: cls(path,name,speed)
            except ValueError: pass
            else: require(False,'Neplatné jméno/rychlost odmítněte ValueError.')
        # Ukončení ani menu nezapisují další pokusy.
        h.zpracuj(pygame.event.Event(pygame.QUIT))
        before=path.read_bytes()
        h.update((0,0),0)
        require(path.read_bytes()==before and not h.bezi,'Po QUIT se nic nezapisuje.')
    return True

def over(c, ns, stage, task):
    def probe():
        require(ns is not None,'Nejprve opravte načtení programu.')
        if stage==0: scenario(ns,task)
        elif stage==1: students_tests(c,task)
        elif stage==2: records(ns,task)
        elif stage==3: delivery(ns,task)
        else: final_game(ns)
        return True
    ok,result=c.call({'probe':probe},'probe')
    c.add('Chování nové části',ok and result is True,'' if ok and result is True else f'{type(result).__name__}: {result}')
    if stage==4:
        r=c.pygame_run(frames=75,events={0:[{'type':'KEYDOWN','key':'K_SPACE'}],30:[{'type':'KEYDOWN','key':'K_p'}],64:[{'type':'QUIT'}]},
                       held={0:['K_RIGHT']},pixels=[(383,300)],colors=[(245,135,90,24,90,672,390)])
        if c.pg_no_error(r):
            c.add('Skutečné okno a ovladatelný hráč',r.size==[720,540] and r.pixel((383,300),frame=7)==(80,185,255) and r.ended and r.frames==65,'Použijte stejný model a skutečné SDL okno, zavření i v pauze.')
            c.add('Profil v obraze',r.rendered('px/s') and r.rendered('Výsledky'),'Kreslete i připravený přehled profilu a výsledků.')
            raw=Path('droni.png').read_bytes() if Path('droni.png').exists() else b''
            c.add('Poslední PNG',len(raw)>24 and raw[:8]==b'\x89PNG\r\n\x1a\n' and struct.unpack('>II',raw[16:24])==(720,540),'Normální zavření ukládá snímek 720×540.')
    else:
        r=c.run()
        if c.no_error(r) and stage==1:
            c.add('Spuštěné vlastní testy','Ran ' in r.out+r.err and 'OK' in r.out+r.err,'Hlavní blok opravdu provede sadu unittest.')
