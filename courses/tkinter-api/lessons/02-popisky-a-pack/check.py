from dilna_check import check

c = check()
r = c.tk_run()
def enough(value):
    try:
        return all(float(v) >= 8 for v in value) if isinstance(value, (tuple, list)) and len(value) == 2 else float(value) >= 8
    except (TypeError, ValueError):
        return False
if c.tk_no_error(r):
    roots, labels = r.widgets('root'), r.widgets('label')
    c.add('Nástěnka má jedno viditelné okno a smyčku', len(roots) == 1 and roots[0]['visible'] and roots[0]['title'] == 'Nástěnka' and r.mainloops == 1, 'Ponechte připravené hlavní okno a mainloop.')
    c.add('Dva popisky bez dalších ovládacích prvků', len(labels) == 2 and len(r.widgets()) == 3, 'Vytvořte právě dva popisky.')
    ordered = sorted(labels, key=lambda w: w['order'])
    c.add('Správné texty v pořadí pack', [w['text'] for w in ordered] == ['Expediční přehled', 'Stav: připraveno'], 'Nadpis umístěte před stavový popisek.')
    c.add('Oba popisky jsou v okně přes pack', len(roots) == 1 and len(labels) == 2 and all(w['parent'] == roots[0]['id'] and w['visible'] and w['manager'] == 'pack' for w in labels), 'Předávejte hlavní okno jako rodiče a každý popisek umístěte pomocí pack.')
    c.add('Vnější mezery kolem textů', len(labels) == 2 and all(enough(w['layout'].get('padx', 0)) and enough(w['layout'].get('pady', 0)) for w in labels), 'U obou pack nastavte padx a pady alespoň 8 pixelů.')
c.done()
