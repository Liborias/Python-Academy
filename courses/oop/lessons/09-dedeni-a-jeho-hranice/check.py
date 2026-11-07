from dilna_check import check

c = check()
c.defines_class('Balik')
c.defines_class('KrehkyBalik')
ns = c.load()
try:
    base, child = ns['Balik'], ns['KrehkyBalik']
    c.add('Křehký balík je potomkem Balik', issubclass(child, base), 'Uveďte Balik v závorce za názvem třídy.')
    for cls in (base, child):
        for weight in (0, -1, 1.5, '800', None, True):
            ok, error = c.call({'ctor': cls}, 'ctor', ('K-9', weight))
            c.add('Neplatná hmotnost je odmítnuta', not ok and isinstance(error, ValueError), 'Zděděný konstruktor přijímá jen kladný int, nikoli bool.')
        first, second = cls('ŽK-42', 1), cls('B-99', 13500)
        for item, code, weight in ((first, 'ŽK-42', 1), (second, 'B-99', 13500)):
            before = dict(vars(item))
            ok, result = c.call({'popis': item.popis}, 'popis')
            c.add('Zděděný popis vrací údaje konkrétního balíku', ok and result == f'Balík {code}, {weight} g' and c.last_output == ''
                  and item.kod == code and item.hmotnost_g == weight and vars(item) == before, 'Vraťte text s aktuálním kódem a hmotností bez změny stavu.')
            ok, error = c.call({'write': setattr}, 'write', (item, 'hmotnost_g', 999))
            c.add('Hmotnost je pouze pro čtení', not ok and isinstance(error, AttributeError) and item.hmotnost_g == weight, 'Zachovejte property bez možnosti přepsání.')
        first.kod = 'NOVÝ'
        c.add('Instance mají vlastní údaje', first.popis() == 'Balík NOVÝ, 1 g' and second.popis() == 'Balík B-99, 13500 g', 'Použijte údaje instance, nikoli společné údaje třídy nebo uloženou kopii popisu.')
    fragile = child('K-7', 850)
    before = dict(vars(fragile))
    ok, value = c.call({'pokyny': fragile.pokyny}, 'pokyny')
    c.add('Pokyny jsou návratová hodnota', ok and value == 'Chránit před nárazy.' and c.last_output == '' and vars(fragile) == before, 'Vraťte přesný text pokynů, nic nevypisujte ani neměňte.')
    original = base.popis
    try:
        base.popis = lambda self: ('zděděno', self.kod, self.hmotnost_g)
        c.add('Popis se skutečně dědí', fragile.popis() == ('zděděno', 'K-7', 850), 'Nekopírujte popis do potomka; využijte základní třídu.')
    finally:
        base.popis = original
except BaseException as exc:
    c.add('Třídy lze ověřit', False, f'{type(exc).__name__}: {exc}')
r = c.run()
if c.no_error(r):
    c.output_contains(r, 'Křehký je také balík: True')
c.done()
