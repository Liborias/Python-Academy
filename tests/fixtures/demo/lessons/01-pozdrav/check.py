from dilna_check import check
c = check()
r = c.run(stdin="Eva\n")
if c.no_error(r):
    c.output_contains(r, "Ahoj Eva", "Program má pozdravit zadané jméno.")
c.uses_call("input")
c.done()
