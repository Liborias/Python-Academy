from dilna_check import check

c = check()
actions = [{'action': 'key'}, {'action': 'fill', 'value': '  Ema  '}, {'action': 'key'},
           {'action': 'fill', 'value': '  Žofie  Nová  '}, {'action': 'click', 'text': 'Pozdravit'},
           {'action': 'fill', 'value': '   '}, {'action': 'key'},
           {'action': 'fill', 'value': 'Ada'}, {'action': 'key'}, {'action': 'key'}, {'action': 'click', 'text': 'Pozdravit'}]
r = c.tk_run(actions)
if c.tk_no_error(r):
    roots, entries, buttons = r.widgets('root'), r.widgets('entry'), r.widgets('button')
    labels = [w for w in r.widgets('label') if w['text'] == 'Zadejte jméno.']
    c.add('Formulář a jediná smyčka', len(roots) == 1 and roots[0]['visible'] and len(entries) == len(buttons) == len(labels) == 1
          and buttons[0]['text'] == 'Pozdravit' and buttons[0]['has_command'] and len(r.widgets()) == 5 and r.mainloops == 1,
          'Ponechte jedno okno, vstup, dva popisky a tlačítko Pozdravit.')
    c.add('Fokus dostane vstup', len(entries) == 1 and entries[0]['focused'] and entries[0]['visible'], 'Po vytvoření Entry použijte focus_set().')
    expected = ['Zadejte jméno.', 'Zadejte jméno.', 'Zadejte jméno.', 'Ahoj, Ema!', 'Ahoj, Ema!', 'Ahoj, Žofie  Nová!',
                'Ahoj, Žofie  Nová!', 'Zadejte jméno.', 'Zadejte jméno.', 'Ahoj, Ada!', 'Ahoj, Ada!', 'Ahoj, Ada!']
    for index, text in enumerate(expected):
        results = [w for w in r.widgets('label', index) if labels and w['id'] == labels[0]['id']]
        c.add('Tlačítko i Enter, krok ' + str(index), len(results) == 1 and results[0]['text'] == text and len(r.widgets(index=index)) == 5,
              'Při Enteru i kliknutí čtěte aktuální jméno, odstraňte krajní mezery a změňte tentýž popisek. Bind předává událost.')
c.done()
