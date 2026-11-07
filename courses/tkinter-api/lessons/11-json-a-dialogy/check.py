import json
from pathlib import Path
from dilna_check import check

c=check()
work=c.student.parent
def fixture(name, data):
    path=work/name
    path.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
    return str(path)
valid=fixture('poznamka-valid.json',{'text':'Žofie\nDruhý řádek.','navic':True})
empty=fixture('poznamka-empty.json',{'text':''})
invalid=[fixture('poznamka-bad-'+str(i)+'.json',data) for i,data in enumerate([[],{}, {'text':None},{'text':4}])]
bad_json=work/'poznamka-broken.json';bad_json.write_text('{',encoding='utf-8');invalid.append(str(bad_json))
bad_utf=work/'poznamka-encoding.json';bad_utf.write_bytes(b'\xff');invalid.append(str(bad_utf))
saved=work/'poznamka-pure-save.json'
calls=[{'name':'nacti_poznamku','args':[valid]},{'name':'nacti_poznamku','args':[empty]}]
calls += [{'name':'nacti_poznamku','args':[path]} for path in invalid]
calls += [{'name':'uloz_poznamku','args':[str(saved),'Česká poznámka\nS koncem.\n']}]
pure=c.tk_run(calls=calls,run_name='student')
if c.tk_no_error(pure,'Souborové funkce lze importovat'):
    c.add('Bez otevření okna při importu',not pure.widgets() and pure.mainloops==0,'Souborové funkce oddělte od hlavni a hlavního bloku.')
    for index,text in enumerate(['Žofie\nDruhý řádek.','']):
        result=(pure.calls or [])[index] if len(pure.calls or [])>index else {}
        c.add('Načtení textu '+str(index),not result.get('error') and result.get('value')==text,'Vraťte pouze text; prázdná poznámka i klíče navíc jsou platné.')
    for index in range(2,2+len(invalid)):
        result=(pure.calls or [])[index] if len(pure.calls or [])>index else {}
        c.add('Odmítnutí neplatných dat '+str(index),(result.get('error') or {}).get('type') in ('ValueError','JSONDecodeError','UnicodeDecodeError'), 'Ověřte slovník a textový klíč, chybný JSON ani kódování nesmějí projít.')
    try:
        raw=saved.read_text('utf-8');ok=json.loads(raw)=={'text':'Česká poznámka\nS koncem.\n'} and 'Česká' in raw
    except (OSError,ValueError): ok=False
    c.add('Čitelný JSON v UTF-8',ok,'Zapište přesný text do objektu text, s UTF-8 a ensure_ascii=False.')

original='Rozpracovaná Žofie\nDruhý řádek.\n'
target=work/'poznamka-gui-save.json';empty_target=work/'poznamka-gui-empty.json'
actions=[{'action':'fill_text','value':original}]
dialogs=[];expect=[('Moje první poznámka.\nDruhý řádek.','Poznámka zatím není uložená.'),(original,'Poznámka zatím není uložená.')]
def click(kind,path,content,message):
    actions.append({'action':'click','text':'Uložit JSON' if kind=='save' else 'Načíst JSON'})
    dialogs.append({'kind':kind,'path':str(path)})
    expect.append((content,message))
click('save','',original,'Ukládání zrušeno.')
click('open','',original,'Načítání zrušeno.')
for path in [str(bad_json),invalid[0],str(work/'neexistuje.json'),str(bad_utf)]:
    click('open',path,original,'Soubor se nepodařilo načíst.')
click('save',work,original,'Soubor se nepodařilo uložit.')
click('save',target,original,'Poznámka uložena.')
actions.append({'action':'fill_text','value':'Změněná poznámka'});expect.append(('Změněná poznámka','Poznámka uložena.'))
click('open',target,original,'Poznámka načtena.')
click('open',empty,'','Poznámka načtena.')
click('save',empty_target,'','Poznámka uložena.')
r=c.tk_run(actions,dialogs=dialogs)
if c.tk_no_error(r):
    texts,roots=r.widgets('text'),r.widgets('root')
    labels=[w for w in r.widgets('label') if w['text']==expect[0][1]]
    c.add('Poznámka a dialogy',len(texts)==len(roots)==len(labels)==1 and roots[0]['visible'] and r.mainloops==1 and len(r.dialogs or [])==len(dialogs),'Ponechte jedno okno, Text, stavový popisek a oba souborové dialogy.')
    for index,(content,message) in enumerate(expect):
        t=r.widgets('text',index);s=[w for w in r.widgets('label',index) if labels and w['id']==labels[0]['id']]
        c.add('Soubor a zachování poznámky '+str(index),len(t)==len(s)==1 and t[0]['value']==content and s[0]['text']==message
              and len(r.widgets(index=index))==len(r.widgets()) and all(w['visible'] for w in r.widgets(index=index)),
              'Zrušení i chyba zachová text. Nahraďte jej až po úspěšném ověření nového obsahu.')
    for path,text in [(target,original),(empty_target,'')]:
        try: ok=json.loads(path.read_text('utf-8'))=={'text':text}
        except (OSError,ValueError): ok=False
        c.add('Uložení aktuálního obsahu '+path.name,ok,'Ukládejte aktuální Text bez automatického koncového nového řádku.')
c.done()
