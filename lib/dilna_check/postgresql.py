"""Offline kontrakt PostgreSQL operací. Skutečný server má samostatný integrační test."""
import importlib
from .sqlite_intro import require


def odmita(call,typ=ValueError):
    try:call()
    except typ:return
    require(False,f'Očekávána {typ.__name__}.')


def model(ns):
    from demonstrace import DemoSpojeni,DemoIntegrita
    con=DemoSpojeni()
    con.radky=[(37,'Vzdálené id',4),(11,'Krabice',0)];con.dalsi_id=58
    add,read=ns['pridej_pg'],ns['prehled_pg']
    for name,n in [("  Karty O'Neil  ",2),("'); DROP TABLE akademie_pomucky; --",3),('Český míč',1)]:
        ident=add(con,name,n)
        require(type(ident) is int and con.radky[-1]==(ident,name.strip(),n),'Vraťte id z RETURNING a zachovejte název jako parametr.')
    require(read(con)==sorted(con.radky) and read(con,2)==sorted(r for r in con.radky if r[2]>=2),'Vraťte přesné tuple podle id, filtr je včetně minima.')
    before=list(con.radky)
    odmita(lambda:add(con,'Krabice',9),DemoIntegrita)
    require(con.radky==before and not con.closed and con.hloubka==0,'Chyba vrátí transakci, předané spojení zůstane použitelné.')
    require(read(con,1_000_000)==[],'Prázdný výběr vrací [].')
    for name,n in [('',1),(' '*3,0),(None,1),('x'*101,1),('X',True),('X',-1),('X',1.0),('X',1_000_001)]:
        old=len(con.udalosti);odmita(lambda:add(con,name,n));require(len(con.udalosti)==old,'Neplatné hodnoty odmítněte před SQL a transakcí.')
    for n in [None,True,-1,1.0,1_000_001]:odmita(lambda:read(con,n))
    empty=DemoSpojeni();require(read(empty)==[],'Prázdná tabulka vrací [].')
    require(not con.closed and con.hloubka==0,'Spojení vlastní volající; funkce je nezavírá.')
    # Není dovoleno použít jinou tabulku či parametry jen vypsat: simulace zaznamená SQL.
    require(any(isinstance(x,tuple) and "drop table" in str(x[2]).lower() and 'drop table' not in x[1] for x in con.udalosti),'Text se zvláštními znaky patří do parametrů, ne SQL.')
    return True


def pool(ns):
    from demonstrace import DemoPool,DemoIntegrita
    batch,read=ns['pridej_davku'],ns['prehled_z_poolu'];p=DemoPool()
    require(batch(p,[])==[] and p.prevzeti==0,'Prázdná dávka nečerpá spojení.')
    for rows in [None,'text',[('Dobrá',1),('Špatná',-1)],[('X',True)],[('X',1,2)],[('X',1)]*101]:
        odmita(lambda:batch(p,rows));require(p.prevzeti==0,'Celou dávku validujte ještě před převzetím spojení.')
    for n in [None,True,-1,1.0]:odmita(lambda:read(p,n));require(p.prevzeti==0,'Minimum ověřte před převzetím spojení.')
    ids=batch(p,[("  Karty O'Neil  ",2),('Krabice',0)])
    require(len(ids)==2 and len(set(ids))==2 and [r[0] for r in p.con.radky]==ids,'Vraťte id z jednotlivých INSERT v pořadí dávky.')
    require(read(p)==[(ids[0],"Karty O'Neil",2),(ids[1],'Krabice',0)] and read(p,1)==[(ids[0],"Karty O'Neil",2)],'Přehled používá předchozí funkci a správný filtr.')
    old=list(p.con.radky);odmita(lambda:batch(p,[('Míč',3),('Krabice',1)]),DemoIntegrita)
    require(p.con.radky==old,'Pozdější konflikt vrátí celou dávku včetně prvního INSERT.')
    require(not p.closed and not p.con.closed and p.vypujceno==0 and p.prevzeti==p.vraceni,'I po chybě se lease vrací; spojení ani pool funkce nezavírá.')
    again=batch(p,[('Po chybě',1)]);require(len(again)==1 and read(p,1)[-1][1]=='Po chybě','Pool je po rollbacku znovu použitelný; nečekejte souvislá id.')
    class StopPool:
        def connection(self,timeout):raise TimeoutError('Cílené vyčerpání poolu')
    odmita(lambda:read(StopPool()),TimeoutError)
    return True


def over(c,stage):
    ns=c.load()
    def probe():
        require(ns is not None,'Opravte načtení programu.')
        return (model if stage==0 else pool)(ns)
    ok,result=c.call({'probe':probe},'probe')
    c.add('Parametry a životnost spojení' if stage==0 else 'Dávka a vrácení spojení do poolu',ok and result is True,'' if ok and result is True else str(result))
    c.no_error(c.run(timeout=12))
