import sys
from unittest.mock import patch
import smtplib
from dilna_check import check

c=check();sys.path.insert(0,str(c.student.parent));ns=c.load()
if ns and callable(ns.get('odesli_do_zachytu')):
    message=ns['vytvor_zpravu']('eva@example.test','jan@example.test','Česká zpráva','Tělo')
    sessions=[];plan={}
    class Client:
        def __init__(self,host='',port=0,**options):
            self.host,self.port,self.options=host,port,options;self.entered=False;self.closed=False;self.sent=[];sessions.append(self)
            if plan.get('connect_error'):raise ConnectionRefusedError('Cvičné odmítnutí spojení')
        def __enter__(self):self.entered=True;return self
        def __exit__(self,*args):self.closed=True
        def send_message(self,msg):self.sent.append(msg);return plan.get('refused',{})
    with patch.object(smtplib,'SMTP',Client):
        for i,(port,timeout) in enumerate([(23111,.25),(24123,2)]):
            before=len(sessions);ok,value=c.call(ns,'odesli_do_zachytu',(message,'127.0.0.1',port,timeout))
            created=sessions[before:]
            good=ok and value is None and len(created)==1
            good=good and created[0].host=='127.0.0.1' and created[0].port==port and created[0].options.get('timeout')==timeout
            good=good and created[0].entered and created[0].closed and len(created[0].sent)==1 and created[0].sent[0] is message
            c.add('Předání a úklid '+str(i),good,'Použijte předaný host, port, timeout, SMTP kontext a tentýž objekt v send_message.')
        plan['refused']={'jan@example.test':(550,b'Cvicne odmitnuti')}
        c.raises(ns,'odesli_do_zachytu',(message,'127.0.0.1',23111),smtplib.SMTPRecipientsRefused,'Odmítnuté adresy nejsou úspěch.')
        plan.clear();plan['connect_error']=True
        c.raises(ns,'odesli_do_zachytu',(message,'127.0.0.1',23111),OSError,'Chybu spojení předejte volajícímu.')
        plan.clear();before=len(sessions)
        for args in [('smtp.example.test',23111,2),('127.0.0.1',0,2),('127.0.0.1',65536,2),('127.0.0.1',True,2),('127.0.0.1',23111,0),('127.0.0.1',23111,float('inf')),('127.0.0.1',23111,6)]:
            ok,value=c.call(ns,'odesli_do_zachytu',(message,*args))
            c.add('Neplatné spojení '+str(args[1:]),not ok and isinstance(value,ValueError),'Ověřte loopback, rozsah portu a konečný kladný timeout do 5 sekund před připojením.')
        c.add('Neplatné nastavení neotevře SMTP',len(sessions)==before,'Před voláním SMTP použijte over_spojeni.')
else:c.add('Funkce odesli_do_zachytu',False,'Definujte odesli_do_zachytu(zprava, host, port, timeout=2).')
c.done()
