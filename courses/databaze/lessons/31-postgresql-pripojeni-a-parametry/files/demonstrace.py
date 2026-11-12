"""Označená výuková simulace dvou dotazů, nikoli PostgreSQL ani obecný SQL stroj.
Skutečné SQL, izolaci a pool ověřujte samostatně proti vlastnímu serveru.
"""
from contextlib import contextmanager
import copy
import re

class DemoIntegrita(ValueError):
    pass

class DemoCursor:
    def __init__(self,con):self.con=con;self.radky=[];self.closed=False
    def __enter__(self):return self
    def __exit__(self,*exc):self.closed=True
    def execute(self,sql,params=None):
        self.radky=self.con.dotaz(sql,params)
        return self
    def fetchone(self):return self.radky[0] if self.radky else None
    def fetchall(self):return list(self.radky)

class DemoSpojeni:
    def __init__(self):
        self.radky=[];self.dalsi_id=1;self.closed=False;self.hloubka=0
        self.udalosti=[];self.autocommit=True
    @contextmanager
    def transaction(self):
        if self.closed:raise RuntimeError('Spojení je zavřené.')
        stav=copy.deepcopy(self.radky);self.hloubka+=1;self.udalosti.append('zacatek')
        try:yield
        except BaseException:
            self.radky=stav;self.udalosti.append('rollback');raise
        else:self.udalosti.append('uspech')
        finally:self.hloubka-=1
    def cursor(self):return DemoCursor(self)
    def execute(self,sql,params=None):return self.cursor().execute(sql,params)
    def dotaz(self,sql,params):
        if self.closed:raise RuntimeError('Spojení je zavřené.')
        if not self.hloubka:raise AssertionError('Operace musí být v transaction().')
        text=re.sub(r'\s+',' ',str(sql).replace('"','').strip()).lower()
        text=re.sub(r'\b[a-z_]\w*\.', '', text)
        text=re.sub(r'from akademie_pomucky(?: as)? [a-z_]\w* where', 'from akademie_pomucky where', text)
        self.udalosti.append(('sql',text,params))
        if text.startswith('insert into akademie_pomucky') and re.search(r'returning id(?: as \w+)?;?$',text):
            if not re.search(r'values\s*\(\s*%s\s*,\s*%s\s*\)',text) or not isinstance(params,(tuple,list)) or len(params)!=2:
                raise AssertionError('Hodnoty předejte odděleně jako dva parametry %s.')
            columns=re.match(r'insert into akademie_pomucky\s*\((.*?)\)',text)
            fields=[x.strip() for x in columns[1].split(',')] if columns else []
            if len(fields)!=2 or set(fields)!={'nazev','kusy'}:raise AssertionError('INSERT má dvě pole nazev a kusy.')
            data=dict(zip(fields,params));nazev,kusy=data['nazev'],data['kusy']
            ident=self.dalsi_id;self.dalsi_id+=1
            if any(r[1]==nazev for r in self.radky):raise DemoIntegrita('Stejný název už existuje.')
            self.radky.append((ident,nazev,kusy));return [(ident,)]
        if text.startswith('select ') and 'from akademie_pomucky' in text:
            projection=text.split(' from ',1)[0][7:]
            if projection.strip()!='*' and [x.strip() for x in projection.split(',')]!=['id','nazev','kusy']:
                raise AssertionError('SELECT musí vrátit id, nazev a kusy v tomto pořadí.')
            if not re.search(r'where kusy\s*>=\s*%s',text) or not isinstance(params,(tuple,list)) or len(params)!=1 or not re.search(r'order by (?:\w+\.)?id(?: asc)?(?:;|$)',text):
                raise AssertionError('Použijte filtr kusy >= %s s parametrem a pořadí podle id.')
            return sorted([r for r in self.radky if r[2]>=params[0]])
        raise AssertionError('Simulace podporuje jen dva dotazy ze zadání.')
    def close(self):self.closed=True

class DemoPool:
    def __init__(self):self.con=DemoSpojeni();self.vypujceno=0;self.prevzeti=0;self.vraceni=0;self.closed=False
    @contextmanager
    def connection(self,timeout=3):
        if self.closed or self.con.closed:raise RuntimeError('Pool/spojení je zavřené.')
        if timeout!=3:raise AssertionError('Převzetí má limit 3 sekundy.')
        self.vypujceno+=1;self.prevzeti+=1
        try:yield self.con
        finally:self.vypujceno-=1;self.vraceni+=1
    def close(self):self.closed=True;self.con.close()
