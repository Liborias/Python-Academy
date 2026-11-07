import math
from dilna_check import check

c = check()
valid = [(0, 'km-m', 0), (1.25, 'km-m', 1250), (0.0005, 'km-m', 0.5), (1250, 'm-km', 1.25), (3, 'm-km', 0.003)]
invalid = [(-1, 'km-m'), (-0.1, 'm-km'), (float('nan'), 'km-m'), (float('inf'), 'm-km'), (float('-inf'), 'km-m'), (1e308, 'km-m'), (1, 'jiny')]
calls = [{'name': 'preved_vzdalenost', 'args': [value, direction]} for value, direction, _ in valid]
calls += [{'name': 'preved_vzdalenost', 'args': list(args)} for args in invalid]
pure = c.tk_run(calls=calls, run_name='student')
if c.tk_no_error(pure, 'Výpočet lze importovat bez otevření okna'):
    c.add('Import a výpočet nevytvářejí widgety', not pure.widgets() and pure.mainloops == 0 and not pure.out.strip(), 'Vytváření okna dejte do hlavni a volejte ji jen v hlavním bloku. Výpočet pouze vrací číslo.')
    for index, (_, _, expected) in enumerate(valid):
        result = pure.calls[index] if pure.calls and index < len(pure.calls) else {}
        value = result.get('value')
        c.add('Samostatný výpočet ' + str(index), not result.get('error') and isinstance(value, (int, float)) and not isinstance(value, bool)
              and math.isfinite(value) and math.isclose(value, expected, rel_tol=1e-12, abs_tol=1e-12), 'Vraťte přesné převedené číslo bez textu a bez zaokrouhlení.')
    for index in range(len(valid), len(calls)):
        result = pure.calls[index] if pure.calls and index < len(pure.calls) else {}
        c.add('Neplatný výpočet ' + str(index), (result.get('error') or {}).get('type') == 'ValueError', 'Neplatné číslo, přetečení a neznámý směr odmítněte pomocí ValueError.')

actions = []
expected = ['Zadejte nezápornou vzdálenost.']
entry_values = ['']
current, text = expected[0], ''
for action, value in [('click', 'Převést'), ('fill', '  1,25  '), ('key', '1250.000 m'),
                      ('click', 'Metry na kilometry'), ('click-result', '0.001 km'),
                      ('fill', '1250'), ('key', '1.250 km'), ('fill', '-1'), ('key', 'Zadejte platné nezáporné číslo.'),
                      ('fill', 'abc'), ('click-result', 'Zadejte platné nezáporné číslo.'),
                      ('fill', 'nan'), ('key', 'Zadejte platné nezáporné číslo.'),
                      ('fill', 'inf'), ('click-result', 'Zadejte platné nezáporné číslo.'),
                      ('click', 'Kilometry na metry'), ('fill', '1e308'), ('key', 'Zadejte platné nezáporné číslo.'),
                      ('fill', '1.2,3'), ('key', 'Zadejte platné nezáporné číslo.'),
                      ('fill', '0'), ('click-result', '0.000 m'), ('fill', '0.0005'), ('key', '0.500 m')]:
    if action == 'fill':
        actions.append({'action': 'fill', 'value': value})
        text = value
    elif action == 'key':
        actions.append({'action': 'key'})
        current = value
    elif action == 'click-result':
        actions.append({'action': 'click', 'text': 'Převést'})
        current = value
    else:
        actions.append({'action': 'click', 'text': value})
        if value == 'Převést':
            current = 'Zadejte platné nezáporné číslo.'
    expected.append(current)
    entry_values.append(text)
r = c.tk_run(actions)
if c.tk_no_error(r):
    results = [w for w in r.widgets('label') if w['text'] == expected[0]]
    roots, entries, buttons, radios = r.widgets('root'), r.widgets('entry'), r.widgets('button'), r.widgets('radiobutton')
    c.add('Převodník připravený k ovládání', len(roots) == len(entries) == len(buttons) == len(results) == 1 and roots[0]['visible'] and r.mainloops == 1
          and entries[0]['focused'] and buttons[0]['text'] == 'Převést' and buttons[0]['has_command']
          and len(radios) == 2 and [w['text'] for w in radios if w['selected']] == ['Kilometry na metry'], 'Ponechte připravený vstup, volby, tlačítko a fokus.')
    for index, message in enumerate(expected):
        labels = [w for w in r.widgets('label', index) if results and w['id'] == results[0]['id']]
        current_entries = r.widgets('entry', index)
        c.add('Výsledek a oprava vstupu ' + str(index), len(labels) == 1 and labels[0]['text'] == message and labels[0]['visible']
              and len(current_entries) == 1 and current_entries[0]['value'] == entry_values[index]
              and len(r.widgets(index=index)) == len(r.widgets()) and all(w['visible'] for w in r.widgets(index=index)),
              'Čtěte aktuální text i směr, použijte výpočet a zachovejte vstup. Po chybě musí další tlačítko i Enter fungovat. Výsledek má tři desetinná místa a jednotku.')
c.done()
