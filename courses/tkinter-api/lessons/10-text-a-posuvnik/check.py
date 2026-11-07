from dilna_check import check

c = check()
initial='\n'.join(f'Řádek {i}: poznámka k výuce.' for i in range(1,31))
actions=[{'action':'scroll','fraction':0.5}, {'action':'scroll','kind':'text','fraction':0}, {'action':'click','text':'Spočítat'},
         {'action':'fill_text','value':'A\nB\n'}, {'action':'click','text':'Spočítat'},
         {'action':'fill_text','value':''}, {'action':'click','text':'Spočítat'},
         {'action':'fill_text','value':'Žofie  Nová'}, {'action':'click','text':'Spočítat'}]
r=c.tk_run(actions)
if c.tk_no_error(r):
    texts, bars, roots = r.widgets('text'),r.widgets('scrollbar'),r.widgets('root')
    labels=[w for w in r.widgets('label') if w['text']=='Text můžete upravit.']
    c.add('Text a svislý posuvník', len(texts)==len(bars)==len(roots)==len(labels)==1 and roots[0]['visible'] and r.mainloops==1
          and bars[0]['orient']=='vertical' and texts[0]['value']==initial, 'Ponechte třicet úvodních řádků, Text, svislý Scrollbar a stavovou zprávu.')
    moved, returned = r.widgets('text',1),r.widgets('text',2)
    c.add('Posuvník skutečně ovládá výřez', len(moved)==len(returned)==1 and moved[0]['yview'][0]>0 and returned[0]['yview'][0]==0,
          'Předejte text.yview do command posuvníku bez závorek.')
    for index in (0,1,2):
        t,b=r.widgets('text',index),r.widgets('scrollbar',index)
        c.add('Zpětné hlášení výřezu '+str(index),len(t)==len(b)==1 and b[0]['range']==t[0]['yview'], 'Připojte text.configure(yscrollcommand=posuvnik.set).')
    content, message = initial, 'Text můžete upravit.'
    expected=[(content,message)]
    for action in actions:
        if action['action']=='fill_text': content=action['value']
        elif action['action']=='click': message=f'Znaků: {len(content)}; řádků: {content.count(chr(10))+1 if content else 0}.'
        expected.append((content,message))
    for index,(content,message) in enumerate(expected):
        t=r.widgets('text',index)
        status=[w for w in r.widgets('label',index) if labels and w['id']==labels[0]['id']]
        c.add('Aktuální obsah a počty '+str(index),len(t)==len(status)==1 and t[0]['value']==content and status[0]['text']==message
              and len(r.widgets(index=index))==len(r.widgets()) and all(w['visible'] for w in r.widgets(index=index)),
              'Čtěte 1.0 až end-1c, započítejte vlastní nové řádky, prázdný text má 0 řádků. Obsah neměňte.')
c.done()
