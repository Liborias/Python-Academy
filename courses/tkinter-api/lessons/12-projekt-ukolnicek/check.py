import json
from dilna_check import check

c=check()
work=c.student.parent
def fixture(name,data):
    path=work/name
    path.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
    return str(path)
model=[{'nazev':'Žofie  Nová','hotovo':True},{'nazev':'Číst','hotovo':False}]
valid=fixture('ukoly-valid.json',model)
empty=fixture('ukoly-empty.json',[])
duplicates=[{'nazev':'Stejné','hotovo':False},{'nazev':'Stejné','hotovo':True}]
extra=fixture('ukoly-extra.json',[dict(duplicates[0],navic=123),duplicates[1]])
invalid=[fixture('ukoly-bad-'+str(i)+'.json',data) for i,data in enumerate([
    {},[None],[{'nazev':'','hotovo':False}],[{'nazev':'   ','hotovo':False}],
    [{'nazev':4,'hotovo':False}],[{'nazev':'A','hotovo':1}],[{'nazev':'A'}],
    [{'nazev':'A','hotovo':False},{'nazev':'B','hotovo':None}]])]
bad_json=work/'ukoly-broken.json';bad_json.write_text('{',encoding='utf-8');invalid.append(str(bad_json))
bad_utf=work/'ukoly-encoding.json';bad_utf.write_bytes(b'\xff');invalid.append(str(bad_utf))
pure_save=work/'ukoly-pure-save.json'
calls=[{'name':'nacti_ukoly','args':[valid]},{'name':'nacti_ukoly','args':[empty]},{'name':'nacti_ukoly','args':[extra]}]
calls += [{'name':'nacti_ukoly','args':[path]} for path in invalid]
calls += [{'name':'uloz_ukoly','args':[str(pure_save),model]}]
pure=c.tk_run(calls=calls,run_name='student')
if c.tk_no_error(pure,'Souborový model lze importovat'):
    c.add('Import nevytváří okno',not pure.widgets() and pure.mainloops==0,'Souborové funkce nemají vytvářet Tk ani spouštět hlavní smyčku.')
    for index,value in enumerate([model,[],duplicates]):
        result=(pure.calls or [])[index] if len(pure.calls or [])>index else {}
        c.add('Načtení celého modelu '+str(index),not result.get('error') and result.get('value')==value,'Zachovejte pořadí, názvy a skutečné bool stavy; prázdný seznam je platný.')
    for index in range(3,3+len(invalid)):
        result=(pure.calls or [])[index] if len(pure.calls or [])>index else {}
        c.add('Neplatný model '+str(index),(result.get('error') or {}).get('type') in ('ValueError','JSONDecodeError','UnicodeDecodeError'), 'Ověřte všechny záznamy a jejich typy, neplatná pozdější položka odmítne celý soubor.')
    try:
        raw=pure_save.read_text('utf-8');ok=json.loads(raw)==model and 'Žofie' in raw
    except (OSError,ValueError):ok=False
    c.add('Čitelný a úplný uložený model',ok,'JSON v UTF-8 obsahuje název a bool stav každé položky, bez značek z Listbox.')

prompt='Vyberte úkol pro podrobnosti.'
state={'items':[],'message':'Úkolníček je připravený.','detail':prompt,'selection':[],'entry':''}
actions=[];expected=[dict(state)]
dialogs=[]
def step(action,**changes):
    actions.append(action);state.update(changes);expected.append(dict(state))
def fill(value):step({'action':'fill','value':value},entry=value)
def click(name,**changes):step({'action':'click','text':name},**changes)
def select(index,detail):step({'action':'select','index':index},selection=[] if index is None else [index],detail=detail)
def dialog(kind,path,**changes):
    dialogs.append({'kind':kind,'path':str(path)})
    click('Uložit JSON' if kind=='save' else 'Načíst JSON',**changes)

click('Dokončit',message='Nejprve vyberte úkol.')
click('Odstranit',message='Nejprve vyberte úkol.')
fill('   ');click('Přidat',message='Napište název úkolu.')
fill('  Ema  ');click('Přidat',items=['[ ] Ema'],entry='',selection=[],detail=prompt,message='Přidáno: Ema.')
fill('Druhý');click('Přidat',items=['[ ] Ema','[ ] Druhý'],entry='',message='Přidáno: Druhý.')
fill('Ema');click('Přidat',items=['[ ] Ema','[ ] Druhý','[ ] Ema'],entry='',message='Přidáno: Ema.')
select(2,'Úkol: Ema\nStav: čeká')
click('Dokončit',items=['[ ] Ema','[ ] Druhý','[hotovo] Ema'],detail='Úkol: Ema\nStav: hotovo',message='Dokončeno: Ema.')
click('Dokončit')
click('Odstranit',items=['[ ] Ema','[ ] Druhý'],selection=[],detail=prompt,message='Odstraněno: Ema.')
select(0,'Úkol: Ema\nStav: čeká')
click('Dokončit',items=['[hotovo] Ema','[ ] Druhý'],detail='Úkol: Ema\nStav: hotovo',message='Dokončeno: Ema.')
select(1,'Úkol: Druhý\nStav: čeká')
target=work/'ukoly-gui-save.json';new_target=work/'ukoly-new-save.json'
dialog('save',target,message='Úkoly uloženy.')
dialog('open','',message='Načítání zrušeno.')
for path in [invalid[7],str(work/'neexistuje.json'),str(bad_utf),str(bad_json)]:
    dialog('open',path,message='Soubor se nepodařilo načíst.')
dialog('save',work,message='Soubor se nepodařilo uložit.')
dialog('save','',message='Ukládání zrušeno.')
click('Odstranit',items=['[hotovo] Ema'],selection=[],detail=prompt,message='Odstraněno: Druhý.')
dialog('open',target,items=['[hotovo] Ema','[ ] Druhý'],selection=[],detail=prompt,message='Úkoly načteny.')
dialog('open',valid,items=['[hotovo] Žofie  Nová','[ ] Číst'])
select(0,'Úkol: Žofie  Nová\nStav: hotovo')
# Text s podrobnostmi musí zůstat pouze pro čtení.
step({'action':'fill_text','value':'Nesmí přepsat detail'})
dialog('open',empty,items=[],selection=[],detail=prompt)
fill(' Nový ');click('Přidat',items=['[ ] Nový'],entry='',message='Přidáno: Nový.')
dialog('save',new_target,message='Úkoly uloženy.')
dialog('open',empty,items=[],detail=prompt,message='Úkoly načteny.')
dialog('open',new_target,items=['[ ] Nový'])
r=c.tk_run(actions,dialogs=dialogs)
if c.tk_no_error(r):
    lists,texts,roots,entries=r.widgets('listbox'),r.widgets('text'),r.widgets('root'),r.widgets('entry')
    labels=[w for w in r.widgets('label') if w['text']=='Úkolníček je připravený.']
    c.add('Úkolníček připravený k ovládání',len(lists)==len(texts)==len(roots)==len(entries)==len(labels)==1 and roots[0]['visible'] and r.mainloops==1
          and len(r.dialogs or [])==len(dialogs),'Ponechte Listbox, detail, vstup, zprávu a souborové dialogy v jediném okně.')
    for index,state in enumerate(expected):
        l,t,e=r.widgets('listbox',index),r.widgets('text',index),r.widgets('entry',index)
        s=[w for w in r.widgets('label',index) if labels and w['id']==labels[0]['id']]
        c.add('Model, detail a soubor '+str(index),len(l)==len(t)==len(e)==len(s)==1 and l[0]['items']==state['items']
              and l[0]['selection']==state['selection'] and t[0]['value']==state['detail'] and t[0]['state']=='disabled'
              and e[0]['value']==state['entry'] and s[0]['text']==state['message'] and len(r.widgets(index=index))==len(r.widgets())
              and all(w['visible'] for w in r.widgets(index=index)),
              'Měňte správný index, dokončení nastavuje True, detail odpovídá výběru. Neplatné načtení i zrušení zachová celý současný stav.')
    for path,model in [(target,[{'nazev':'Ema','hotovo':True},{'nazev':'Druhý','hotovo':False}]),(new_target,[{'nazev':'Nový','hotovo':False}])]:
        try:ok=json.loads(path.read_text('utf-8'))==model
        except (OSError,ValueError):ok=False
        c.add('Uložení modelu '+path.name,ok,'Zapisujte skutečný model včetně pořadí a bool stavu, nikoli textové značky z Listbox.')
c.done()
