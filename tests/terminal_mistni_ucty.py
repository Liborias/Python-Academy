"""Linux PTY: skutečný getpass bez echa a export/import mezi uloženými kroky."""
import errno,os,pty,select,shutil,sqlite3,subprocess,sys,tempfile,time
from pathlib import Path
from contextlib import closing
ROOT=Path(__file__).resolve().parent.parent
PW='Řízená fráze do cvičení!'
WRONG='Jiná fráze do cvičení!'
IDS=['23-mistni-prihlaseni-a-poznamky','25-zlib-base64-a-prenos-poznamek']
python=os.environ.get('DILNA_TEST_PYTHON') or sys.executable

def terminal(entry,args,answers,expected=0):
    pid,fd=pty.fork()
    if pid==0:
        os.execv(python,[python,'-X','utf8',str(entry),*args])
    output=b'';cursor=0;pending=list(answers);deadline=time.monotonic()+20
    try:
        while True:
            if time.monotonic()>deadline:raise AssertionError('Terminál neodpověděl v limitu.')
            ready,_,_=select.select([fd],[],[],0.1)
            if ready:
                try:part=os.read(fd,65536)
                except OSError as e:
                    if e.errno==errno.EIO:break
                    raise
                if not part:break
                output+=part
            if pending:
                prompt,value=pending[0];at=output.find(prompt.encode('utf-8'),cursor)
                if at>=0:
                    cursor=at+len(prompt.encode('utf-8'));pending.pop(0)
                    os.write(fd,(value+'\n').encode('utf-8'))
        _,status=os.waitpid(pid,0);code=os.waitstatus_to_exitcode(status)
        text=output.decode('utf-8','replace')
        assert not pending,(pending,text)
        assert code==expected,(code,text)
        assert PW not in text and WRONG not in text,'Getpass nesmí zobrazit zadanou frázi.'
        return text
    except BaseException:
        try:os.kill(pid,15)
        except ProcessLookupError:pass
        try:os.waitpid(pid,0)
        except ChildProcessError:pass
        raise
    finally:os.close(fd)

with tempfile.TemporaryDirectory() as temp:
    root=Path(temp);works=[]
    for lid in IDS:
        d=ROOT/'courses/databaze/lessons'/lid;w=root/lid
        shutil.copytree(d/'files',w);(w/'reseni.py').write_bytes((d/'solution.py').read_bytes());works.append(w)
    entry=works[0]/'spust_ucty.py';db=works[0]/'ucty.sqlite3'
    assert 'Účet ID: 1' in terminal(entry,['registrace','Žofie'],[('Cvičné heslo: ',PW),('Zopakujte heslo: ',PW)])
    menu='1 Výpis, 2 Přidat, 3 Odhlásit: '
    out=terminal(entry,['prihlaseni','ŽOFIE'],[('Cvičné heslo: ',PW),(menu,'2'),('Poznámka: ','Poznámka z terminálu; žluťoučká'),(menu,'1'),(menu,'3')])
    assert 'Poznámka z terminálu; žluťoučká' in out
    terminal(entry,['prihlaseni','Žofie'],[('Cvičné heslo: ',WRONG)],expected=2)
    packed=works[1]/'prenos.txt';entry=works[1]/'spust_ucty.py'
    for action in ['export','import']:
        out=terminal(entry,['--db',str(db),action,'Žofie',str(packed)],[('Cvičné heslo: ',PW)])
        assert 'Počet poznámek: 1' in out
    with closing(sqlite3.connect(db,autocommit=True)) as con:
        assert con.execute('SELECT COUNT(*) FROM poznamky').fetchone()==(2,)
        assert PW not in con.execute('SELECT overeni FROM uzivatele').fetchone()[0]
    assert packed.read_text(encoding='ascii').startswith('z1:')
    print('OK: pět skutečných PTY procesů, getpass bez echa, přihlášení/odhlášení, neúspěch a přenos 23→25 se stejnou DB')
    d=ROOT/'courses/databaze/lessons/24-volitelne-cteni-textu-offline';w=root/'rec';shutil.copytree(d/'files',w)
    (w/'reseni.py').write_bytes((d/'solution.py').read_bytes())
    for args in [[],['--mluv']]:
        r=subprocess.run([python,str(w/'precti.py'),'Krátká ukázka.',*args],capture_output=True,text=True,timeout=20)
        assert r.returncode in (0,2),(r.stdout,r.stderr)
        print('Řeč', 'skutečná volba' if args else 'náhled',r.returncode,r.stdout.strip())
