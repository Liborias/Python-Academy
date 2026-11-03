from dilna_check import check
c = check()
c.uses_call("get_pos", "Polohu myši zjistíte voláním pygame.mouse.get_pos().")
ZLUTA, CERVENA, POZADI = (255, 220, 0), (200, 60, 60), (0, 0, 30)
click = lambda pos, b: {"type": "MOUSEBUTTONDOWN", "pos": list(pos), "button": b}
r = c.pygame_run(frames=10, pixels=[(100, 100), (300, 200), (150, 120), (60, 230), (250, 50), (5, 5), (158, 120), (163, 120), (68, 230), (73, 230), (161, 120), (71, 230)], mouse={0: [100, 100], 5: [300, 200]},
                 events={3: [click((150, 120), 1)], 4: [click((250, 50), 3)], 6: [click((60, 230), 1)]})
if c.pg_no_error(r):
    c.add("Titulek je „Myš“", r.caption == "Myš", f"Titulek je {r.caption!r}.")
    c.add("Pozadí je (0, 0, 30)", r.pixel((5, 5)) == POZADI, f"V bodě (5, 5) je {r.pixel((5, 5))}.")
    c.add("Hvězda je v místě kurzoru", r.pixel((100, 100), 1) == ZLUTA and r.pixel((300, 200), 9) == ZLUTA, "Střed hvězdy má být v bodě get_pos().")
    c.add("Hvězda sleduje myš (na staré poloze už není)", r.pixel((100, 100), 9) != ZLUTA, "Hvězdu překreslujte podle aktuální polohy myši.")
    c.add("Levé kliknutí zanechá červený otisk", r.pixel((150, 120), 9) == CERVENA and r.pixel((60, 230), 9) == CERVENA, "Při MOUSEBUTTONDOWN s button == 1 uložte pozici a kreslete ji v každém snímku.")
    c.add("Otisk má poloměr 10", r.pixel((158, 120), 9) == CERVENA and r.pixel((68, 230), 9) == CERVENA and r.pixel((161, 120), 9) == POZADI and r.pixel((71, 230), 9) == POZADI and r.pixel((163, 120), 9) == POZADI and r.pixel((73, 230), 9) == POZADI,
          "Kruh otisku má mít poloměr 10: bod 8 napravo od středu má být červený a 11 napravo už ne.")
    c.add("Otisk se neobjeví před kliknutím", r.pixel((150, 120), 2) == POZADI, "Otisk se má objevit až po kliknutí.")
    c.add("Pravé tlačítko nic nedělá", r.pixel((250, 50), 9) == POZADI, "Otisk dělejte jen pro levé tlačítko (udalost.button == 1).")
c.done()
