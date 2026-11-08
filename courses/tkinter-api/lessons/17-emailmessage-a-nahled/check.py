from email.message import EmailMessage
from email.parser import BytesParser
from email.policy import default
from email.utils import parsedate_to_datetime
from dilna_check import check

c=check();ns=c.load()
def normal(text):return text.replace('\r\n','\n').replace('\r','\n')
if ns and callable(ns.get('vytvor_zpravu')):
    for i,(sender,to,subject,body) in enumerate([
        (' eva+kurz@example.test ','jan@example.test','  Žofie: přílohy  ','Dobrý den,\r\n\r\n.Řádek.\rKonec'),
        ('a@example.test','b@example.test','Prázdné tělo',''),
        ('a@example.test','b@example.test','Druhý pokus','Dvě  mezery\n\n')]):
        ok,msg=c.call(ns,'vytvor_zpravu',(sender,to,subject,body))
        valid=ok and isinstance(msg,EmailMessage)
        c.add('Objekt zprávy '+str(i),valid,'Vraťte EmailMessage, nikoli text či None.')
        if not valid:continue
        expected=normal(body)
        if not expected.endswith('\n'):expected+='\n'
        parsed=BytesParser(policy=default).parsebytes(msg.as_bytes())
        c.add('Hlavičky a české tělo '+str(i),str(parsed['From'])==sender.strip() and str(parsed['To'])==to.strip()
              and str(parsed['Subject'])==subject.strip() and parsed.get_content_type()=='text/plain'
              and parsed.get_content_charset()=='utf-8' and normal(parsed.get_content())==expected
              and all(len(parsed.get_all(name,[]))==1 for name in ['From','To','Subject']),
              'Použijte ověřené adresy, oříznutý předmět a text v UTF-8. Zachovejte vnitřní mezery i nové řádky.')
        try:metadata=parsedate_to_datetime(str(msg['Date'])).tzinfo is not None and str(msg['Message-ID']).startswith('<') and str(msg['Message-ID']).endswith('@example.test>')
        except (TypeError,ValueError):metadata=False
        c.add('Datum a identifikátor '+str(i),metadata,'Ponechte připravené Date a Message-ID.')
    bad=[('a','b@example.test','A','B'),('a@example.test','b@example.test,c@example.test','A','B'),
         ('a@example.test','žofie@example.test','A','B'),('a@example.test','b@example.test','  ','B'),
         ('a@example.test','b@example.test','A\nBcc: c@example.test','B'),
         ('a@example.test\r\nX: y','b@example.test','A','B'),('a@example.test','b@example.test','A',None)]
    for i,args in enumerate(bad):
        ok,value=c.call(ns,'vytvor_zpravu',args)
        c.add('Odmítnutí neplatného vstupu '+str(i),not ok and isinstance(value,ValueError),'Hlavičky jsou jednořádkové, adresy ASCII a tělo text.')
else:c.add('Funkce vytvor_zpravu',False,'Definujte vytvor_zpravu(odesilatel, prijemce, predmet, text).')
c.done()
