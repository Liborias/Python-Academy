from dilna_check import check
c = check()
c.uses_call("input", "Použijte input() pro načtení věku.")
c.uses_call("int", "Odpověď z input() je text, převeďte ji pomocí int().")
for zadano, ocek in (("15", "16"), ("30", "31"), ("0", "1")):
    r = c.run(stdin=zadano + "\n")
    if c.no_error(r, f"Běh se vstupem {zadano}"):
        c.output_contains(r, f"Za rok ti bude {ocek}.", f"Pro vstup {zadano} očekávám „Za rok ti bude {ocek}.“. Máte: {c._short(r.out)}")
c.done()
