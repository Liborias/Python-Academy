from dilna_check import check

c = check()
r = c.tk_run()
def position(w, column):
    try:
        return w['manager'] == 'grid' and int(w['layout'].get('row', 0)) == 0 and int(w['layout'].get('column', 0)) == column
    except (ValueError, TypeError):
        return False
if c.tk_no_error(r):
    roots, frames, labels, entries = r.widgets('root'), r.widgets('frame'), r.widgets('label'), r.widgets('entry')
    c.add('Jedno okno a dvě části formuláře', len(roots) == 1 and roots[0]['visible'] and roots[0]['title'] == 'Příprava výpravy'
          and len(frames) == 2 and len(labels) == 2 and len(entries) == 1 and len(r.widgets()) == 6 and r.mainloops == 1,
          'Vytvořte jedno okno, dva rámečky, dva popisky a jeden vstup.')
    names = [w for w in labels if w['text'] == 'Název výpravy:']
    messages = [w for w in labels if w['text'] == 'Formulář je připravený.']
    form = [f for f in frames if names and f['id'] == names[0]['parent']]
    info = [f for f in frames if messages and f['id'] == messages[0]['parent']]
    c.add('Každá část má svého rodiče', len(form) == len(info) == len(entries) == 1 and form[0]['id'] != info[0]['id']
          and entries[0]['parent'] == form[0]['id'] and len(roots) == 1
          and all(f['parent'] == roots[0]['id'] and f['manager'] == 'pack' for f in frames),
          'Horní rámeček obsahuje název a vstup, jiný dolní rámeček obsahuje zprávu. Oba patří přímo do okna.')
    c.add('Pořadí a rozložení uvnitř částí', len(form) == len(info) == len(names) == len(messages) == len(entries) == 1
          and form[0]['order'] < info[0]['order'] and position(names[0], 0) and position(entries[0], 1) and messages[0]['manager'] == 'pack'
          and all(w['visible'] for w in frames + labels + entries),
          'V okně použijte pack, nahoře grid na řádku 0 a dole pack. Horní rámeček umístěte první.')
    try:
        stretch = len(form) == len(entries) == 1 and all(f['layout'].get('fill') in ('x', 'both') for f in frames)
        stretch = stretch and float(form[0]['columns'].get('1', {}).get('weight', 0)) > 0 and set('ew') <= set(entries[0]['layout'].get('sticky', '')) <= set('nsew')
    except (TypeError, ValueError):
        stretch = False
    c.add('Šířka projde až ke vstupu', stretch, 'Rámečkům dejte pack fill x, formuláři kladnou váhu sloupce 1 a vstupu sticky ew.')
c.done()
