from dilna_check import check

c = check()
names = ['Zobrazit volby', 'Křehký obsah', 'Zobrazit volby', 'Kurýr', 'Zobrazit volby',
         'Kurýr', 'Zobrazit volby', 'Křehký obsah', 'Zobrazit volby', 'Osobní odběr', 'Zobrazit volby']
r = c.tk_run([{'action': 'click', 'text': text} for text in names])
if c.tk_no_error(r):
    roots, checks, radios, buttons = r.widgets('root'), r.widgets('checkbutton'), r.widgets('radiobutton'), r.widgets('button')
    results = [w for w in r.widgets('label') if w['text'] == 'Zvolte možnosti a potvrďte.']
    c.add('Ovládací prvky a propojené proměnné', len(roots) == 1 and roots[0]['visible'] and r.mainloops == 1
          and len(checks) == len(buttons) == len(results) == 1 and len(radios) == 2 and len(r.widgets()) == 6
          and checks[0]['text'] == 'Křehký obsah' and checks[0]['variable_kind'] == 'int'
          and {w['text'] for w in radios} == {'Osobní odběr', 'Kurýr'} and all(w['variable_kind'] == 'string' for w in radios)
          and buttons[0]['text'] == 'Zobrazit volby' and buttons[0]['has_command'],
          'Potřebujete IntVar pro zaškrtávátko, společnou StringVar pro dva přepínače, výsledek a potvrzovací tlačítko.')
    expected = ['Zvolte možnosti a potvrďte.', 'Doprava: odběr; křehké: ne.', 'Doprava: odběr; křehké: ne.',
                'Doprava: odběr; křehké: ano.', 'Doprava: odběr; křehké: ano.', 'Doprava: kurýr; křehké: ano.',
                'Doprava: kurýr; křehké: ano.', 'Doprava: kurýr; křehké: ano.', 'Doprava: kurýr; křehké: ano.',
                'Doprava: kurýr; křehké: ne.', 'Doprava: kurýr; křehké: ne.', 'Doprava: odběr; křehké: ne.']
    for index, text in enumerate(expected):
        current = [w for w in r.widgets('label', index) if results and w['id'] == results[0]['id']]
        controls = r.widgets('radiobutton', index)
        chosen = 'Osobní odběr' if index < 4 or index >= 10 else 'Kurýr'
        fragile = index >= 2 and index < 8
        c.add('Aktuální volby a potvrzení ' + str(index), len(current) == 1 and current[0]['text'] == text
              and len(r.widgets(index=index)) == 6 and all(w['visible'] for w in r.widgets(index=index))
              and len(controls) == 2 and [w['text'] for w in controls if w['selected']] == [chosen]
              and len(r.widgets('checkbutton', index)) == 1 and r.widgets('checkbutton', index)[0]['selected'] == fragile,
              'Přepínače sdílejí jednu hodnotu, zaškrtávátko lze zapnout i vypnout. Zpráva se změní až při potvrzení.')
c.done()
