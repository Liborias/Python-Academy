from dilna_check import check
c = check()
ns = c.load()
if ns is not None:
    c.returns(ns, 'analyza', ('Kočka běží. Kočka spí, pes běží!',), {'slov': 6, 'unikatnich': 4, 'nejdelsi': 'kočka', 'nejcastejsi': 'běží', 'prumerna_delka': 4.0})
    c.returns(ns, 'analyza', ('',), {'slov': 0, 'unikatnich': 0, 'nejdelsi': '', 'nejcastejsi': '', 'prumerna_delka': 0})
    c.returns(ns, 'analyza', ('... - !!!',), {'slov': 0, 'unikatnich': 0, 'nejdelsi': '', 'nejcastejsi': '', 'prumerna_delka': 0})
    c.returns(ns, 'analyza', ('Pes',), {'slov': 1, 'unikatnich': 1, 'nejdelsi': 'pes', 'nejcastejsi': 'pes', 'prumerna_delka': 3.0})
    c.returns(ns, 'analyza', ('a b a b c',), {'slov': 5, 'unikatnich': 3, 'nejdelsi': 'a', 'nejcastejsi': 'a', 'prumerna_delka': 1.0})
    c.returns(ns, 'analyza', ('Ahoj, AHOJ! ahoj?',), {'slov': 3, 'unikatnich': 1, 'nejdelsi': 'ahoj', 'nejcastejsi': 'ahoj', 'prumerna_delka': 4.0})
    c.returns(ns, 'analyza', ('aa bb cc bb cc',), {'slov': 5, 'unikatnich': 3, 'nejdelsi': 'aa', 'nejcastejsi': 'bb', 'prumerna_delka': 2.0})
    c.returns(ns, 'analyza', ('jedna dva tři',), {'slov': 3, 'unikatnich': 3, 'nejdelsi': 'jedna', 'nejcastejsi': 'dva', 'prumerna_delka': 3.67})
    c.returns(ns, 'analyza', ('  mezery   všude  ',), {'slov': 2, 'unikatnich': 2, 'nejdelsi': 'mezery', 'nejcastejsi': 'mezery', 'prumerna_delka': 5.5})
c.done()
