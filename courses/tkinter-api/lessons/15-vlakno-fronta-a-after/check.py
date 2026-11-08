from urllib.parse import urlsplit
from dilna_check import check

c=check()
first={'mena':'EUR','czk_za_jednotku':27.5,'datum':'2026-02-20','zdroj':'Test API'}
second=dict(first,czk_za_jednotku=30,zdroj='Jiný test')
wait={'action':'wait','until':{'text':'Načíst kurz','state':'normal'},'timeout':2}
actions=[{'action':'click','text':'Načíst kurz'},{'action':'click','text':'Načíst kurz'},
         {'action':'click','text':'Chyba serveru'},{'action':'click','text':'Klikni během načítání'},wait,
         {'action':'click','text':'Chyba serveru'},{'action':'click','text':'Načíst kurz'},wait,
         {'action':'click','text':'Běžná odpověď'},{'action':'click','text':'Načíst kurz'},wait,
         {'action':'click','text':'Klikni během načítání'}]
r=c.tk_run(actions,http=[{'json':first,'delay_ms':350},{'status':503,'json':first,'delay_ms':80},{'json':second,'delay_ms':80}])
if c.tk_no_error(r):
    roots=r.widgets('root');labels=r.widgets('label')
    status=[w for w in labels if w['text']=='Připraveno k načtení.']
    rate=[w for w in labels if w['text']=='Kurz zatím není načtený.']
    counter=[w for w in labels if w['text']=='Kliknutí: 0']
    c.add('Okno a počáteční stav',len(roots)==len(status)==len(rate)==len(counter)==1 and roots[0]['visible'] and r.mainloops==1,'Ponechte jediné okno, zprávu, kurz a počítadlo.')
    expected=[('Připraveno k načtení.','Kurz zatím není načtený.',0,False)]
    loading=('Načítám kurz...','Kurz zatím není načtený.',0,True)
    expected += [loading,loading,loading,('Načítám kurz...','Kurz zatím není načtený.',1,True),
                 ('Kurz načten.','1 EUR = 27.50 CZK | 2026-02-20 | Test API',1,False),
                 ('Kurz načten.','1 EUR = 27.50 CZK | 2026-02-20 | Test API',1,False),
                 ('Načítám kurz...','Kurz zatím není načtený.',1,True),
                 ('Kurz se nepodařilo načíst. Zkuste to znovu.','Kurz zatím není načtený.',1,False),
                 ('Kurz se nepodařilo načíst. Zkuste to znovu.','Kurz zatím není načtený.',1,False),
                 ('Načítám kurz...','Kurz zatím není načtený.',1,True),
                 ('Kurz načten.','1 EUR = 30.00 CZK | 2026-02-20 | Jiný test',1,False),
                 ('Kurz načten.','1 EUR = 30.00 CZK | 2026-02-20 | Jiný test',2,False)]
    for index,(message,value,count,busy) in enumerate(expected):
        widgets=r.widgets(index=index);by_id={w['id']:w for w in widgets}
        load=[w for w in r.widgets('button',index) if w['text']=='Načíst kurz']
        radios=r.widgets('radiobutton',index)
        ok=len(status)==len(rate)==len(counter)==len(load)==1 and len(radios)==3
        ok=ok and by_id.get(status[0]['id'],{}).get('text')==message and by_id.get(rate[0]['id'],{}).get('text')==value and by_id.get(counter[0]['id'],{}).get('text')==f'Kliknutí: {count}'
        ok=ok and (load[0]['state']=='disabled')==busy and all((w['state']=='disabled')==busy for w in radios)
        ok=ok and len(widgets)==len(r.widgets()) and all(w['visible'] for w in widgets)
        c.add('Průběh načítání '+str(index),ok,'Počítadlo musí fungovat při čekání, druhý požadavek se nespustí. Po úspěchu i chybě znovu povolte ovládání.')
    c.add('Tři požadavky ve pracovníkovi',len(r.http or [])==3 and all(not h['main_thread'] for h in r.http)
          and [urlsplit(h['url']).path for h in r.http]==['/pomalu/kurz','/chyba/kurz','/kurz'],
          'Snímejte volbu v hlavním vlákně a spusťte právě jednoho pracovníka, další kliknutí při práci ignorujte.')
    c.add('Callbacky vracejí řízení',all(row['ms']<250 for row in r.callbacks or []),'Síťový požadavek ani join nepatří do hlavní smyčky.')
c.done()
