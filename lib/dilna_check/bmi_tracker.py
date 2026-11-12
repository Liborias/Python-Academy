"""BMI 16–20: jednotky, skutečný SQLite, období, GUI a přenos souborů."""
from contextlib import closing
import csv
import math
from pathlib import Path
import sqlite3
import tempfile
from unittest.mock import patch
from .sqlite_intro import ProbeConnection, bindings, require

DATA=[('2026-04-05',81.123,180.,'Žofie; "poznámka"\ndruhý řádek'),
      ('2024-02-29',90.,200.,'Přestupný den'),('2026-04-01',64.,160.,''),
      ('2026-04-05',82.,200.,'  mezery  ')]
HEADER=['id','datum','hmotnost_kg','vyska_cm','bmi','poznamka']


def odmita(call, typ=ValueError):
    try:
        call()
    except typ:
        return
    require(False, f'Neplatný vstup musí vyvolat {typ.__name__}.')


def blizko(a,b):
    return type(a) in (int,float) and math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-12)


def vypocty(ns):
    require(ns is not None,'Opravte načtení programu.')
    for h,v in [(81,180),(64,160),(50.123,171.23),(100,200)]:
        require(blizko(ns['bmi'](h,v),h/(v/100)**2),'BMI počítejte z kg a metrů, bez předčasného zaokrouhlení.')
    for h,v in [(0,180),(-1,180),(81,0),(True,180),(81,False),('81',180),
                (float('nan'),180),(81,float('inf')),(10**500,180),(1e308,1e-308),(1e-308,1e308)]:
        odmita(lambda:ns['bmi'](h,v))
    for hodnota,expected in [(18.499,'pod 18,5'),(18.5,'18,5 až pod 25'),(24.999,'18,5 až pod 25'),
                             (25,'25 až pod 30'),(29.999,'25 až pod 30'),(30,'30 a více')]:
        require(ns['pasmo'](hodnota)==expected,'Pásma porovnávejte s původní hodnotou, včetně přesných hranic.')
    for value in [0,-1,True,'25',float('nan'),float('inf')]:odmita(lambda:ns['pasmo'](value))
    return True


def trvale(cesta, expected):
    with closing(sqlite3.connect(cesta,autocommit=True)) as other:
        require(other.execute('SELECT id,den,hmotnost,vyska_cm,poznamka FROM mereni ORDER BY den,id').fetchall()==expected,
                'Každé úspěšné přidání musí být potvrzené hned pro druhé spojení.')


def radky_blizko(got, expected):
    require(isinstance(got,list) and len(got)==len(expected),'Vraťte seznam právě vybraných měření.')
    for a,b in zip(got,expected):
        require(len(a)==6 and a[:4]==b[:4] and blizko(a[4],b[4]) and a[5]==b[5],
                'Výpis má id/datum/kg/cm/BMI/poznámku, pořadí datum,id a nezaokrouhlený výpočet.')


def databaze(Model, stage):
    original=sqlite3.connect;opened=[]
    def tracked(*a,**kw):
        kw.setdefault('factory',ProbeConnection)
        con=original(*a,**kw);opened.append(con);return con
    try:
        with patch.object(sqlite3,'connect',side_effect=tracked),tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path=root/'Moje měření.sqlite3'
            with closing(Model(path)) as m:
                require(m.con.autocommit is False,'Model vlastní transakční spojení.')
                require(m.seznam()==[],'Nová databáze začíná prázdná.')
                odmita(lambda:m.pridej('2026-02-29',81,180))
                for day in ['20260401','2026-4-01',' 2026-04-01','2026-W14-3']:
                    odmita(lambda:m.pridej(day,81,180))
                for h,v in [(True,180),(81,0),(float('nan'),180),(81,float('inf'))]:
                    odmita(lambda:m.pridej('2026-04-01',h,v))
                odmita(lambda:m.pridej('2026-04-01',81,180,None))
                expected=[]
                for day,h,v,note in DATA:
                    m.con.events.clear();ident=m.pridej(day,h,v,note)
                    bindings(m.con,[day,h,v,note])
                    expected.append((ident,day,h,v,note));expected.sort(key=lambda r:(r[1],r[0]))
                    trvale(path,expected)  # Před čtením modelem: to by mohlo skrýt chybějící commit.
                require(m.seznam()==expected,'Zachovejte datum,id, hodnoty a přesný text poznámky včetně mezer.')
                if stage>=2:
                    for start,end in [(None,None),('2026-04-05','2026-04-05'),(None,'2026-04-01'),
                                      ('2026-04-02',None),('2030-01-01',None)]:
                        chosen=[r for r in expected if (start is None or r[1]>=start) and (end is None or r[1]<=end)]
                        wanted=[(*r[:4],r[2]/(r[3]/100)**2,r[4]) for r in chosen]
                        m.con.events.clear();radky_blizko(m.prehled(start,end),wanted)
                        if start:bindings(m.con,[start])
                        if end:bindings(m.con,[end])
                        s=m.souhrn(start,end)
                        require(set(s)=={'pocet','prvni_den','posledni_den','prumer_bmi','zmena_kg'},'Souhrn má dohodnuté klíče.')
                        require(s['pocet']==len(chosen) and s['prvni_den']==(chosen[0][1] if chosen else None)
                                and s['posledni_den']==(chosen[-1][1] if chosen else None),'Souhrn odpovídá období a skutečnému pořadí.')
                        require(blizko(s['prumer_bmi'],sum(r[4] for r in wanted)/len(wanted)) if wanted else s['prumer_bmi'] is None,
                                'Průměr jednotlivých BMI není BMI z průměrné hmotnosti a výšky.')
                        require(blizko(s['zmena_kg'],chosen[-1][2]-chosen[0][2]) if chosen else s['zmena_kg'] is None,
                                'Změna kg je poslední minus první záznam podle data,id, ne podle vložení.')
                    for args in [('2026-04-05','2026-04-01'),('',None),('2026-02-29',None)]:
                        odmita(lambda:m.prehled(*args));odmita(lambda:m.souhrn(*args))
                if stage==4:
                    vystup=root/'Český export.csv'
                    require(m.export_csv(vystup,'2026-04-05','2026-04-05')==2,'Export vrací počet datových řádků bez hlavičky.')
                    with vystup.open(encoding='utf-8',newline='') as f: rows=list(csv.reader(f,delimiter=';'))
                    require(rows[0]==HEADER and len(rows)==3,'CSV má středník, přesnou hlavičku a vybrané období.')
                    require(rows[1][5]==DATA[0][3] and rows[2][5]==DATA[3][3],'CSV správně cituje středník, uvozovky, nový řádek a zachová mezery.')
                    require(blizko(float(rows[1][4]),DATA[0][1]/(DATA[0][2]/100)**2) and float(rows[2][4])==20.5,'CSV uchová nezaokrouhlená čísla.')
                    before=vystup.read_bytes()
                    odmita(lambda:m.export_csv(vystup,'2026-04-05','2026-04-01'))
                    require(vystup.read_bytes()==before,'Chyba období nesmaže předchozí export.')
                    require(m.export_csv(vystup,'2030-01-01')==0,'Prázdný export má počet nula.')
                    with vystup.open(encoding='utf-8',newline='') as f:require(list(csv.reader(f,delimiter=';'))==[HEADER],'Prázdný export má stále hlavičku.')
                    for fn in [m.export_csv,m.zaloha]:odmita(lambda:fn(path))
                    cil=root/'kopie.sqlite3';calls=[]
                    def backup(con,target,*a,**kw):
                        calls.append(True);return sqlite3.Connection.backup(con,target,*a,**kw)
                    with patch.object(ProbeConnection,'backup',backup):
                        require(m.zaloha(cil)==cil.resolve(),'Záloha vrací absolutní Path cíle.')
                    require(calls and cil.read_bytes().startswith(b'SQLite format 3\x00'),'Použijte skutečné SQLite backup API, ne CSV ani kopii otevřeného souboru.')
                    m.pridej('2027-01-01',70,180,'Po záloze')
                    with closing(Model(cil)) as copy:require(copy.seznam()==expected,'Záloha je samostatná databáze ve stavu při kopírování.')
                    saved=cil.read_bytes()
                    def failed(con,target,*a,**kw):
                        target.execute('CREATE TABLE nedokoncena_kopie(x)')
                        raise sqlite3.OperationalError('Řízené selhání backup')
                    with patch.object(ProbeConnection,'backup',failed):odmita(lambda:m.zaloha(cil),sqlite3.Error)
                    require(cil.read_bytes()==saved and not list(root.glob('.bmi-*')),'Neúspěšná záloha zachová starý cíl a uklidí dočasný soubor.')
                    with closing(Model(':memory:')) as memory:
                        memory.pridej('2026-04-01',64,160)
                        memory.zaloha(root/'pamet.sqlite3')
                    with closing(Model(root/'pamet.sqlite3')) as copy:require(len(copy.seznam())==1,'Backup funguje i z paměti.')
            m.close()
            with closing(Model(path)) as reopened:require(len(reopened.seznam())==(5 if stage==4 else 4),'Nový model zachová data.')
            odmita(lambda:m.seznam(),sqlite3.ProgrammingError)
            if stage>=2:
                with closing(Model(':memory:')) as velke:
                    velke.pridej('2026-04-01',1e308,100)
                    velke.pridej('2026-04-02',1e308,100)
                    require(velke.souhrn()['prumer_bmi']==1e308, 'Průměr velkých konečných hodnot nesmí přetéct v mezisoučtu.')
        require(opened and all(c.was_closed for c in opened),'Zavřete všechna vlastní spojení.')
    finally:
        for con in opened:con.close()
    return True


def named(r,name,index=-1):return next((w for w in r.widgets(index=index) if w.get('name')==name),{})
def fill(name,value):return {'action':'fill','name':name,'value':value}
def click(text):return {'action':'click','text':text}


def formular(c):
    actions=[fill('den','2026-02-29'),fill('hmotnost','72,5'),fill('poznamka','Rozepsáno'),click('Uložit měření'),
             fill('den','2026-04-03'),click('Uložit měření'),
             fill('od','2026-04-03'),fill('do','2026-04-03'),click('Použít období'),
             fill('od','2026-05-01'),click('Použít období'),click('Všechna měření'),
             fill('od','2030-01-01'),click('Použít období')]
    r=c.tk_run(actions)
    if not c.tk_no_error(r):return
    c.add('Jedno viditelné okno a smyčka',len(r.widgets('root'))==1 and r.mainloops==1 and r.widgets('root')[0]['visible'])
    c.add('Chybné datum zachová obě pole a poznámku',named(r,'hmotnost',4).get('value')=='72,5'
          and named(r,'poznamka',4).get('value')=='Rozepsáno' and len(named(r,'mereni',4).get('items',[]))==2)
    c.add('Česká čárka se uloží až po opravě',len(named(r,'mereni',6).get('items',[]))==3
          and named(r,'hmotnost',6).get('value')=='' and named(r,'poznamka',6).get('value')=='')
    c.add('Obě hranice období jsou včetně',named(r,'mereni',9).get('items')==['3: 2026-04-03 | 72.5 kg / 180 cm | BMI 22.38'])
    c.add('Chybný filtr nezmění přehled',named(r,'mereni',11).get('items')==named(r,'mereni',9).get('items')
          and named(r,'stav',11).get('text')=='Začátek období nesmí být po konci.')
    c.add('Všechna měření vrátí data i vyčistí filtr',len(named(r,'mereni',12).get('items',[]))==3
          and named(r,'od',12).get('value')=='' and named(r,'do',12).get('value')=='')
    c.add('Prázdné období je platný výsledek',named(r,'mereni').get('items')==[]
          and named(r,'souhrn').get('text')=='Počet: 0 | Průměr BMI: —')


def over(c, stage):
    with patch.object(sqlite3,'connect',side_effect=RuntimeError('Import nesmí otevírat databázi.')):
        ns=c.load()
    if stage==3:
        formular(c)
    else:
        def probe():
            require(ns is not None,'Opravte načtení programu.')
            return vypocty(ns) if stage==0 else databaze(ns['Tracker'],stage)
        ok,value=c.call({'probe':probe},'probe')
        c.add('Pravidla výpočtu a měření',ok and value is True,'' if ok and value is True else str(value))
        c.no_error(c.run())
