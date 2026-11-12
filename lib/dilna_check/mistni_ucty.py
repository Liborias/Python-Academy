"""Místní účty 21–25: skutečný scrypt/SQLite, oddělené poznámky, řeč a kodek."""
from contextlib import closing
import base64
import copy
import hashlib
import hmac
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
from unittest.mock import patch
import zlib
from .sqlite_intro import ProbeConnection, bindings, require

HESLO='  Cvičná fráze Žofie!  '
JINE='Jiné cvičné heslo!'
PARAM={'verze':1,'algoritmus':'scrypt','n':2**17,'r':8,'p':1,'dklen':32}


def odmita(call,typ=ValueError):
    try:call()
    except typ:return
    require(False,f'Očekávám {typ.__name__}.')


def hesla(ns,calls,compares):
    a=ns['vytvor_zaznam'](HESLO);b=ns['vytvor_zaznam'](HESLO)
    for record in [a,b]:
        require(isinstance(record,dict) and set(record)==set(PARAM)|{'sul','otisk'},'Záznam obsahuje pouze pevný profil, sůl a otisk.')
        require(all(type(record[k]) is type(v) and record[k]==v for k,v in PARAM.items()),'Verze a scrypt parametry odpovídají pevnému profilu.')
        require(len(bytes.fromhex(record['sul']))==16 and len(bytes.fromhex(record['otisk']))==32,'Sůl 16 bajtů, otisk 32 bajtů; obojí hex.')
    require(a['sul']!=b['sul'] and a['otisk']!=b['otisk'],'Každé vytvoření potřebuje novou náhodnou sůl.')
    require(calls and calls[0][0]==HESLO.encode('utf-8') and all(calls[0][1].get(k)==v for k,v in [('n',2**17),('r',8),('p',1),('dklen',32)]),'Použijte skutečný scrypt a přesné bajty hesla.')
    require(ns['over_heslo'](HESLO,a) is True and ns['over_heslo'](HESLO.strip(),a) is False,'Heslo se neořezává, stejný text projde, jiný ne.')
    bad=copy.deepcopy(a);bad['n']=2**30
    count=len(calls)
    require(ns['over_heslo'](HESLO,bad) is False and len(calls)==count,'Neznámý profil odmítněte ještě před výpočtem.')
    for record in [None,{},dict(a,sul='zz'),dict(a,otisk='00'),dict(a,verze=True)]:
        require(ns['over_heslo'](HESLO,record) is False,'Poškozený záznam není úspěšné ověření.')
    for pw in ['',None,True,'kratke','x'*257,'\ud800'*12]:
        odmita(lambda:ns['vytvor_zaznam'](pw))
        require(ns['over_heslo'](pw,a) is False,'Neplatný text hesla odmítněte.')
    require(compares,'Použijte hmac.compare_digest.')
    return True


def trvale(path,expected):
    with closing(sqlite3.connect(path,autocommit=True)) as con:
        require(con.execute('SELECT id,jmeno FROM uzivatele ORDER BY id').fetchall()==expected,'Registraci musí hned vidět jiné spojení.')


def model(ns,stage):
    original=sqlite3.connect;opened=[]
    def connect(*a,**kw):
        kw.setdefault('factory',ProbeConnection);con=original(*a,**kw);opened.append(con);return con
    try:
        with patch.object(sqlite3,'connect',connect),tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'České účty.sqlite3'
            with closing(ns['Ucty'](path)) as m:
                require(m.con.autocommit is False and m.con.execute('PRAGMA foreign_keys').fetchone()==(1,),'Model vlastní transakční spojení a vynucuje vazby.')
                require(m.seznam()==[],'Nová databáze je prázdná.')
                m.con.events.clear();a=m.registruj('  ŽOFIE  ',HESLO);bindings(m.con,['žofie'])
                trvale(path,[(a,'žofie')])
                ulozene=m.con.execute('SELECT overeni FROM uzivatele WHERE id=?',(a,)).fetchone()[0]
                record=json.loads(ulozene)
                require(set(record)==set(PARAM)|{'sul','otisk'} and record.get('algoritmus')=='scrypt' and HESLO not in ulozene and HESLO.strip() not in ulozene,'DB obsahuje ověřovací záznam, nikoli heslo.')
                expected=hashlib.scrypt(HESLO.encode('utf-8'),salt=bytes.fromhex(record['sul']),n=2**17,r=8,p=1,dklen=32,maxmem=256*1024*1024)
                require(hmac.compare_digest(expected,bytes.fromhex(record['otisk'])),'Registrace musí uložit otisk právě předaného hesla.')
                odmita(lambda:m.registruj('Žofie',JINE),sqlite3.IntegrityError)
                for jmeno,pw in [('',HESLO),('x'*65,HESLO),('Validní','krátké')]:odmita(lambda:m.registruj(jmeno,pw))
                require(m.seznam()==[(a,'žofie')],'Chybná a duplicitní registrace nepřidá účet.')
                if stage==2:
                    b=m.registruj("Ada O'Neil",JINE)
                    require(m.prihlaseni("  ADA O'NEIL  ",JINE)==(b,"ada o'neil"),'Jméno normalizujte, hodnoty jsou SQL parametry.')
                    require(m.prihlaseni("' OR 1=1 --",HESLO) is None,'Neznámé jméno není SQL příkaz.')
                    s=ns['Sezeni'](m)
                    odmita(lambda:s.seznam(),PermissionError);odmita(lambda:s.uloz('Bez přihlášení'),PermissionError)
                    require(s.prihlas('Žofie',HESLO) is True and s.uzivatel==(a,'žofie'),'Úspěch nastaví pouze id/jméno.')
                    note='  Žofie; poznámka\ndruhý řádek  '
                    require(s.uloz(note)==1 and s.seznam()[0][1]==note,'Poznámka zachová přesný obsah.')
                    before=s.seznam()
                    odmita(lambda:s.importuj(['Nesmí se částečně uložit','   ']))
                    require(s.seznam()==before,'Neplatná dávka zachová původní poznámky.')
                    require(s.prihlas('Žofie',JINE) is False and s.uzivatel is None,'Neúspěšný další pokus musí odhlásit starou identitu.')
                    odmita(lambda:s.seznam(),PermissionError)
                    require(s.prihlas("Ada O'Neil",JINE) is True and s.seznam()==[],'Jiný uživatel nevidí cizí poznámky.')
                    s.uloz('Poznámka Ady')
                    require(len(s.seznam())==1 and s.seznam()[0][1]=='Poznámka Ady','Dotaz filtruje id vlastníka.')
                    s.odhlas();odmita(lambda:s.importuj(['Bez identity']),PermissionError)
                    other=ns['Sezeni'](m);require(other.uzivatel is None,'Nové sezení nezačíná přihlášené.')
                    # Skutečná chyba uprostřed dávky musí vrátit i předchozí INSERT.
                    with m.con:m.con.execute("CREATE TRIGGER stop_poznamka BEFORE INSERT ON poznamky WHEN NEW.text='STOP' BEGIN SELECT RAISE(ABORT,'zkouška'); END")
                    odmita(lambda:m.zapis(a,['První část','STOP']),sqlite3.IntegrityError)
                    require(m.cti(a)==before,'Chyba druhého INSERT vrátí první část dávky.')
                    require(m.prihlaseni('Žofie',HESLO)==(a,'žofie'),'Po chybách zůstává přihlášení funkční.')
                    with m.con:m.con.execute('UPDATE uzivatele SET overeni=? WHERE id=?',('{',a))
                    require(m.prihlaseni('Žofie',HESLO) is None,'Poškozený ověřovací JSON se odmítne.')
            m.close()
            with closing(ns['Ucty'](path)) as znovu:require(znovu.seznam()[0]==(a,'žofie'),'Nové otevření zachová účet.')
            odmita(lambda:m.seznam(),sqlite3.ProgrammingError)
        require(opened and all(c.was_closed for c in opened),'Zavřete všechna vlastní spojení.')
    finally:
        for con in opened:con.close()
    return True


def rec(ns):
    text="  Ahoj; $(není příkaz) ' poznámka\nŽofie  "
    with patch.object(subprocess,'run') as run:
        require(ns['precti'](text)=='nahled' and not run.called,'Výchozí běh je pouze náhled bez subprocessu.')
    with patch.dict(ns,{'vyber_prikaz':lambda:None}):require(ns['precti'](text,mluv=True)=='nedostupne','Absence hlasu má srozumitelný stav.')
    with patch.dict(ns,{'vyber_prikaz':lambda:['/hlas','--stdin']}),patch.object(subprocess,'run') as run:
        require(ns['precti'](text,mluv=True)=='precteno' and run.call_count==1,'Explicitní volba spustí jeden místní program.')
        args,kw=run.call_args
        require(args==(['/hlas','--stdin'],) and kw.get('input')==text and kw.get('encoding')=='utf-8'
                and kw.get('check') is True and kw.get('errors')=='replace' and kw.get('timeout')==15 and not kw.get('shell',False),
                'Pevné argv bez shellu, přesný text přes UTF-8 stdin, timeout a kontrola návratového kódu.')
    for error in [FileNotFoundError('není hlas'),subprocess.CalledProcessError(1,['hlas']),subprocess.TimeoutExpired(['hlas'],15)]:
        with patch.dict(ns,{'vyber_prikaz':lambda:['/hlas']}),patch.object(subprocess,'run',side_effect=error):
            require(ns['precti'](text,mluv=True)=='nedostupne','Selhání hlasového programu neohlašuje přečtení.')
    # Skutečný podproces simuluje diagnostiku v jiném kódování, bez hlasu.
    argv=[sys.executable,'-c',"import sys;sys.stderr.buffer.write(bytes([255]));sys.exit(1)"]
    with patch.dict(ns,{'vyber_prikaz':lambda:argv}):
        require(ns['precti']('Krátká ukázka.',mluv=True)=='nedostupne','Cizí kódování chybového výstupu nesmí způsobit pád.')
    for text in ['',None,' '*4,'x'*2001]:odmita(lambda:ns['precti'](text))
    return True


def kodek(ns):
    require(ns is not None,'Opravte načtení programu.')
    for text in ['', 'Žofie\n\t"; zkouška', ' '*50,'A'*65536,'ž'*32768]:
        packed=ns['zabal_text'](text)
        require(isinstance(packed,str) and packed.startswith('z1:') and packed.isascii(),'Výstup má verzi z1: a ASCII Base64.')
        require(zlib.decompress(base64.b64decode(packed[3:],validate=True)).decode('utf-8')==text,'Balíček má skutečný UTF-8/zlib/Base64 formát.')
        require(ns['rozbal_text'](packed)==text,'Přenos zachová přesný text včetně mezer a prázdného vstupu.')
    for text in [None,b'text','A'*65537,'ž'*32769,'\ud800']:odmita(lambda:ns['zabal_text'](text))
    def pack(data):return 'z1:'+base64.b64encode(data).decode('ascii')
    data=zlib.compress(b'validni')
    for value in [None,'','z2:abc','z1:$$$',pack(b'neni zlib'),pack(data[:-1]),pack(data+b'navic'),
                  pack(data+zlib.compress(b'dalsi')),pack(zlib.compress(b'\xff')),pack(zlib.compress(b'A'*65537)),
                  'z1:'+'A'*100001]:odmita(lambda:ns['rozbal_text'](value))
    # Dekodér musí uvést limit výstupu; rozbalení celého obsahu před kontrolou není omezení paměti.
    original=zlib.decompressobj;limits=[]
    class Limited:
        def __init__(self,*a,**kw):self.obj=original(*a,**kw)
        def __getattr__(self,name):return getattr(self.obj,name)
        def decompress(self,data,max_length=0):
            limits.append(max_length);return self.obj.decompress(data,max_length)
    with patch.object(zlib,'decompressobj',Limited):
        require(ns['rozbal_text'](pack(zlib.compress(b'abc')))=='abc','Platný záznam se čte i s měřením limitu.')
    require(limits and all(0<n<=65537 for n in limits),'Rozbalujte s max_length, ne neomezeně před kontrolou délky.')
    return True


def over(c,stage):
    calls=[];compares=[]
    original_scrypt=hashlib.scrypt;original_compare=hmac.compare_digest
    def tracked(*args,**kw):
        calls.append((args[0] if args else kw.get('password'),kw))
        return original_scrypt(*args,**kw)
    def compared(*args,**kw):
        compares.append(True)
        return original_compare(*args,**kw)
    # Patch už při importu podchytí i správné varianty from hashlib/hmac import.
    with patch.object(hashlib,'scrypt',tracked),patch.object(hmac,'compare_digest',compared):
        with patch.object(sqlite3,'connect',side_effect=RuntimeError('Import nesmí otevírat databázi.')):
            ns=c.load()
        def probe():
            require(ns is not None,'Opravte načtení programu.')
            if stage==0:return hesla(ns,calls,compares)
            if stage in (1,2):return model(ns,stage)
            if stage==3:return rec(ns)
            return kodek(ns)
        ok,value=c.call({'probe':probe},'probe')
        c.add('Pravidla místních účtů a souborů',ok and value is True,'' if ok and value is True else str(value))
    c.no_error(c.run(timeout=12))
