from dilna_check import check

c = check()
actions = [{'action': 'click', 'text': text} for text in ['Potvrdit', 'Potvrdit', 'Obnovit', 'Obnovit', 'Potvrdit']]
r = c.tk_run(actions)
if c.tk_no_error(r):
    roots, labels, buttons = r.widgets('root'), r.widgets('label'), r.widgets('button')
    c.add('Okno a hlavní smyčka', len(roots) == 1 and roots[0]['visible'] and r.mainloops == 1, 'Ponechte jedno viditelné okno a mainloop.')
    c.add('Obě tlačítka mají funkci', len(buttons) == 2 and {w['text'] for w in buttons} == {'Potvrdit', 'Obnovit'} and all(w['visible'] and w['has_command'] for w in buttons), 'Předejte command funkci bez závorek, ne její výsledek.')
    expected = ['Čekám na potvrzení.', 'Akce potvrzena.', 'Akce potvrzena.', 'Čekám na potvrzení.', 'Čekám na potvrzení.', 'Akce potvrzena.']
    for index, text in enumerate(expected):
        current = r.widgets('label', index)
        c.add('Stav před akcí a po kliknutí ' + str(index), len(labels) == 1 and len(current) == 1 and current[0]['id'] == labels[0]['id'] and current[0]['visible'] and current[0]['text'] == text and len(r.widgets(index=index)) == 4,
              'Upravujte text stejného popisku. Před prvním kliknutím má zůstat původní zpráva, Obnovit ji vrátí.')
c.done()
