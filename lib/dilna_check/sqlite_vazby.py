"""SQLite6–10: skutečné NULL/souhrny/vazby/JOIN a transakční konzolový model."""
from contextlib import closing
import copy
import math
from pathlib import Path
import sqlite3
import tempfile
from unittest.mock import patch
from .sqlite_intro import ProbeConnection,bindings,require

TEXTY=[(3,'Šachy',2),(4,'šachy',1),(8,'Karty 100%',0),(11,'Míč_A',5),(12,'MíčXA',1),(20,"Karty O'Neil",1),(25,'karty malé',2),(40,'',0)]
POZNAMKY=[(1,'První',None),(4,'Druhá',''),(7,'Dar','Žofie'),(9,'Jiný dar','Žofie'),(13,'Text NULL','NULL')]
SKUPINY=[(3,'Šachy',2,'Hry'),(8,'Karty',0,'Hry'),(11,'Lana',5,'Sport'),(20,'Míče',1,'Sport'),(30,'Krabice',3,None),(41,'Nula',0,'Nulová'),(50,'Další hra',2,'Hry')]
KATEGORIE=[(2,'Hry'),(7,'Sport'),(15,'Prázdná')]
POMUCKY=[(3,'Šachy',2,2),(8,'Karty',0,2),(11,'Lana',5,7),(20,'Krabice',1,None),(30,'Druhé lano',4,7)]
VYPUJCKY=[(1,3,'Žofie',0),(4,3,'Ada',1),(7,11,'Žofie',1),(9,8,'Ada',0),(12,3,'Žofie',0)]

def otevri(cesta=':memory:'):
    con=sqlite3.connect(cesta,autocommit=True,factory=ProbeConnection)
    con.execute('PRAGMA foreign_keys=ON')
    con.autocommit=False
    return con

def relacni_schema(con):
    # Nezávislá tabulka požadovaných pravidel, ne import studentského řešení.
    con.execute('CREATE TABLE kategorie(id INTEGER PRIMARY KEY,nazev TEXT NOT NULL UNIQUE)')
    con.execute("CREATE TABLE pomucky(id INTEGER PRIMARY KEY,nazev TEXT NOT NULL UNIQUE,kusy INTEGER NOT NULL CHECK(typeof(kusy)='integer' AND kusy>=0),kategorie_id INTEGER REFERENCES kategorie(id) ON DELETE SET NULL)")
    con.execute('CREATE TABLE vypujcky(id INTEGER PRIMARY KEY,pomucka_id INTEGER NOT NULL REFERENCES pomucky(id) ON DELETE RESTRICT,clen TEXT NOT NULL,vraceno INTEGER NOT NULL DEFAULT 0 CHECK(vraceno IN(0,1)))')

def priprav(con,kind,empty=False):
    if kind=='text':
        con.execute('CREATE TABLE pomucky(id INTEGER PRIMARY KEY,nazev TEXT NOT NULL,kusy INTEGER NOT NULL)')
        con.execute('CREATE TABLE udalosti(id INTEGER PRIMARY KEY,popis TEXT NOT NULL,poznamka TEXT)')
        if not empty:
            con.executemany('INSERT INTO pomucky VALUES(?,?,?)',TEXTY)
            con.executemany('INSERT INTO udalosti VALUES(?,?,?)',POZNAMKY)
    elif kind=='group':
        con.execute('CREATE TABLE pomucky(id INTEGER PRIMARY KEY,nazev TEXT NOT NULL,kusy INTEGER NOT NULL,kategorie TEXT)')
        con.execute('CREATE TABLE udalosti(id INTEGER PRIMARY KEY,popis TEXT NOT NULL,poznamka TEXT)')
        if not empty:
            con.executemany('INSERT INTO pomucky VALUES(?,?,?,?)',SKUPINY)
            con.executemany('INSERT INTO udalosti VALUES(?,?,?)',POZNAMKY)
    else:
        relacni_schema(con)
        if not empty:
            con.executemany('INSERT INTO kategorie VALUES(?,?)',KATEGORIE)
            con.executemany('INSERT INTO pomucky VALUES(?,?,?,?)',POMUCKY)
            con.executemany('INSERT INTO vypujcky VALUES(?,?,?,?)',VYPUJCKY)
    con.execute('CREATE TABLE rozpracovane(x INTEGER)')
    con.commit()
    con.execute('INSERT INTO rozpracovane VALUES(1)')
    con.events.clear()

def vlastnik(con):
    require(not con.was_closed,'Předané spojení nezavírejte.')
    con.rollback()
    require(con.execute('SELECT * FROM rozpracovane').fetchall()==[],
            'Nepotvrzujte cizí rozepsanou práci; hranice transakce patří volajícímu.')

def texty(ns,task):
    if task==4:
        original=sqlite3.connect;opened=[]
        def tracked(*args,**kw):
            kw.setdefault('factory',ProbeConnection);con=original(*args,**kw);opened.append(con);return con
        values=[None,'003',2.0,2.5,'ahoj',b'003',True,'']
        expected=[('null','null',None,None),('text','integer','003',3),('real','integer',2.0,2),
                  ('real','real',2.5,2.5),('text','text','ahoj','ahoj'),('blob','blob',b'003',b'003'),
                  ('integer','integer',1,1),('text','text','','')]
        try:
            with patch.object(sqlite3,'connect',side_effect=tracked):
                require(ns['zkus_typy'](iter(values))==expected and ns['zkus_typy']([])==[],
                        'Zkoumejte skutečnou afinitu SQLite, bez typu proti INTEGER; prázdný vstup dává [].')
            require(opened and all(c.was_closed for c in opened),'Vlastní paměťová spojení po pokusu zavřete.')
        finally:
            for c in opened:c.close()
        return
    for empty in [False,True]:
        with closing(otevri()) as con:
            priprav(con,'text',empty)
            data=[] if empty else TEXTY
            notes=[] if empty else POZNAMKY
            if task==0:
                require(ns['bez_poznamky'](con)==[(i,p) for i,p,n in notes if n is None],
                        'NULL testujte jako chybějící hodnotu, ne jako prázdný či doslovný text.')
            elif task==1:
                for fallback in ['bez poznámky',"  O'Neil  ",'']:
                    con.events.clear()
                    got=ns['zobraz_poznamky'](con,fallback)
                    bindings(con,[fallback])
                    require(got==[(i,p,fallback if n is None else n) for i,p,n in notes],
                            'COALESCE nahradí jen NULL, nikoli prázdný text; data nepřepisujte.')
            elif task==2:
                for term in ['%','_',"'Neil",'Š','karty','']:
                    con.events.clear()
                    got=ns['najdi_doslovne'](con,term);bindings(con,[term])
                    require(got==[r for r in data if term in r[1]],'Doslovné hledání nevykládá %/_ jako zástupné znaky a rozlišuje velikost.')
            else:
                cases={'Karty%':{8,20,25},'karty%':{8,20,25},'Míč_A':{11,12},'šachy':{4},'Šachy':{3},'':{40},'%':{r[0] for r in data}}
                for pattern,ids in cases.items():
                    con.events.clear()
                    got=ns['podle_vzoru'](con,pattern);bindings(con,[pattern])
                    require(got==[r for r in data if r[0] in ids],'LIKE vykládá %/_, ASCII velikost písmen a Unicode se nechovají stejně.')
            require(con.events,'Použijte skutečné SQL.')
            vlastnik(con)

def souhrny(ns,task):
    for empty in [False,True]:
        with closing(otevri()) as con:
            priprav(con,'group',empty);data=[] if empty else SKUPINY;notes=[] if empty else POZNAMKY
            if task==0:
                counts=[r[2] for r in data]
                expected=(len(data),sum(counts),min(counts) if counts else None,max(counts) if counts else None)
                require(ns['celkovy_souhrn'](con)==expected,'Prázdný COUNT je0, součet nahrazujeme nulou, MIN/MAX zůstávají None.')
            elif task in (1,3):
                groups={}
                for _,_,amount,cat in data:groups.setdefault(cat,[]).append(amount)
                if task==1:
                    expected=[(cat,len(groups[cat]),sum(groups[cat])) for cat in sorted(groups,key=lambda x:(x is not None,x or ''))]
                    require(ns['souhrn_kategorii'](con)==expected,'GROUP BY zahrne i jednu společnou skupinu pro NULL.')
                else:
                    for minimum in [0,3,6,50]:
                        con.events.clear()
                        got=ns['silne_kategorie'](con,minimum);bindings(con,[minimum])
                        expected=[(k,sum(v)) for k,v in groups.items() if sum(v)>=minimum]
                        expected.sort(key=lambda x:(-x[1],x[0] is not None,x[0] or ''))
                        require(got==expected,'HAVING filtruje hotové skupiny včetně přesné rovnosti hranice.')
            elif task==2:
                filled=[r[2] for r in notes if r[2] is not None]
                require(ns['pocet_vyplnenych'](con)==(len(notes),len(filled),len(set(filled))),
                        'COUNT sloupce ignoruje NULL, prázdný text počítá; DISTINCT odstraní shodné neprázdné i prázdné hodnoty.')
            else:
                got=ns['prumer_kusu'](con)
                require(got is None if empty else isinstance(got,(int,float)) and math.isclose(got,sum(r[2] for r in data)/len(data)),
                        'AVG zahrnuje nuly, prázdná tabulka vrací None.')
            require(con.events,'Souhrn počítejte skutečným SQL.')
            vlastnik(con)

def vazby(ns,task):
    if task==0:
        original=sqlite3.connect;opened=[]
        def tracked(*args,**kw):
            kw.setdefault('factory',ProbeConnection);con=original(*args,**kw);opened.append(con);return con
        try:
            with tempfile.TemporaryDirectory() as temp,patch.object(sqlite3,'connect',side_effect=tracked):
                for path in [':memory:',Path(temp)/'Český klub.sqlite3']:
                    con=ns['spojeni_s_vazbami'](path)
                    require(isinstance(con,sqlite3.Connection) and not con.was_closed and con.autocommit is False,
                            'Vraťte otevřené spojení s autocommit=False.')
                    require(con.execute('PRAGMA foreign_keys').fetchone()==(1,),'Foreign keys zapněte před začátkem transakce a ověřte.')
                    relacni_schema(con)
                    try:con.execute('INSERT INTO pomucky(nazev,kusy,kategorie_id) VALUES(?,?,?)',('Chybná vazba',1,999))
                    except sqlite3.IntegrityError:pass
                    else:require(False,'Vazba se musí skutečně vynucovat.')
        finally:
            for con in opened:con.close()
        return
    with closing(otevri()) as con:
        if task==1:
            ns['vytvor_relacni_schema'](con)
            con.execute('INSERT INTO kategorie VALUES(2,?)',('Hry',))
            con.execute('INSERT INTO pomucky VALUES(3,?,?,2)',('Šachy',2))
            con.execute('INSERT INTO pomucky VALUES(8,?,?,NULL)',('Krabice',0))
            con.execute('INSERT INTO vypujcky(id,pomucka_id,clen) VALUES(1,3,?)',('Žofie',))
            require(con.execute('SELECT vraceno FROM vypujcky').fetchone()==(0,),'Výchozí výpůjčka je aktivní.')
            for sql,args in [
                ('INSERT INTO pomucky(nazev,kusy,kategorie_id) VALUES(?,?,?)',('Neplatná',1,999)),
                ('INSERT INTO pomucky(nazev,kusy) VALUES(?,?)',('Záporná',-1)),
                ('INSERT INTO pomucky(nazev,kusy) VALUES(?,?)',('Textová','abc')),
                ('INSERT INTO vypujcky(pomucka_id,clen) VALUES(?,?)',(999,'Ema')),
                ('INSERT INTO vypujcky(pomucka_id,clen,vraceno) VALUES(?,?,?)',(3,'Ema',2)),
            ]:
                try:con.execute(sql,args)
                except sqlite3.IntegrityError:pass
                else:require(False,'Schéma skutečně vynucuje typ uložených kusů, rozsah a vazby.')
            con.execute('DELETE FROM kategorie WHERE id=2')
            require(con.execute('SELECT kategorie_id FROM pomucky WHERE id=3').fetchone()==(None,),'SET NULL zachová pomůcku po zrušení kategorie.')
            con.execute('UPDATE vypujcky SET vraceno=1')
            try:con.execute('DELETE FROM pomucky WHERE id=3')
            except sqlite3.IntegrityError:pass
            else:require(False,'RESTRICT chrání i vrácenou historii výpůjček.')
            before=con.execute('SELECT * FROM pomucky ORDER BY id').fetchall()
            ns['vytvor_relacni_schema'](con)
            require(con.execute('SELECT * FROM pomucky ORDER BY id').fetchall()==before,'Opakovaná příprava nemaže řádky.')
            con.rollback()
            require(con.execute("SELECT name FROM sqlite_schema WHERE type='table'").fetchall()==[],'Schéma nepotvrzuje transakci volajícího.')
            return
        priprav(con,'relations')
        if task==2:
            key=ns['zapis_pomucku'](con,"  Karty O'Neil  ",3,7);bindings(con,["  Karty O'Neil  ",3,7])
            require(con.execute('SELECT nazev,kusy,kategorie_id FROM pomucky WHERE id=?',(key,)).fetchone()==("  Karty O'Neil  ",3,7),'Vložte přesné hodnoty a vraťte skutečné id.')
            require(ns['zapis_pomucku'](con,'Bez kategorie',0) is not None,'Kategorie je volitelná.')
            try:ns['zapis_pomucku'](con,'Chybný odkaz',2,999)
            except sqlite3.IntegrityError:pass
            else:require(False,'Chybějící kategorii nepřijímejte.')
        elif task==3:
            require(ns['presun_do_kategorie'](con,3,7)==1,'Přiřazení vrací rowcount.')
            bindings(con,[3,7])
            require(con.execute('SELECT kategorie_id FROM pomucky WHERE id=3').fetchone()==(7,),'Změňte jen předané id.')
            require(ns['presun_do_kategorie'](con,3,None)==1 and ns['presun_do_kategorie'](con,999,7)==0,'NULL ruší vazbu, chybějící pomůcka vrací0.')
            try:ns['presun_do_kategorie'](con,8,999)
            except sqlite3.IntegrityError:pass
            else:require(False,'Neplatná cílová kategorie má vyvolat IntegrityError.')
        else:
            require(ns['smaz_kategorii'](con,2)==1 and ns['smaz_kategorii'](con,2)==0,'Zrušení vrací počet a je opakovatelné.')
            bindings(con,[2])
            require(con.execute('SELECT id,kategorie_id FROM pomucky WHERE id IN(3,8) ORDER BY id').fetchall()==[(3,None),(8,None)],'Zůstávají všechny pomůcky, jejich kategorie se uvolní.')
            require(con.execute('SELECT COUNT(*) FROM vypujcky').fetchone()==(len(VYPUJCKY),),'Historie výpůjček zůstává.')
        vlastnik(con)
        require(con.execute('SELECT * FROM pomucky ORDER BY id').fetchall()==POMUCKY,'Rollback volajícího vrátí i změnu vazby či SET NULL.')

def joiny(ns,task):
    for empty in [False,True]:
        with closing(otevri()) as con:
            priprav(con,'relations',empty)
            cats={} if empty else dict(KATEGORIE);items=[] if empty else POMUCKY;loans=[] if empty else VYPUJCKY
            if task in (0,1):
                f=ns['pomucky_s_kategorii' if task==0 else 'vsechny_pomucky']
                expected=[(i,n,q,cats.get(k)) for i,n,q,k in items if task==1 or k in cats]
                require(f(con)==expected,'INNER JOIN vybere jen přiřazené, LEFT JOIN zachová nezařazené bez duplikace.')
            elif task==2:
                expected=[(k,n,sum(1 for r in items if r[3]==k),sum(r[2] for r in items if r[3]==k)) for k,n in cats.items()]
                require(ns['prehled_kategorii'](con)==expected,'Prázdná kategorie má počet i součet0; COUNT(*) po LEFT JOIN není počet pomůcek.')
            elif task==3:
                active={p for _,p,_,returned in loans if returned==0}
                require(ns['bez_aktivni_vypujcky'](con)==[(i,n,q) for i,n,q,_ in items if i not in active],
                        'Pomůcka s aktivní i vrácenou výpůjčkou stále není bez aktivní; každý výsledek jednou.')
            else:
                names={i:n for i,n,_,_ in items}
                for name in ['Žofie','Ada',"Žofie' OR 1=1 --",'','žofie']:
                    con.events.clear()
                    got=ns['vypujcky_clena'](con,name);bindings(con,[name])
                    require(got==[(i,names[p]) for i,p,member,returned in loans if member==name and returned==0],
                            'Filtr člena je parametr, ponechte samostatná id opakovaných aktivních půjčení.')
            require(con.events,'Použijte skutečné SQL.')
            vlastnik(con)

def projekt(ns):
    cls=ns['Evidence']
    with tempfile.TemporaryDirectory() as temp:
        path=Path(temp)/'Český klub.sqlite3';e=cls(path)
        try:
            require(e.con.autocommit is False and e.con.execute('PRAGMA foreign_keys').fetchone()==(1,),'Projekt má vlastní transakční spojení a vynucuje vazby.')
            cat=e.pridej_kategorii('  Sport  ')
            item=e.pridej_pomucku("  Míč O'Neil  ",2,cat)
            box=e.pridej_pomucku('Krabice',0)
            require(e.prehled()==[(item,"Míč O'Neil",2,'Sport'),(box,'Krabice',0,None)],'Profil ořízne krajní mezery, výpis zachová nezařazené.')
            a=e.pujc(item,'  Žofie  ');b=e.pujc(item,'Ada')
            require(e.aktivni_vypujcky()==[(a,"Míč O'Neil",'Žofie'),(b,"Míč O'Neil",'Ada')],'Každá výpůjčka má vlastní id a normalizovaného člena.')
            for args in [(item,'Další'),(999,'Ema')]:
                try:e.pujc(*args)
                except ValueError:pass
                else:require(False,'Nedostupná pomůcka neotevře výpůjčku.')
            require(e.vrat(a) is True and e.vrat(a) is False and e.vrat(999) is False,'Stejný pokus vrátí kus jen jednou.')
            require(e.prehled()[0][2]==1,'Vrácený kus se skutečně obnoví.')
            # Selhání druhého zápisu nesmí ponechat první změnu skladu.
            with e.con:e.con.execute("CREATE TRIGGER stop_insert BEFORE INSERT ON vypujcky BEGIN SELECT RAISE(ABORT,'Zkouška zápisu'); END")
            try:e.pujc(item,'Ema')
            except sqlite3.IntegrityError:pass
            else:require(False,'Chybu druhého zápisu nepohlcujte.')
            require(e.prehled()[0][2]==1 and len(e.aktivni_vypujcky())==1,'Chyba INSERT vrátí předchozí odečet.')
            with e.con:
                e.con.execute('DROP TRIGGER stop_insert')
                e.con.execute("CREATE TRIGGER stop_return BEFORE UPDATE OF vraceno ON vypujcky BEGIN SELECT RAISE(ABORT,'Zkouška návratu'); END")
            try:e.vrat(b)
            except sqlite3.IntegrityError:pass
            else:require(False,'Chyba označení návratu se předá volajícímu.')
            require(e.prehled()[0][2]==1 and len(e.aktivni_vypujcky())==1,'Chyba vrácení nezdvojí počet.')
            with e.con:e.con.execute('DROP TRIGGER stop_return')
            require(e.vrat(b) is True and e.prehled()[0][2]==2 and not e.aktivni_vypujcky(),'Úspěšné vrácení zachová historii a původní dostupný počet.')
            for amount in [-1,True,2.0]:
                try:e.pridej_pomucku('Chybná',amount)
                except ValueError:pass
                else:require(False,'Počet v API je nezáporný přesný int.')
            try:e.pridej_pomucku('Chybná vazba',1,999)
            except sqlite3.IntegrityError:pass
            else:require(False,'Neplatný odkaz se neuloží.')
            for call in [lambda:e.pridej_kategorii(' '),lambda:e.pridej_pomucku('',1),lambda:e.pujc(item,' ')]:
                try:call()
                except ValueError:pass
                else:require(False,'Jméno je neprázdný text po strip.')
            with closing(sqlite3.connect(path,autocommit=True)) as other:
                require(other.execute('SELECT kusy FROM pomucky WHERE id=?',(item,)).fetchone()==(2,),'Výsledky jsou potvrzené i pro jiný proces.')
        finally:e.close()
        e.close()
        try:e.prehled()
        except sqlite3.ProgrammingError:pass
        else:require(False,'Po close se zavřené spojení znovu neotevírá.')
        with closing(cls(path)) as again:
            require(len(again.prehled())==2 and not again.aktivni_vypujcky(),'Znovunačtení zachová data bez duplikování.')
        old=Path(temp)/'stary.sqlite3'
        with closing(sqlite3.connect(old,autocommit=True)) as con:
            con.execute('CREATE TABLE pomucky(id INTEGER PRIMARY KEY,nazev TEXT,kusy INTEGER)')
            con.execute("INSERT INTO pomucky VALUES(1,'Původní data',3)")
        try:cls(old)
        except ValueError:pass
        else:require(False,'Staré nekompatibilní schéma se nemá vydávat za nový projekt.')
        with closing(sqlite3.connect(old,autocommit=True)) as con:
            require(con.execute('SELECT * FROM pomucky').fetchall()==[(1,'Původní data',3)] and con.execute("SELECT name FROM sqlite_schema WHERE type='table'").fetchall()==[('pomucky',)],
                    'Neúspěšná příprava starý soubor nemigruje a nic do něj trvale nepřidá.')

def over(c,ns,stage,task):
    def probe():
        require(ns is not None,'Nejprve opravte načtení programu.')
        if stage<4:[texty,souhrny,vazby,joiny][stage](ns,task)
        else:projekt(ns)
        return True
    ok,value=c.call({'probe':probe},'probe')
    c.add('Pravidla dotazů a klubovní evidence',ok and value is True,'' if ok and value is True else f'{type(value).__name__}: {value}')
    c.no_error(c.run())
