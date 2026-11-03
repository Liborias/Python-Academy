import ast
from dilna_check import check
c = check()
c.uses(ast.If, "Použijte příkaz if (a elif, else).")
for t, ocek in (("-5", "Mráz"), ("0", "Mráz"), ("1", "Chladno"), ("10", "Chladno"), ("19", "Chladno"), ("20", "Teplo"), ("35", "Teplo")):
    r = c.run(stdin=t + "\n")
    if c.no_error(r, f"Běh pro {t} °C"):
        c.output_contains(r, ocek, f"Pro teplotu {t} má program vypsat „{ocek}“. Máte: {c._short(r.out)}")
c.done()
