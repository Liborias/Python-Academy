from dilna_check import check
c = check()
r = c.run()
if c.no_error(r):
    c.output_has_line(r, "2", "Vypište počet řádků souboru data.txt.")
c.done()
