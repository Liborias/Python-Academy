import json
import math
from dilna_check import check

c=check()
valid=[(10,25,250),(0,2,0),(1.234,2,2.468),(1,.5,.5)]
invalid=[(-1,25),(1,0),(1,-1),(True,25),(1,False),('1',25),(float('nan'),25),(1,float('inf')),(1e308,1e3),(10**400,1)]
calls=[{'name':'preved_castku','args':[a,b]} for a,b,_ in valid]+[{'name':'preved_castku','args':list(args)} for args in invalid]
custom=c.student.parent/'jine-kurzy.json'
custom_data={'USD':{'mena':'USD','czk_za_jednotku':7.5,'datum':'2026-02-28','zdroj':'Jiný soubor'}}
custom.write_text(json.dumps(custom_data,ensure_ascii=False),encoding='utf-8')
calls += [{'name':'nacti_kurz_soubor','args':[str(custom),' usd ']}]
pure=c.tk_run(run_name='student',calls=calls)
if c.tk_no_error(pure,'Výpočet a soubor lze importovat'):
    c.add('Výpočet je oddělený od okna',not pure.widgets() and pure.mainloops==0,'Import a výpočet nevytvářejí Tk widgety.')
    for i,(_,_,expected) in enumerate(valid):
        row=(pure.calls or [])[i] if len(pure.calls or [])>i else {};value=row.get('value')
        c.add('Součin bez zaokrouhlení '+str(i),not row.get('error') and isinstance(value,(int,float)) and not isinstance(value,bool)
              and math.isfinite(value) and math.isclose(value,expected,rel_tol=1e-12,abs_tol=1e-12),'Částku násobte kurzem, vraťte číslo bez textu a zaokrouhlení.')
    for i in range(len(valid),len(valid)+len(invalid)):
        row=(pure.calls or [])[i] if len(pure.calls or [])>i else {}
        c.add('Neplatný výpočet '+str(i),(row.get('error') or {}).get('type')=='ValueError','Částka je konečná nezáporná, kurz konečný kladný; bool, text a přetečení odmítněte ValueError.')
    last=(pure.calls or [{}])[-1]
    c.add('Předaný soubor a měna',not last.get('error') and last.get('value')==custom_data['USD'],'Čtěte předanou cestu a ověřte záznam požadované měny.')

wait={'action':'wait','until':{'text':'Načíst kurz','state':'normal'},'timeout':2}
actions=[];expected=[]
state={'status':'Vyberte zdroj a načtěte kurz.','rate':'Kurz zatím není načtený.','result':'Výsledek: zatím nic.','entry':'','busy':False,'ready':False}
expected.append(dict(state))
def step(action,**changes):actions.append(action);state.update(changes);expected.append(dict(state))
def click(text,**changes):step({'action':'click','text':text},**changes)
def fill(value):step({'action':'fill','value':value},entry=value)
def start():click('Načíst kurz',busy=True,ready=False,status='Načítám kurz...',rate='Kurz zatím není načtený.',result='Výsledek: zatím nic.')
def finish(rate):step(wait,busy=False,ready=True,status='Kurz načten. Převod používá zobrazená cvičná data.',rate=rate)
def convert(value):click('Převést',result=f'Výsledek: {value} CZK',status='Převod dokončen. Jde o cvičný výpočet.')
def invalid_amount():click('Převést',result='Výsledek: zatím nic.',status='Zadejte platnou nezápornou částku.')
def change(text):click(text,ready=False,status='Volba změněna. Načtěte nový kurz.',rate='Kurz zatím není načtený.',result='Výsledek: zatím nic.')
click('Převést');fill('10');start()
click('Načíst kurz');click('USD');click('Převést');fill(' 1,5 ')
finish('1 EUR = 27.00 CZK | 2026-02-20 | Test API');convert('40.50')
fill('-1');invalid_amount();fill('0');convert('0.00');fill('nan');invalid_amount();fill('abc');invalid_amount();fill('10');convert('270.00')
start();step(wait,busy=False,ready=False,status='Kurz se nepodařilo načíst. Zvolte zdroj a zkuste to znovu.')
click('Převést');change('USD');start();finish('1 USD = 21.25 CZK | 2026-02-21 | Nový test');fill('2');convert('42.50')
change('Cvičný soubor');start();finish('1 USD = 19.00 CZK | 2026-01-14 | Cvičný soubor');convert('38.00')
change('EUR');start();finish('1 EUR = 24.00 CZK | 2026-01-14 | Cvičný soubor');convert('48.00')
plans=[{'json':{'mena':'EUR','czk_za_jednotku':27,'datum':'2026-02-20','zdroj':'Test API'},'delay_ms':350},
       {'json':{},'status':503,'delay_ms':80},
       {'json':{'mena':'USD','czk_za_jednotku':21.25,'datum':'2026-02-21','zdroj':'Nový test'},'delay_ms':80}]
r=c.tk_run(actions,http=plans)
if c.tk_no_error(r):
    labels=r.widgets('label')
    groups={key:[w for w in labels if w['text']==expected[0][key]] for key in ('status','rate','result')}
    c.add('Tři čitelné zprávy',all(len(g)==1 for g in groups.values()) and len(r.widgets('root'))==1 and r.mainloops==1,'Ponechte stav, kurz se zdrojem/datem a výsledek.')
    for i,state in enumerate(expected):
        widgets=r.widgets(index=i);by_id={w['id']:w for w in widgets};entries=r.widgets('entry',i)
        load=[w for w in r.widgets('button',i) if w['text']=='Načíst kurz'];convert_button=[w for w in r.widgets('button',i) if w['text']=='Převést']
        radios=r.widgets('radiobutton',i)
        ok=all(len(g)==1 and by_id.get(g[0]['id'],{}).get('text')==state[key] for key,g in groups.items())
        ok=ok and len(entries)==len(load)==len(convert_button)==1 and entries[0]['value']==state['entry']
        ok=ok and (load[0]['state']=='disabled')==state['busy'] and (convert_button[0]['state']!='disabled')==state['ready']
        ok=ok and len(radios)==4 and all((w['state']=='disabled')==state['busy'] for w in radios)
        ok=ok and len(widgets)==len(r.widgets()) and all(w['visible'] for w in widgets)
        c.add('Převod a stav '+str(i),ok,'Používejte aktuální částku i zobrazený kurz. Změna volby a neúspěšné načtení zneplatní starý kurz, vstup zůstane zachovaný.')
    c.add('API ve pracovníkovi, soubor bez požadavku',len(r.http or [])==3 and all(not h['main_thread'] for h in r.http),'Načítání běží na pozadí, zakázané tlačítko nezaloží další požadavek.')
    c.add('Krátké callbacky',all(row['ms']<250 for row in r.callbacks or []),'HTTP ani čekání na pracovníka nesmí blokovat hlavní smyčku.')

# Nesmí se zobrazit starý nebo vymyšlený kurz při chybě souboru.
path=c.student.parent/'kurzy.json';backup=path.read_bytes();path.unlink()
try:
    missing=c.tk_run([{'action':'click','text':'Cvičný soubor'},{'action':'click','text':'Načíst kurz'},wait])
    if c.tk_no_error(missing,'Chyba souboru se vrátí do okna'):
        labels=[w['text'] for w in missing.widgets('label',-1)]
        buttons=[w for w in missing.widgets('button',-1) if w['text']=='Převést']
        c.add('Chybějící soubor nepovolí převod','Kurz zatím není načtený.' in labels and 'Kurz se nepodařilo načíst. Zvolte zdroj a zkuste to znovu.' in labels and len(buttons)==1 and buttons[0]['state']=='disabled','Chyba souboru ponechá převod zakázaný a dovolí nové načítání.')
finally:path.write_bytes(backup)
c.done()
