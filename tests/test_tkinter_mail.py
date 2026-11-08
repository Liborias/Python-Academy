"""E-maily 17–20: Unicode, SMTP obálka, přílohy, konfigurace a nejisté potvrzení."""
import json
import runpy
import sys
import tempfile
import unittest
from email.parser import BytesParser
from email.policy import default
from pathlib import Path
import smtplib

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from server.checker import run_check
from tools.setup_env import wanted

BASE=ROOT/'courses/tkinter-api/lessons'
IDS=['17-emailmessage-a-nahled','18-smtp-a-mistni-zachyt','19-prilohy-a-vyber-souboru','20-nastaveni-smtp-a-chyby']


class TkinterMailTest(unittest.TestCase):
    def source(self,index):return (BASE/IDS[index]/'solution.py').read_text('utf-8')
    def variants(self,index,wrong,correct):
        for expected,variants in [(False,wrong),(True,correct)]:
            for code in variants:
                self.assertNotEqual(code,self.source(index))
                with self.subTest(expected=expected,code=code),tempfile.TemporaryDirectory() as temp:
                    result=run_check(BASE/IDS[index],code,ROOT/'lib',Path(temp))
                    self.assertNotIn('error',result,result)
                    self.assertEqual(result.get('ok'),expected,result)

    def test_message_headers_body_and_unicode_roundtrip(self):
        s=self.source(0)
        wrong=[s.replace('zprava["To"] = prijemce','zprava["To"] = odesilatel'),s.replace('zprava["Subject"] = predmet.strip()','zprava["Subject"] = predmet'),
               s.replace('charset="utf-8"','charset="ascii"'),s.replace('return zprava','return zprava.as_string()'),
               s.replace('text.replace("\\r\\n", "\\n").replace("\\r", "\\n")','"Pevný text"'),
               s.replace('odesilatel = over_adresu(odesilatel)','odesilatel = "a@example.test"'),
               s.replace('or "\\r" in predmet or "\\n" in predmet','or False').replace('zprava["Subject"] = predmet.strip()','zprava["Subject"] = predmet.replace("\\n", " ").strip()')]
        correct=[s.replace('zprava["Subject"] = predmet.strip()','zprava["Subject"] = predmet.lstrip().rstrip()'),
                 s.replace('policy=SMTP','policy=SMTP.clone(utf8=False)'),s.replace('zprava["To"] = prijemce','zprava["to"] = prijemce')]
        self.variants(0,wrong,correct)

    def test_smtp_parameters_context_errors_and_local_only(self):
        s=self.source(1)
        wrong=[s.replace('host, port, timeout = over_spojeni(host, port, timeout)','pass'),
               s.replace('SMTP(host, port,','SMTP(host, 2525,'),s.replace('timeout=timeout','timeout=2'),
               s.replace('klient.send_message(zprava)','{}'),s.replace('klient.send_message(zprava)','klient.send_message(zprava.as_string())'),
               s.replace('if odmitnuti:','if False:'),
               s.replace('with smtplib.SMTP(host, port, timeout=timeout, local_hostname="localhost") as klient:','klient = smtplib.SMTP(host, port, timeout=timeout, local_hostname="localhost")\n    if True:')]
        correct=[s.replace('SMTP(host, port,','SMTP(host=host, port=port,'),s.replace('if odmitnuti:','if len(odmitnuti) != 0:'),
                 s.replace('klient.send_message(zprava)','klient.send_message(msg=zprava)')]
        self.variants(1,wrong,correct)

    def test_attachment_exact_bytes_size_and_unchanged_failure(self):
        s=self.source(2)
        wrong=[s.replace('cesta.open("rb")','cesta.open("r", encoding="utf-8")'),s.replace('read(MAX_PRILOHA + 1)','read(MAX_PRILOHA)'),
               s.replace('filename=cesta.name','filename=str(cesta)'),s.replace('if len(data) > MAX_PRILOHA:','if False:'),
               s.replace('data, maintype=','b"pevny obsah", maintype='),s.replace('if typ is None or kodovani is not None:','if typ is None:'),
               s.replace('    cesta = Path(cesta)','    zprava.clear()\n    cesta = Path(cesta)'),s.replace('    return zprava','    return None')]
        correct=[s.replace('filename=cesta.name','filename=Path(cesta).name'),s.replace('typ.split("/", 1)','typ.split("/")'),
                 s.replace('if len(data) > MAX_PRILOHA:','if len(data) >= MAX_PRILOHA + 1:')]
        self.variants(2,wrong,correct)

    def test_settings_types_and_gui_accept_reject_uncertain(self):
        s=self.source(3)
        wrong=[s.replace('prostredi.get("DILNA_SMTP_PORT", str(vychozi_port))','str(vychozi_port)'),
               s.replace('prostredi.get("DILNA_SMTP_TIMEOUT", "2")','"2"'),
               s.replace('host.strip(), int(port_text.strip()), float(timeout_text.strip())','"127.0.0.1", int(port_text.strip()), float(timeout_text.strip())'),
               s.replace('"odmitnuto": "Příjemce byl odmítnut. Zpráva nebyla převzata."','"odmitnuto": "Zprávu převzal místní záchyt."'),
               s.replace('"nejiste": "Přenos není potvrzený. Před novým pokusem zkontrolujte záchyt."','"nejiste": "Zpráva určitě nebyla převzata."'),
               s.replace('odeslat.configure(state="disabled")','odeslat.configure(state="normal")'),
               s.replace('threading.Thread(target=pracovnik, args=(zprava, nastaveni), daemon=True).start()','pracovnik(zprava, nastaveni)')]
        correct=[s.replace('nastaveni_text','konfigurace_text'),s.replace('int(port_text.strip())','int(port_text)'),
                 s.replace('queue.Queue()','queue.SimpleQueue()')]
        self.variants(3,wrong,correct)

    def test_metadata_dependencies_and_helper_copies(self):
        course=json.loads((BASE.parent/'course.json').read_text('utf-8'))
        self.assertEqual(course['modules'][4]['lessons'],IDS)
        self.assertIn('aiosmtpd>=1.4.6,<2',course['requires_packages'])
        self.assertIn('aiosmtpd>=1.4.6,<2',wanted('tkinter-api'))
        for i,lid in enumerate(IDS):
            d=BASE/lid
            self.assertEqual(json.loads((d/'lesson.json').read_text('utf-8'))['kind'],'console' if i<2 else 'gui')
            self.assertEqual(len(json.loads((d/'quiz.json').read_text('utf-8'))),3)
            if i:self.assertEqual((d/'files/zpravy.py').read_bytes(),(BASE/IDS[0]/'solution.py').read_bytes())
        for i in (1,3):self.assertEqual((BASE/IDS[i]/'files/cvicna_posta.py').read_bytes(),(BASE.parent/'shared/cvicna_posta.py').read_bytes())
        self.assertEqual((BASE/IDS[3]/'files/odesilani.py').read_bytes(),(BASE/IDS[1]/'solution.py').read_bytes())

    def test_actual_smtp_unicode_attachment_rejection_and_lost_confirmation(self):
        names=['zpravy','cvicna_posta'];previous={name:sys.modules.pop(name,None) for name in names}
        sys.path.insert(0,str(BASE/IDS[1]/'files'))
        try:
            ns=runpy.run_path(str(BASE/IDS[1]/'solution.py'),run_name='smtp_test')
            attachments=runpy.run_path(str(BASE/IDS[2]/'solution.py'),run_name='attachment_test')
            msg=ns['vytvor_zpravu']('eva@example.test','jan@example.test','Český předmět','Dobrý den.\n.Řádek s tečkou.')
            with tempfile.TemporaryDirectory() as temp:
                path=Path(temp)/'česká příloha.txt';data='Žofie\n'.encode('utf-8');path.write_bytes(data)
                attachments['pridej_prilohu'](msg,path)
                with ns['cvicna_posta']() as server:
                    ns['odesli_do_zachytu'](msg,server.host,server.port)
                    self.assertEqual(len(server.zpravy),1)
                    record=server.zpravy[0];parsed=BytesParser(policy=default).parsebytes(record.data)
                    self.assertEqual((record.odesilatel,record.prijemci),('eva@example.test',('jan@example.test',)))
                    self.assertEqual(str(parsed['Subject']),'Český předmět')
                    self.assertEqual(parsed.get_body(preferencelist=('plain',)).get_content().replace('\r\n','\n'),'Dobrý den.\n.Řádek s tečkou.\n')
                    part=list(parsed.iter_attachments())[0]
                    self.assertEqual((part.get_filename(),part.get_payload(decode=True)),(path.name,data))
                    server.nastav_rezim('odmitnout')
                    with self.assertRaises(smtplib.SMTPRecipientsRefused):ns['odesli_do_zachytu'](msg,server.host,server.port)
                    self.assertEqual(len(server.zpravy),1)
                    server.nastav_rezim('prijmout');ns['odesli_do_zachytu'](msg,server.host,server.port)
                    self.assertEqual(len(server.zpravy),2)
                    server.nastav_rezim('pomalu')
                    with self.assertRaises((smtplib.SMTPServerDisconnected,TimeoutError)):ns['odesli_do_zachytu'](msg,server.host,server.port,.05)
                    self.assertEqual(len(server.zpravy),3,'Zpráva už byla převzatá před opožděným potvrzením.')
        finally:
            sys.path.pop(0)
            for name,value in previous.items():
                sys.modules.pop(name,None)
                if value is not None:sys.modules[name]=value


if __name__=='__main__':unittest.main()
