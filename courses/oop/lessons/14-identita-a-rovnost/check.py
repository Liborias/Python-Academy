from dilna_check import check

c = check()
c.defines_class('Adresa')
ns = c.load()
try:
    cls = ns['Adresa']
    values = ('  Žlutá 8  ', 'Nové Město', '01234')
    a, b = cls(*values), cls(*values)
    c.add('Údaje zůstávají původní texty', (a.ulice, a.mesto, a.psc) == values, 'Neořezávejte vstupy a nepřevádějte PSČ na číslo.')
    c.add('Hodnota není totožnost', a is not b and a == b and b == a and a == a, 'Dvě instance mohou mít stejnou hodnotu všech tří údajů.')
    for attr, other in [('ulice', 'Jiná 2'), ('mesto', 'Jiné Město'), ('psc', '01235')]:
        before_a = dict(vars(a))
        previous = getattr(b, attr)
        setattr(b, attr, other)
        before_b = dict(vars(b))
        ok, value = c.call({'eq': a.__eq__}, 'eq', (b,))
        c.add('Každý údaj se účastní aktuálního porovnání', ok and type(value) is bool and value is False and b != a and c.last_output == ''
              and vars(a) == before_a and vars(b) == before_b, 'Porovnejte ulici, město i PSČ bez změn stavu.')
        setattr(b, attr, previous)
        c.add('Po obnovení hodnot jsou adresy opět rovné', a == b and b == a, 'Nepořizujte zastaralou kopii hodnot pro porovnávání.')
    class JinaAdresa(cls):
        pass
    class DruhaStrana:
        def __eq__(self, other):
            return other is a
    for other in (None, 'adresa', 7, tuple(values), JinaAdresa(*values), DruhaStrana()):
        before = dict(vars(a))
        ok, value = c.call({'eq': a.__eq__}, 'eq', (other,))
        c.add('Cizí konkrétní typ vrací NotImplemented', ok and value is NotImplemented and c.last_output == '' and vars(a) == before,
              'Pro jiný konkrétní typ vraťte hodnotu NotImplemented; nevyvolávejte výjimku.')
    c.add('Python může zkusit druhou stranu', a == DruhaStrana() and not (a == 'adresa'), 'NotImplemented dovolí Pythonu pokračovat v porovnání.')
    ok, value = c.call({'eq': a.__eq__}, 'eq', (b,))
    c.add('Shoda vrací skutečný bool', ok and value is True and c.last_output == '', 'Vraťte výsledek porovnání, nikoli výpis nebo samotný objekt.')
except BaseException as exc:
    c.add('Rovnost lze ověřit', False, f'{type(exc).__name__}: {exc}')
r = c.run()
if c.no_error(r):
    for text in ('Dvě instance: False', 'Stejné údaje: True', 'Tentýž objekt: True', 'Po opravě PSČ: False', 'Původní PSČ: 60200'):
        c.output_contains(r, text)
c.done()
