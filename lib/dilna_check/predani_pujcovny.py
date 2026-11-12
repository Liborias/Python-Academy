"""Luhn, volitelný QR, účinné vlastní testy, předání a závěrečná půjčovna."""
import base64
from contextlib import closing
import csv
import io
from pathlib import Path
import sqlite3
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from .sqlite_intro import ProbeConnection,require


def odmita(call,typ=ValueError):
    try:call()
    except typ:return
    require(False,f'Očekávám {typ.__name__}.')


def cislice(telo):
    soucet=0
    for i,c in enumerate(telo[::-1]):
        n=int(c)*(2 if i%2==0 else 1)
        soucet+=n//10+n%10
    return str((-soucet)%10)


def luhn(ns):
    for telo in ['0','7','12','0007','109','12345678901234567890123456789012']:
        k=telo+cislice(telo)
        require(ns['kontrolni_cislice'](telo)==k[-1] and ns['platny_kod'](k) is True,'Zachovejte ASCII číslice, úvodní nuly a správnou paritu zprava.')
        for i in range(len(k)):
            spatne=k[:i]+str((int(k[i])+1)%10)+k[i+1:]
            require(ns['platny_kod'](spatne) is False,'Změnu jedné číslice je třeba odhalit.')
    for telo in ['',None,123,True,'1 2','+12','１２','١٢','0'*33]:odmita(lambda:ns['kontrolni_cislice'](telo))
    for kod in ['',None,12,True,'1','１２','١٢','0'*34]:require(ns['platny_kod'](kod) is False,'Neplatný formát vrací False.')
    require(ns['platny_kod']('1099') and ns['platny_kod']('1909'),'Nezaměňujte kontrolní číslici s důkazem správného předmětu.')
    return True


def qr(ns):
    events=[]
    pixel=base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jP2sAAAAASUVORK5CYII=')
    class Image:
        def save(self,path,**kw):
            events.append(('save',kw));Path(path).write_bytes(pixel)
    class QR:
        def __init__(self,**kw):events.append(('init',kw))
        def add_data(self,data):events.append(('data',data))
        def make(self,**kw):events.append(('fit',kw))
        def make_image(self,**kw):events.append(('colors',kw));return Image()
    def make(data,**kw):
        q=QR(**kw);q.add_data(data);q.make(fit=True);return q.make_image(fill_color='black',back_color='white')
    fake=SimpleNamespace(QRCode=QR,make=make,constants=SimpleNamespace(ERROR_CORRECT_M=0))
    with tempfile.TemporaryDirectory() as temp:
        p=Path(temp)/'Český štítek.png';text='  Žofie; štítek\ndruhý řádek  '
        with patch.dict(ns,{'ziskej_qrcode':lambda:None}):
            require(ns['qr_png'](text,p) is None and not p.exists(),'Chybějící volitelná knihovna nic nezapisuje.')
        with patch.dict(ns,{'ziskej_qrcode':lambda:fake}):
            require(ns['qr_png'](text,p)==p.resolve() and p.read_bytes()==pixel,'Vraťte absolutní PNG Path.')
            require(('data',text.encode('utf-8')) in events,'QR obsah je přesný UTF-8 včetně mezer.')
            require(any(kind=='init' and all(settings.get(k)==v for k,v in {'error_correction':0,'box_size':6,'border':4}.items()) for kind,settings in events) and ('fit',{'fit':True}) in events,'Použijte profil M, modul6, okraj4 a fit=True.')
            require(('colors',{'fill_color':'black','back_color':'white'}) in events and ('save',{'format':'PNG'}) in events,'Kontrastní PNG se ukládá s výslovným formátem.')
            odmita(lambda:ns['qr_png'](text,p,zdroj=p))
            for text in ['',None,' '*5,'ž'*257,'\ud800']:odmita(lambda:ns['qr_png'](text,p))
            odmita(lambda:ns['qr_png']('text',Path(temp)/'soubor.svg'))
            p.write_bytes(b'predchozi')
            def failed(self,path,**kw):Path(path).write_bytes(b'cast');raise OSError('Řízené selhání PNG')
            with patch.object(Image,'save',failed):odmita(lambda:ns['qr_png']('text',p),OSError)
            require(p.read_bytes()==b'predchozi' and not list(Path(temp).glob('.bmi-*')),'Chyba nezničí starý cíl a uklidí dočasný soubor.')
    return True


def sada(ns):
    from model import Pujcovna
    def run(Model):
        suite=ns['vytvor_sadu'](Model)
        require(isinstance(suite,unittest.TestSuite) and suite.countTestCases()>=6,'Vraťte alespoň šest unittest případů.')
        out=io.StringIO();r=unittest.TextTestRunner(stream=out).run(suite)
        return r,out.getvalue()
    result,out=run(Pujcovna)
    require(result.wasSuccessful() and not result.skipped,'Správný model musí projít bez skip.\n'+out[-1200:])
    class BezCommit(Pujcovna):
        def pridej_pomucku(self,nazev,kusy,kategorie_id=None):
            return self.con.execute('INSERT INTO pomucky(nazev,kusy,kategorie_id) VALUES(?,?,?)',(nazev.strip(),kusy,kategorie_id)).lastrowid
    class BezPoctu(Pujcovna):
        def pujc(self,ident,clen):
            row=self.con.execute('SELECT kusy FROM pomucky WHERE id=?',(ident,)).fetchone()
            if row and row[0]==0:
                with self.con:return self.con.execute('INSERT INTO vypujcky(pomucka_id,clen) VALUES(?,?)',(ident,clen)).lastrowid
            return super().pujc(ident,clen)
    class DvojiteVraceni(Pujcovna):
        def vrat(self,ident):
            row=self.con.execute('SELECT pomucka_id,vraceno FROM vypujcky WHERE id=?',(ident,)).fetchone()
            if row and row[1]:
                with self.con:self.con.execute('UPDATE pomucky SET kusy=kusy+1 WHERE id=?',(row[0],))
                return True
            return super().vrat(ident)
    class BezCislice(Pujcovna):
        def id_z_kodu(self,kod):
            if isinstance(kod,str) and len(kod)>1 and kod.isascii() and kod.isdigit():
                i=int(kod[:-1])
                if not ns['platny_kod'](kod) and any(r[0]==i for r in self.prehled()):return i
            return super().id_z_kodu(kod)
    class BezApostrofu(Pujcovna):
        def pridej_pomucku(self,nazev,kusy,kategorie_id=None):return super().pridej_pomucku(nazev.replace("'",''),kusy,kategorie_id)
    class BezRollback(Pujcovna):
        def pujc(self,ident,clen):
            row=self.con.execute('SELECT kusy FROM pomucky WHERE id=?',(ident,)).fetchone()
            if row and row[0]>0:
                with self.con:self.con.execute('UPDATE pomucky SET kusy=kusy-1 WHERE id=?',(ident,))
                with self.con:return self.con.execute('INSERT INTO vypujcky(pomucka_id,clen) VALUES(?,?)',(ident,clen)).lastrowid
            return super().pujc(ident,clen)
    for cls,name in [(BezCommit,'trvalost'),(BezPoctu,'nedostupný kus'),(DvojiteVraceni,'druhé vrácení'),
                     (BezCislice,'kontrolní číslice'),(BezApostrofu,'přesný název'),(BezRollback,'celý rollback')]:
        result,_=run(cls);require(not result.wasSuccessful(),f'Vaše testy neodhalí poruchu: {name}.')
    return True


def paths_backup(ns):
    from model import Pujcovna
    with tempfile.TemporaryDirectory() as temp:
        root=Path(temp);script=root/'neexistující složka'/'app.py'
        got=ns['cesty_projektu'](script)
        require(got=={'koren':script.parent,'db':script.with_name('pujcovna.sqlite3')},'Výchozí DB patří vedle skriptu, ne do cwd.')
        require(not script.parent.exists(),'Výpočet cest nic nezapisuje.')
        relative=ns['cesty_projektu'](script,'externí.sqlite3')
        require(relative['db']==(Path.cwd()/'externí.sqlite3').resolve(),'Zadaná relativní cesta je vůči aktuálnímu adresáři.')
        source=root/'zdroj.sqlite3';target=root/'kopie.sqlite3'
        with closing(Pujcovna(source)) as m:
            m.pridej_pomucku('Český míč',2)
            require(ns['zaloha_projektu'](m,target)==target.resolve(),'Vraťte absolutní cílový Path.')
            odmita(lambda:ns['zaloha_projektu'](m,source))
            m.pridej_pomucku('Pozdější',1)
            with closing(Pujcovna(target)) as copy:require(len(copy.prehled())==1,'Kopie je samostatný stav před dalšími změnami.')
        with closing(Pujcovna(':memory:')) as memory:
            memory.pridej_pomucku('Paměť',1);ns['zaloha_projektu'](memory,root/'pamet.sqlite3')
        with closing(Pujcovna(root/'pamet.sqlite3')) as copy:require(len(copy.prehled())==1,'Backup pracuje i z paměti.')
    return True


def final_model(ns):
    Model=ns['MojePujcovna']
    with tempfile.TemporaryDirectory() as temp:
        root=Path(temp);path=root/'pujcovna.sqlite3';out=root/'štítky.csv'
        with closing(Model(path)) as m:
            require(m.karty()==[] and m.souhrn()=={'pomucky':0,'dostupne':0,'vypujceno':0},'Prázdná půjčovna má prázdné karty a nulové počty.')
            require(m.stitky_csv(out)==0,'Prázdný CSV má jen hlavičku.')
            with out.open(encoding='utf-8',newline='') as f:
                empty=csv.DictReader(f,delimiter=';')
                require(empty.fieldnames==['id','nazev','kod','dostupne','vypujceno','celkem'] and list(empty)==[],'I prázdný CSV má přesnou hlavičku bez datových řádků.')
            a=m.pridej_pomucku("Karty O'Neil",2);b=m.pridej_pomucku('Krabice',0)
            with m.con:m.con.execute('INSERT INTO pomucky(id,nazev,kusy) VALUES(37,?,3)',('Míč; "modrý"\nA',))
            old=m.pujc_kod(m.kod(a),'Ada');m.vrat(old)
            m.pujc_kod(m.kod(a),'Žofie');m.pujc_kod(m.kod(37),'Ada');m.pujc_kod(m.kod(37),'Žofie')
            expected=[{'id':i,'nazev':name,'kod':str(i)+cislice(str(i)),'dostupne':free,'vypujceno':loans,'celkem':total}
                      for i,name,free,loans,total in [(a,"Karty O'Neil",1,1,2),(b,'Krabice',0,0,0),(37,'Míč; "modrý"\nA',1,2,3)]]
            require(m.karty()==expected,'Karty mají skutečné id, kód a počet jen aktivních výpůjček; prázdná pomůcka nezmizí.')
            require(m.souhrn()=={'pomucky':3,'dostupne':2,'vypujceno':3},'Souhrn sečte pomůcky, dostupné kusy a aktivní půjčení.')
            require(m.stitky_csv(out)==3,'Export vrací počet karet.')
            with out.open(encoding='utf-8',newline='') as f:
                reader=csv.DictReader(f,delimiter=';');rows=list(reader)
                require(reader.fieldnames==['id','nazev','kod','dostupne','vypujceno','celkem'],'CSV má dohodnutou hlavičku.')
            require(rows==[{k:str(v) for k,v in row.items()} for row in expected],'CSV zachová každé id, název, kód i počet beze změn.')
            odmita(lambda:m.stitky_csv(path))
        with closing(Model(path)) as again:require(again.karty()==expected,'Nový proces zachová celou půjčovnu.')
    return True


def over(c,stage):
    with patch.object(sqlite3,'connect',side_effect=RuntimeError('Import nesmí otevřít databázi.')):ns=c.load()
    def probe():
        require(ns is not None,'Opravte načtení programu.')
        if stage==0:return luhn(ns)
        if stage==1:return qr(ns)
        if stage==2:
            from luhn import platny_kod
            ns['platny_kod']=platny_kod
            return sada(ns)
        if stage==3:return paths_backup(ns)
        return final_model(ns)
    ok,value=c.call({'probe':probe},'probe')
    c.add('Pravidla nástrojů a předání',ok and value is True,'' if ok and value is True else str(value))
    c.no_error(c.run(timeout=12))
