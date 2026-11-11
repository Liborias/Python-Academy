"""SQLite 1–5: skutečný databázový stroj, vazba parametrů a hranice transakcí."""
from contextlib import closing
import copy
from pathlib import Path
import sqlite3
import tempfile
from unittest.mock import patch

def require(ok,message):
    if not ok:raise AssertionError(message)

def saved_parameters(parameters):
    return dict(parameters) if isinstance(parameters,dict) else tuple(parameters)

class ProbeCursor(sqlite3.Cursor):
    def execute(self,sql,parameters=()):
        self.connection.events.append((sql,saved_parameters(parameters)))
        return super().execute(sql,parameters)
    def executemany(self,sql,rows):
        def values():
            for row in rows:
                self.connection.events.append((sql,saved_parameters(row)))
                yield row
        return super().executemany(sql,values())

class ProbeConnection(sqlite3.Connection):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.events=[]
        self.was_closed=False
    def execute(self,sql,parameters=()):
        self.events.append((sql,saved_parameters(parameters)))
        return super().execute(sql,parameters)
    def executemany(self,sql,rows):
        def values():
            for row in rows:
                self.events.append((sql,saved_parameters(row)))
                yield row
        return super().executemany(sql,values())
    def executescript(self,sql):
        self.events.append((sql,()))
        return super().executescript(sql)
    def cursor(self,*args,**kwargs):
        if not args and 'factory' not in kwargs:kwargs['factory']=ProbeCursor
        return super().cursor(*args,**kwargs)
    def close(self):
        self.was_closed=True
        return super().close()

def bindings(con,values):
    parameters=[v for _,p in con.events for v in (p.values() if isinstance(p,dict) else p)]
    require(all(any(v==value for v in parameters) for value in values),
            'Předávejte hodnoty odděleně jako SQL parametry, přes spojení nebo kurzor; nevkládejte je do textu SQL.')

def rows(con):
    return [tuple(r) for r in con.execute('SELECT id,nazev,kusy FROM pomucky ORDER BY id')]

def fixture(con,data=()):
    # Vlastní popis požadovaných tabulek, nepoužívá studentskou implementaci.
    con.execute('CREATE TABLE pomucky (id INTEGER PRIMARY KEY, nazev TEXT NOT NULL UNIQUE, kusy INTEGER NOT NULL DEFAULT 0 CHECK(kusy>=0))')
    con.execute('CREATE TABLE udalosti (id INTEGER PRIMARY KEY, popis TEXT NOT NULL, poznamka TEXT)')
    con.executemany('INSERT INTO pomucky(id,nazev,kusy) VALUES(?,?,?)',data)
    con.commit()
    con.events.clear()

def expect_integrity(con,sql,params):
    try:con.execute(sql,params)
    except sqlite3.IntegrityError:return
    require(False,'Pravidla tabulky musí odmítnout zakázanou hodnotu přes sqlite3.IntegrityError.')

def connection_probe(ns,task):
    real_connect=sqlite3.connect
    opened=[]
    def connect(*args,**kwargs):
        kwargs.setdefault('factory',ProbeConnection)
        con=real_connect(*args,**kwargs)
        opened.append(con)
        return con
    def check_closed():
        require(opened and all(c.was_closed for c in opened),'Vlastní spojení po získání hodnoty výslovně zavřete, například přes closing.')
        require(any(c.events for c in opened),'Výsledek má vzniknout skutečným SQL dotazem.')
    with tempfile.TemporaryDirectory() as temp:
        root=Path(temp)
        try:
            with patch.object(sqlite3,'connect',side_effect=connect):
                if task==0:
                    path=root/'Česká databáze.sqlite3'
                    require(ns['verze_databaze'](path)==sqlite3.sqlite_version and path.is_file(),'Přijměte předanou cestu a vraťte verzi skutečného SQLite stroje.')
                    with closing(real_connect(path,autocommit=True)) as other:
                        other.execute('CREATE TABLE puvodni(text TEXT)')
                        other.execute('INSERT INTO puvodni VALUES(?)',('Žofie',))
                    require(ns['verze_databaze'](str(path))==sqlite3.sqlite_version,'Přijměte také textovou cestu.')
                    with closing(real_connect(path,autocommit=True)) as other:
                        require(other.execute('SELECT text FROM puvodni').fetchall()==[('Žofie',)],'Existující databázi nemažte ani neobnovujte.')
                    require(ns['verze_databaze'](':memory:')==sqlite3.sqlite_version,'Paměťová databáze je platná cesta.')
                    check_closed()
                elif task==1:
                    for text in ["Žofie O'Neil",'  Ada  ',"'); DROP TABLE x; --",'']:
                        require(ns['pozdrav_sql'](text)=='Ahoj, '+text,'Apostrof i mezery patří do hodnoty; text neořezávejte.')
                    check_closed()
                    parameters=[v for c in opened for _,p in c.events for v in (p.values() if isinstance(p,dict) else p)]
                    require("Žofie O'Neil" in parameters,'Jméno předávejte jako oddělený parametr dotazu.')
                elif task==2:
                    for a,b in [(2,3),(-9,4),(0,0),(12345,-231)]:
                        require(ns['secti_sql'](a,b)==a+b,'Součet získáte skutečným SQL s předanými hodnotami.')
                    check_closed()
                elif task==3:
                    path=root/'počty.sqlite3'
                    with closing(real_connect(path,autocommit=True)) as other:
                        other.execute('CREATE TABLE hraci(id INTEGER PRIMARY KEY AUTOINCREMENT)')
                        other.execute('CREATE TABLE sqlitex(hodnota TEXT)')
                        other.execute('CREATE VIEW pohled AS SELECT * FROM hraci')
                        other.execute('CREATE INDEX index_hodnot ON sqlitex(hodnota)')
                    require(ns['pocet_tabulek'](path)==2,'Počítejte jen vlastní tabulky; ne view/index ani sqlite_sequence, sqlitex je vlastní tabulka.')
                    require(ns['pocet_tabulek'](':memory:')==0,'Prázdná paměťová databáze nemá vlastní tabulky.')
                    check_closed()
                else:
                    a,b=ns['otevri_databazi'](':memory:'),ns['otevri_databazi'](':memory:')
                    require(isinstance(a,sqlite3.Connection) and a is not b and a.autocommit is True and b.autocommit is True,
                            'Vraťte nové otevřené spojení s autocommit=True; vlastní je volající.')
                    a.execute('CREATE TABLE vlastni(x INTEGER)')
                    a.execute('INSERT INTO vlastni VALUES(7)')
                    require(a.execute('SELECT x FROM vlastni').fetchall()==[(7,)] and not a.in_transaction,'Samostatné zápisy mají být potvrzené.')
                    require(b.execute("SELECT COUNT(*) FROM sqlite_schema WHERE type='table'").fetchone()[0]==0,'Dvě :memory: spojení nesdílí data.')
                    path=root/'vracene.sqlite3'
                    c=ns['otevri_databazi'](path)
                    require(c.execute('SELECT 5').fetchone()==(5,) and path.exists(),'Vraťte použitelné spojení i k souboru.')
        finally:
            for con in opened:con.close()

def schema_probe(ns,task):
    names=['vytvor_pomucky','vytvor_kategorie','vytvor_vypujcky','vytvor_udalosti','vytvor_sklad']
    with closing(sqlite3.connect(':memory:',autocommit=False,factory=ProbeConnection)) as con:
        result=ns[names[task]](con)
        require(result is None and not con.was_closed,'Připravte tabulku bez návratu dat, předané spojení nezavírejte.')
        if task in (0,4):
            con.execute('INSERT INTO pomucky(nazev) VALUES(?)',('Míče',))
            row=con.execute('SELECT id,nazev,kusy FROM pomucky').fetchone()
            require(type(row[0]) is int and row[0]>0 and row[1:]==('Míče',0),'Pomůcka má automatický id a výchozí nulu.')
            for sql,p in [('INSERT INTO pomucky(nazev,kusy) VALUES(?,?)',('Míče',2)),
                          ('INSERT INTO pomucky(nazev,kusy) VALUES(?,?)',(None,2)),
                          ('INSERT INTO pomucky(nazev,kusy) VALUES(?,?)',('Záporné',-1)),
                          ('INSERT INTO pomucky(nazev,kusy) VALUES(?,?)',('Chybí počet',None))]:
                expect_integrity(con,sql,p)
        if task in (1,4):
            con.execute('INSERT INTO kategorie(nazev) VALUES(?)',('Sport',))
            expect_integrity(con,'INSERT INTO kategorie(nazev) VALUES(?)',('Sport',))
            expect_integrity(con,'INSERT INTO kategorie(nazev) VALUES(?)',(None,))
        if task==2:
            con.execute('INSERT INTO vypujcky(pomucka,clen) VALUES(?,?)',('Míč','Žofie'))
            require(con.execute('SELECT vraceno FROM vypujcky').fetchone()==(0,),'Nová výpůjčka má vraceno=0.')
            for p in [('Lano','Ema',2),('Lano','Ema',None),(None,'Ema',0),('Lano',None,0)]:
                expect_integrity(con,'INSERT INTO vypujcky(pomucka,clen,vraceno) VALUES(?,?,?)',p)
        if task==3:
            con.execute('INSERT INTO udalosti(popis) VALUES(?)',('Klub otevřen',))
            require(con.execute('SELECT popis,poznamka FROM udalosti').fetchone()==('Klub otevřen',None),'Poznámka smí chybět, čteme Python None.')
            expect_integrity(con,'INSERT INTO udalosti(popis) VALUES(?)',(None,))
        target=['pomucky','kategorie','vypujcky','udalosti','pomucky'][task]
        generated=con.execute('SELECT id FROM '+target).fetchone()[0]
        require(type(generated) is int and generated>0,'Id se má při vložení bez id skutečně vytvořit jako celé číslo.')
        before=con.execute('SELECT * FROM '+target).fetchall()
        ns[names[task]](con)
        require(con.execute('SELECT * FROM '+target).fetchall()==before,'Opakované vytvoření zachová řádky.')
        con.rollback()
        require(con.execute("SELECT name FROM sqlite_schema WHERE type='table'").fetchall()==[],
                'Funkce s předaným con neukončuje transakci; rollback volajícího musí vrátit i CREATE TABLE.')

def mutation_probe(ns,task):
    with closing(sqlite3.connect(':memory:',autocommit=False,factory=ProbeConnection)) as con:
        baseline=[(7,'Původní',4),(22,'Lana',2)]
        fixture(con,baseline)
        if task==0:
            payload="  Žofie'); DROP TABLE pomucky; --  "
            key=ns['pridej_pomucku'](con,payload,3)
            bindings(con,[payload,3])
            require(type(key) is int and key not in (7,22) and con.execute('SELECT nazev,kusy FROM pomucky WHERE id=?',(key,)).fetchone()==(payload,3),'Vraťte skutečný lastrowid a uložte hodnoty beze změny.')
            key2=ns['pridej_pomucku'](con,'Další',0)
            require(key2!=key,'Každý nový řádek má své id.')
        elif task==1:
            data=[("Kniha O'Neil",0),('  Karty  ',6)]
            before=copy.deepcopy(data)
            require(ns['pridej_vice'](con,iter(data)) is None,'Dávka nic nevrací a přijímá jednorázový iterátor.')
            bindings(con,[x for row in data for x in row])
            require(con.execute("SELECT nazev,kusy FROM pomucky WHERE id>22 ORDER BY id").fetchall()==data and data==before,'Vložte všechny hodnoty beze změny.')
            require(ns['pridej_vice'](con,[]) is None,'Prázdná dávka je platná.')
            try:ns['pridej_vice'](con,[('Před chybou',2),('Chybná',-1)])
            except sqlite3.IntegrityError:pass
            else:require(False,'Chybu dávky předávejte volajícímu, nevynechávejte neplatný řádek potichu.')
        elif task==2:
            require(ns['nastav_pocet'](con,7,9)==1,'Update vrací počet odpovídajících řádků.')
            bindings(con,[7,9])
            require(rows(con)==[(7,'Původní',9),(22,'Lana',2)],'Změňte pouze vybraný záznam.')
            require(ns['nastav_pocet'](con,7,9)==1 and ns['nastav_pocet'](con,999,1)==0,'Počítají se nalezené řádky i při stejné hodnotě.')
        elif task==3:
            require(ns['smaz_pomucku'](con,7)==1,'Delete vrací počet smazaných řádků.')
            bindings(con,[7])
            require(rows(con)==[(22,'Lana',2)],'Ostatní záznamy zůstávají.')
            require(ns['smaz_pomucku'](con,7)==0 and ns['smaz_pomucku'](con,'22 OR 1=1')==0,'Nenalezený id ani text podobný SQL nesmaže jiný záznam.')
        else:
            require(ns['pridej_pokud_chybi'](con,'Karty',3) is True,'Nový název se vloží.')
            bindings(con,['Karty',3])
            require(ns['pridej_pokud_chybi'](con,'Karty',99) is False,'Konflikt názvu vrátí False.')
            require(con.execute("SELECT kusy FROM pomucky WHERE nazev='Karty'").fetchone()==(3,),'Konflikt staré kusy nepřepíše.')
            for name,amount in [('Karty',-1),('Jiná',-1),(None,2)]:
                try:ns['pridej_pokud_chybi'](con,name,amount)
                except sqlite3.IntegrityError:pass
                else:require(False,'Ignorujte jen konflikt názvu, ne jiné porušení pravidel.')
        if task in (0,2):
            try:
                ns['pridej_pomucku'](con,'Záporná',-1) if task==0 else ns['nastav_pocet'](con,22,-1)
            except sqlite3.IntegrityError:pass
            else:require(False,'Chybu integritních pravidel neskrývejte.')
        require(not con.was_closed,'Spojení vlastní volající.')
        con.rollback()
        require(rows(con)==baseline,'Tyto funkce nemají samy commitovat: rollback volajícího vrátí všechny jejich změny.')

def reading_probe(ns,task):
    for baseline in [[],[(41,'Šachy',0),(9,'Míče',3),(25,'Lana',3),(2,'Ada',1)]]:
        with closing(sqlite3.connect(':memory:',autocommit=False,factory=ProbeConnection)) as con:
            fixture(con,baseline)
            if not baseline:
                name=['vypis_pomucky','najdi_pomucku','malo_na_sklade','prehled_jako_slovniky','stranka_pomucek'][task]
                args=[(),(999,),(10,),(),(2,)][task]
                require(ns[name](con,*args)==(None if task==1 else []),'Prázdná tabulka vrací [] pro seznamy, fetchone vrací None.')
            # Nepotvrzený řádek odhalí i nechtěný commit ve čtecí funkci.
            pending=(100,'Rozpracované',2)
            con.execute('INSERT INTO pomucky(id,nazev,kusy) VALUES(?,?,?)',pending)
            data=baseline+[pending]
            con.events.clear()
            if task==0:
                got=ns['vypis_pomucky'](con)
                require(got==sorted(data,key=lambda r:(r[1],r[0])),'Vraťte seznam (id,nazev,kusy) s výslovným pořadím názvu a id.')
            elif task==1:
                require(ns['najdi_pomucku'](con,100)==pending and ns['najdi_pomucku'](con,888) is None,'Fetchone dává řádek nebo None.')
                bindings(con,[100])
                require(ns['najdi_pomucku'](con,'100 OR 1=1') is None,'Id zůstává hodnotou parametru.')
            elif task==2:
                for minimum in [0,2,3,20,-1]:
                    con.events.clear()
                    got=ns['malo_na_sklade'](con,minimum)
                    bindings(con,[minimum])
                    require(got==sorted([r for r in data if r[2]<minimum],key=lambda r:(r[2],r[1],r[0])),
                            'Použijte přísnou hranici a pořadí kusy/nazev/id.')
            elif task==3:
                for factory in [None,sqlite3.Row]:
                    con.row_factory=factory
                    got=ns['prehled_jako_slovniky'](con)
                    require(got==[dict(zip(['id','nazev','kusy'],r)) for r in sorted(data)],'Výstup jsou obyčejné slovníky v pořadí id.')
                    require(con.row_factory is factory,'Nastavení spojení patří volajícímu; použijte lokální kurzor nebo je obnovte.')
                con.row_factory=None
            else:
                for limit,offset in [(0,0),(1,0),(2,1),(8,0),(2,99)]:
                    con.events.clear()
                    got=ns['stranka_pomucek'](con,limit,offset)
                    bindings(con,[limit,offset])
                    require(got==sorted(data)[offset:offset+limit],'Limit/offset pracují nad pořadím id.')
                for limit,offset in [(-1,0),(1,-1),(True,0),(2,False),(1.2,0)]:
                    try:ns['stranka_pomucek'](con,limit,offset)
                    except ValueError:pass
                    else:require(False,'Limit/posun jsou nezáporný int, bool není počet.')
            require(con.events,'Odpověď získejte skutečným SQL dotazem.')
            require(not con.was_closed,'Čtení nesmí zavřít předané spojení.')
            con.rollback()
            require(rows(con)==sorted(baseline),'Čtení nesmí potvrdit cizí rozepsanou změnu.')

def transaction_probe(ns,task):
    names=['uloz_davku','odeber_kusy','presun_kusy','pridej_se_zpravou','pokus_bez_ulozeni']
    with tempfile.TemporaryDirectory() as temp:
        path=Path(temp)/'sklad.sqlite3'
        with closing(sqlite3.connect(path,autocommit=False,factory=ProbeConnection)) as con:
            baseline=[(7,'Zdroj',8),(22,'Cíl',2)]
            fixture(con,baseline)
            def outside():
                with closing(sqlite3.connect(path,autocommit=True)) as observer:return rows(observer)
            if task==0:
                require(ns['uloz_davku'](con,iter([("Kniha O'Neil",3),('Karty',0)])) is None,'Dávka nic nevrací a přijme iterátor.')
                bindings(con,["Kniha O'Neil",3,'Karty',0])
                require([r[1:] for r in outside()]==[r[1:] for r in baseline]+[("Kniha O'Neil",3),('Karty',0)],'Celá úspěšná dávka je vidět jinému spojení.')
                before=outside()
                try:ns['uloz_davku'](con,[('První z pokusu',1),('Záporná',-1)])
                except sqlite3.IntegrityError:pass
                else:require(False,'Chybná dávka musí ohlásit chybu.')
                require(outside()==before and rows(con)==before,'Při chybě nezůstane ani první řádek dávky.')
            elif task==1:
                require(ns['odeber_kusy'](con,7,3) is True and outside()==[(7,'Zdroj',5),(22,'Cíl',2)],'Dostupný odběr se uloží a změní jediný řádek.')
                require(ns['odeber_kusy'](con,7,6) is False and ns['odeber_kusy'](con,999,1) is False,'Nedostatek/mizící id vrátí False.')
                require(outside()==[(7,'Zdroj',5),(22,'Cíl',2)],'Neúspěšný odběr nezmění zásobu.')
                require(ns['odeber_kusy'](con,7,5) is True and outside()==[(7,'Zdroj',0),(22,'Cíl',2)],'Přesně dostupné množství lze odebrat celé.')
                for amount in [0,-1,True,1.5]:
                    try:ns['odeber_kusy'](con,7,amount)
                    except ValueError:pass
                    else:require(False,'Počet musí být kladný int bez bool.')
            elif task==2:
                require(ns['presun_kusy'](con,7,22,3) is None and outside()==[(7,'Zdroj',5),(22,'Cíl',5)],'Úspěšný přesun se celý uloží.')
                for args in [(7,999,1),(7,22,99),(999,22,1),(7,7,1),(7,22,0),(7,22,True)]:
                    before=outside()
                    try:ns['presun_kusy'](con,*args)
                    except ValueError:pass
                    else:require(False,'Nemožný přesun musí vyvolat ValueError.')
                    require(rows(con)==before and outside()==before,'Při chybě se vrátí i již odebraný zdroj.')
                bindings(con,[7,22,3])
            elif task==3:
                key=ns['pridej_se_zpravou'](con,"Karty O'Neil",4,'Dar')
                bindings(con,["Karty O'Neil",4,'Dar'])
                require(any(r==(key,"Karty O'Neil",4) for r in outside()),'Pomůcka i její skutečné id se uloží.')
                with closing(sqlite3.connect(path,autocommit=True)) as other:
                    require(other.execute('SELECT popis FROM udalosti').fetchall()==[('Dar',)],'Zpráva se uloží ve stejné transakci.')
                before=outside()
                try:ns['pridej_se_zpravou'](con,'Pokus bez zprávy',2,None)
                except sqlite3.IntegrityError:pass
                else:require(False,'Neplatná zpráva má vyvolat IntegrityError.')
                require(rows(con)==before and outside()==before,'Chyba druhého zápisu vrátí novou pomůcku.')
            else:
                require(ns['pokus_bez_ulozeni'](con,iter([('Pokus',2)]))==3,'Vrácený počet zahrnuje zkušební řádky.')
                require(rows(con)==baseline and outside()==baseline,'Náhled nikdy neukládá změny.')
                try:ns['pokus_bez_ulozeni'](con,[('Zkouška',1),('Chyba',-1)])
                except sqlite3.IntegrityError:pass
                else:require(False,'Chyba zkoušky se předá volajícímu.')
                require(rows(con)==baseline,'Finally vrátí i nedokončenou dávku.')
            require(not con.was_closed,'Transakční funkce spojení nezavírá.')
        with closing(sqlite3.connect(path,autocommit=True,factory=ProbeConnection)) as wrong:
            args=[([],),(7,1),(7,22,1),('Pokus',1,'Zpráva'),([],)][task]
            before=rows(wrong)
            try:ns[names[task]](wrong,*args)
            except ValueError:pass
            else:require(False,'Autocommit=True nechrání celou transakci; odmítněte jej ValueError.')
            require(rows(wrong)==before,'Neplatný transakční režim nic nezmění.')

def over(c,ns,stage,task):
    def probe():
        require(ns is not None,'Nejprve opravte načtení kódu.')
        [connection_probe,schema_probe,mutation_probe,reading_probe,transaction_probe][stage](ns,task)
        return True
    ok,value=c.call({'probe':probe},'probe')
    c.add('Pravidla práce se SQLite',ok and value is True,'' if ok and value is True else f'{type(value).__name__}: {value}')
    result=c.run()
    c.no_error(result)
