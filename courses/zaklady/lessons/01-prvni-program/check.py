from dilna_check import check
c = check()
r = c.run()
if c.no_error(r):
    c.output_equals(r, "Ahoj, světe!\nZačínám s Pythonem.", "Program má vypsat přesně dva řádky: „Ahoj, světe!“ a „Začínám s Pythonem.“")
c.uses_call("print", "Použijte příkaz print().")
c.done()
