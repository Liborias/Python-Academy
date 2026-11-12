import unittest
from model import Pujcovna
from sada import vytvor_sadu

if __name__ == '__main__':
    r=unittest.TextTestRunner(verbosity=2).run(vytvor_sadu(Pujcovna))
    raise SystemExit(0 if r.wasSuccessful() else 1)
