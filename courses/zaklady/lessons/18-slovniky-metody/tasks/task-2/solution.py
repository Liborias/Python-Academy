def telefon(kontakty, jmeno):
    return kontakty.get(jmeno, "nenalezeno")

print(telefon({'Ema': '123'}, 'Ema'))
