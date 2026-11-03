class Zvire:
    pass                         # Třída zatím nemá vlastní metody.


vydra = Zvire()                   # První konkrétní objekt.
vydra.jmeno = "Vydra"
vydra.energie = 8
jezevec = Zvire()                 # Nová instance má vlastní údaje.
jezevec.jmeno = "Jezevec"
jezevec.energie = 3
vydra.energie += 1
print(vydra.jmeno, vydra.energie)  # Vydra 9
print(jezevec.jmeno, jezevec.energie)  # Jezevec 3

stejna = vydra                    # Jen další odkaz, nikoli nové zvíře.
stejna.energie = 10
print(vydra.energie)              # 10: změna se týká téhož objektu.
