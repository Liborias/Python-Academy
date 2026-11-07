from dilna_check import check

c = check()
actions = [{'action':'click','text':'Odebrat'}, {'action':'select','index':2}, {'action':'click','text':'Odebrat'},
           {'action':'fill','value':'   '}, {'action':'click','text':'Přidat'}, {'action':'fill','value':'  Žofie  Nová  '},
           {'action':'click','text':'Přidat'}, {'action':'select','index':0}, {'action':'click','text':'Odebrat'},
           {'action':'select','index':0}, {'action':'click','text':'Odebrat'}, {'action':'select','index':0},
           {'action':'click','text':'Odebrat'}, {'action':'click','text':'Odebrat'}, {'action':'fill','value':'Znovu'}, {'action':'click','text':'Přidat'}]
r = c.tk_run(actions)
if c.tk_no_error(r):
    lists, entries, roots = r.widgets('listbox'), r.widgets('entry'), r.widgets('root')
    labels = [w for w in r.widgets('label') if w['text'] == 'Přidejte nebo odeberte úkol.']
    c.add('Seznam, vstup a zpráva', len(lists) == len(entries) == len(roots) == len(labels) == 1 and roots[0]['visible'] and r.mainloops == 1,
          'Ponechte Listbox, Entry, stavový popisek a jedno okno.')
    items = ['Přečíst zadání','Vyzkoušet ukázku','Přečíst zadání']
    message, value = 'Přidejte nebo odeberte úkol.', ''
    expected = [(list(items),message,value)]
    selected = None
    for action in actions:
        if action['action'] == 'fill': value = action['value']
        elif action['action'] == 'select': selected = action['index']
        elif action['text'] == 'Přidat':
            if value.strip():
                name=value.strip();items.append(name);value='';selected=None;message=f'Přidáno: {name}.'
            else: message='Napište název úkolu.'
        elif selected is None: message='Nejprve vyberte úkol.'
        else:
            message=f'Odebráno: {items.pop(selected)}.';selected=None
        expected.append((list(items),message,value))
    for index,(items,message,value) in enumerate(expected):
        current, field = r.widgets('listbox',index), r.widgets('entry',index)
        status = [w for w in r.widgets('label',index) if labels and w['id'] == labels[0]['id']]
        c.add('Výběr a změna modelu '+str(index), len(current) == len(field) == len(status) == 1 and current[0]['items'] == items
              and field[0]['value'] == value and status[0]['text'] == message and len(r.widgets(index=index)) == len(r.widgets())
              and all(w['visible'] for w in r.widgets(index=index)),
              'Odebírejte vybraný index z modelu, po změně obnovte zobrazení a ošetřete prázdný vstup i chybějící výběr.')
c.done()
