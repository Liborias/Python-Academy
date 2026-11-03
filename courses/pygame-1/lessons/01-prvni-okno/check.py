from dilna_check import check
c = check()
c.uses_call("init", "Zapněte pygame: pygame.init().")
c.uses_call("wait", "Počkejte 3 sekundy: pygame.time.wait(3000).")
c.uses_call("quit", "Na konci pygame vypněte: pygame.quit().")
c.uses_call("set_mode", "Otevřete okno: pygame.display.set_mode((400, 300)).")
r = c.pygame_run(frames=3, pixels=[(0, 0), (200, 150), (399, 299)])
if c.pg_no_error(r):
    c.add("Okno se zobrazilo (display.flip)", r.frames >= 1, "Zavolejte pygame.display.flip().")
    c.add("Okno má velikost 400 × 300", r.size == [400, 300], f"Okno má velikost {r.size}.")
    c.add("Titulek je „Moje první okno“", r.caption == "Moje první okno", f"Titulek je {r.caption!r}.")
    for bod in ((0, 0), (200, 150), (399, 299)):
        c.add(f"Bod {bod} je světle modrý", r.pixel(bod) == (135, 206, 235), f"V bodě {bod} je barva {r.pixel(bod)}.")
c.done()
