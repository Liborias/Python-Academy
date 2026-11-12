"""Skutečný PostgreSQL smoke. --config ukazuje na soukromý JSON s PG* proměnnými.
Vyžaduje psycopg[binary,pool]>=3.2,<4 a vlastní dočasnou cvičnou DB.
Vytvoří unikátní schéma a v finally smaže pouze toto schéma, ne databázi.
"""
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import uuid
import psycopg
from psycopg import sql
from psycopg.pq import TransactionStatus
from psycopg_pool import PoolTimeout

R=Path(__file__).resolve().parent.parent
B=R/'courses/databaze/lessons'
IDS=['31-postgresql-pripojeni-a-parametry','32-pool-a-sprava-spojeni']

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def main(config):
    settings=json.loads(Path(config).read_text());assert set(settings)<= {'PGHOST','PGPORT','PGDATABASE','PGUSER','PGPASSWORD','PGSSLMODE','PGSSLROOTCERT','PGPASSFILE'}
    assert {'PGHOST','PGPORT','PGDATABASE','PGUSER'}<=set(settings),'Konfigurace musí výslovně určit host, port, databázi a roli.'
    os.environ.update(settings);schema='akademie_test_'+uuid.uuid4().hex
    with psycopg.connect('',autocommit=True,connect_timeout=5) as admin:
        version=admin.execute('SHOW server_version').fetchone()[0]
        admin.execute(sql.SQL('CREATE SCHEMA {}').format(sql.Identifier(schema)))
        try:
            os.environ['PGOPTIONS']='-csearch_path='+schema
            with tempfile.TemporaryDirectory() as tmp:
                works=[]
                for lid in IDS:
                    w=Path(tmp)/lid;shutil.copytree(B/lid/'files',w);shutil.copy(B/lid/'solution.py',w/'reseni.py');works.append(w)
                sys.path.insert(0,str(works[0]));support=load(works[0]/'pg_podpora.py','support_test');model=load(works[0]/'reseni.py','student31')
                with support.pripoj() as con:
                    support.vytvor_tabulku(con)
                    ids=[model.pridej_pg(con,"  Karty O'Neil  ",2),model.pridej_pg(con,'Krabice',0)]
                    assert model.prehled_pg(con)==[(ids[0],"Karty O'Neil",2),(ids[1],'Krabice',0)]
                    assert model.prehled_pg(con,2)==[(ids[0],"Karty O'Neil",2)]
                    try:model.pridej_pg(con,'Krabice',9)
                    except psycopg.errors.UniqueViolation:pass
                    else:raise AssertionError('Duplicitní název prošel.')
                    assert con.info.transaction_status==TransactionStatus.IDLE and not con.closed
                    payload="'); DROP TABLE akademie_pomucky; --"
                    ident=model.pridej_pg(con,payload,1);assert any(r==(ident,payload,1) for r in model.prehled_pg(con))
                assert con.closed
                with support.pripoj() as reopened:assert len(model.prehled_pg(reopened))==3
                sys.path.insert(0,str(works[1]));pooled=load(works[1]/'reseni.py','student32');pool=support.priprav_pool()
                try:
                    batch=pooled.pridej_davku(pool,[('Lano',3),('Stužka',1)]);assert len(batch)==2
                    before=pooled.prehled_z_poolu(pool)
                    try:pooled.pridej_davku(pool,[('Vrátí se',3),('Krabice',1)])
                    except psycopg.errors.UniqueViolation:pass
                    else:raise AssertionError('Dávka s konfliktem prošla.')
                    assert pooled.prehled_z_poolu(pool)==before
                    assert len(pooled.pridej_davku(pool,[('Po chybě',1)]))==1
                    with ThreadPoolExecutor(max_workers=5) as ex:
                        reads=list(ex.map(lambda _:pooled.prehled_z_poolu(pool),range(12)))
                    assert all(rows==reads[0] for rows in reads)
                    with pool.connection(timeout=3) as a,pool.connection(timeout=3) as b,pool.connection(timeout=3) as c:
                        assert len({a.info.backend_pid,b.info.backend_pid,c.info.backend_pid})==3
                        try:pooled.prehled_z_poolu(pool)
                        except PoolTimeout:pass
                        else:raise AssertionError('Převzetí čtvrtého spojení má vypršet.')
                    assert pooled.prehled_z_poolu(pool)==reads[0]
                    stats=pool.get_stats();assert stats['pool_size']<=3 and stats.get('requests_waiting',0)==0
                finally:pool.close()
                assert pool.closed
                def cli(work,*args,expected=0):
                    r=subprocess.run([sys.executable,'-X','utf8',str(work/'spust_postgres.py'),*args],cwd=tmp,capture_output=True,text=True,timeout=20)
                    assert r.returncode==expected,r.stdout+r.stderr
                    assert settings.get('PGPASSWORD','impossible secret') not in r.stdout+r.stderr
                    return r.stdout+r.stderr
                for i,w in enumerate(works):
                    assert 'VÝUKOVÁ SIMULACE' in cli(w)
                    cli(w,'--help');cli(w,'--pripojit','init')
                    cli(w,'--pripojit','pridat','CLI'+str(i), '4')
                    out=cli(w,'--pripojit','prehled','--minimum','4');assert 'CLI'+str(i) in out
                    cli(w,'--pripojit','pridat','CLI'+str(i), '4',expected=2)
                pokus=subprocess.run([sys.executable,'-X','utf8',str(works[1]/'pokus_davky.py'),'--pripojit'],cwd=tmp,capture_output=True,text=True,timeout=20)
                assert pokus.returncode==0 and 'Ověřeno: C neexistuje' in pokus.stdout,pokus.stdout+pokus.stderr
                with support.pripoj() as final:
                    assert final.execute("SELECT COUNT(*) FROM akademie_pomucky WHERE nazev LIKE 'CLI%' ").fetchone()[0]==2
                print('OK: PostgreSQL',version,'/ psycopg',psycopg.__version__)
                print('Parametry/apostrof/SQL text, RETURNING, commit/reopen, skutečný rollback celé dávky a IDLE po chybě.')
                print('Skutečný pool max3, 12 souběžných přehledů, timeout čtvrtého lease, zotavení/close; CLI31/32 v dalších procesech.')
        finally:
            os.environ.pop('PGOPTIONS',None)
            admin.execute(sql.SQL('DROP SCHEMA {} CASCADE').format(sql.Identifier(schema)))

if __name__=='__main__':
    if len(sys.argv)!=3 or sys.argv[1]!='--config':raise SystemExit('Použití: python tests/postgresql_real_smoke.py --config SOUKROMY_JSON')
    main(sys.argv[2])
