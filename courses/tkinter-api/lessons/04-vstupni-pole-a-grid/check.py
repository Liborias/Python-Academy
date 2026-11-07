from dilna_check import check

c = check()
actions = [{'action': 'click', 'text': 'Pozdravit'}, {'action': 'fill', 'value': '  Ema  '}, {'action': 'click', 'text': 'Pozdravit'},
           {'action': 'fill', 'value': '   '}, {'action': 'click', 'text': 'Pozdravit'},
           {'action': 'fill', 'value': '  Žofie  Nová  '}, {'action': 'click', 'text': 'Pozdravit'}]
r = c.tk_run(actions)
def position(widget, row, column, span=1):
    try:
        layout = widget['layout']
        return widget['manager'] == 'grid' and int(layout.get('row', 0)) == row and int(layout.get('column', 0)) == column and int(layout.get('columnspan', 1)) == span
    except (TypeError, ValueError):
        return False
if c.tk_no_error(r):
    roots, labels, entries, buttons = r.widgets('root'), r.widgets('label'), r.widgets('entry'), r.widgets('button')
    c.add('Okno, formulář a hlavní smyčka', len(roots) == 1 and roots[0]['visible'] and len(labels) == 2 and len(entries) == 1 and len(buttons) == 1 and r.mainloops == 1 and len(r.widgets()) == 5, 'Ponechte jedno okno, dva popisky, vstup a tlačítko.')
    captions = [w for w in labels if w['text'] == 'Vaše jméno:']
    results = [w for w in labels if w['text'] == 'Zadejte jméno a klikněte.']
    c.add('Rozložení mřížky', len(captions) == len(results) == len(entries) == len(buttons) == 1
          and position(captions[0], 0, 0) and position(entries[0], 0, 1) and position(buttons[0], 1, 0, 2) and position(results[0], 2, 0, 2),
          'Jméno a vstup patří do prvního řádku, tlačítko do druhého a výsledek do třetího, poslední dva přes oba sloupce.')
    c.add('Widgety patří do stejného okna', len(roots) == 1 and all(w['visible'] and w['parent'] == roots[0]['id'] for w in labels + entries + buttons), 'Předávejte hlavní okno jako rodiče a používejte grid.')
    try:
        weight = float(roots[0]['columns'].get('1', {}).get('weight', 0)) if len(roots) == 1 else 0
        sticky = entries[0]['layout'].get('sticky', '') if len(entries) == 1 else ''
        sticky = ''.join(sticky) if isinstance(sticky, (tuple, list)) else str(sticky)
        sticky = sticky.replace(' ', '')
        stretches = weight > 0 and set('ew') <= set(sticky) <= set('nsew')
    except (TypeError, ValueError):
        stretches = False
    c.add('Vstup se při změně šířky roztáhne', stretches, 'Nastavte kladnou váhu sloupce 1 a sticky ew u vstupu.')
    c.add('Funkce tlačítka', len(buttons) == 1 and buttons[0]['text'] == 'Pozdravit' and buttons[0]['has_command'], 'Použijte command=pozdrav bez závorek.')
    expected = ['Zadejte jméno a klikněte.', 'Zadejte jméno.', 'Zadejte jméno.', 'Ahoj, Ema!',
                'Ahoj, Ema!', 'Zadejte jméno.', 'Zadejte jméno.', 'Ahoj, Žofie  Nová!']
    for index, text in enumerate(expected):
        current = [w for w in r.widgets('label', index) if results and w['id'] == results[0]['id']]
        c.add('Aktuální vstup a reakce ' + str(index), len(current) == 1 and current[0]['text'] == text and len(r.widgets(index=index)) == 5,
              'Čtěte Entry.get při každém kliknutí, odstraňte jen krajní mezery a měňte existující výsledek. Prázdný text zobrazí Zadejte jméno.')
c.done()
