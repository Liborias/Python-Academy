from dilna_check import check
c = check()
c.defines_function("pozdrav", 0, "Vytvořte funkci bez parametrů: def pozdrav():")
f = c.function("pozdrav")
c.add("Výpis je uvnitř funkce pozdrav", bool(f and c.calls_in(f, "print")), "Příkaz print() musí být odsazený uvnitř funkce pozdrav.")
volani = [n for n in c._walk() if getattr(getattr(n, "func", None), "id", "") == "pozdrav"]
c.add("Funkce pozdrav se volá dvakrát", len(volani) >= 2, "Za definicí funkci dvakrát zavolejte: pozdrav() a pozdrav().")
r = c.run()
if c.no_error(r):
    c.output_equals(r, "Ahoj z funkce!\nAhoj z funkce!", "Funkce se má zavolat dvakrát, výstup jsou dva řádky „Ahoj z funkce!“. Máte: " + c._short(r.out))
c.done()
