from dilna_check import check
c = check()
okno = (80, 160, 255)
r = c.pygame_run(frames=121, pixels=[(34, 100), (84, 100), (134, 100), (234, 100), (100, 100), (13, 100), (77, 100)], colors=[okno + (0, 60, 400, 80)])
if c.pg_no_error(r):
    c.add("Okno má velikost 400 × 200 a titulek Let rakety", r.size == [400, 200] and r.caption == "Let rakety", f"Okno {r.size}, titulek {r.caption!r}.")
    c.add("Na začátku je raketa vlevo", r.pixel((34, 100), 0) == okno, f"V prvním snímku má být okénko rakety kolem bodu (32, 100), v bodě (34, 100) je {r.pixel((34, 100), 0)}.")
    c.add("Po 10 snímcích je raketa o 50 bodů dál", r.pixel((84, 100), 10) == okno and r.pixel((34, 100), 10) != okno,
          "Za 10 snímků má raketa urazit 50 bodů (5 bodů za snímek).")
    c.add("Po 20 snímcích je raketa na x ≈ 132", r.pixel((134, 100), 20) == okno, "Raketa se nepohybuje rychlostí 5 bodů za snímek.")
    c.add("Po 40 snímcích je raketa na x ≈ 232", r.pixel((234, 100), 40) == okno, "Raketa se nepohybuje rychlostí 5 bodů za snímek.")
    c.add("Raketa letí ve výšce y = 100", r.pixel((134, 100), 20) == okno and r.pixel((134, 140), 20) != okno, "Střed rakety má být ve výšce 100.")
    c.add("Po vyletění z okna se raketa vrátí zleva", r.color_count(okno, 120, (0, 60, 400, 80)) > 50, "Po průletu okna se raketa musí objevit znovu zleva (rect.right = 0).")
    c.add("Raketa se po průletu vrátí přesně: rect.right = 0", r.pixel((13, 100), 90) == okno and r.pixel((77, 100), 90) != okno,
          "Raketa má vyletět z okna, když její levý okraj přejde 400 (rect.left > 400), a objevit se zleva tak, že její pravý okraj je v 0 (rect.right = 0).")
    c.add("Raketa je obrázek raketa.png", any(i.endswith("raketa.png") for i in r.images), "Načtěte raketa.png a vykreslete ji pomocí screen.blit.")
    c.add("Stopa za raketou nezůstává", r.pixel((100, 100), 40) == (0, 0, 30), f"V bodě (100, 100), kudy raketa už proletěla, je {r.pixel((100, 100), 40)}. Pozadí (0, 0, 30) překreslete v každém snímku (screen.fill).")
c.done()
