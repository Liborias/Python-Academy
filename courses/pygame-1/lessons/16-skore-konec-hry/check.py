from dilna_check import check
c = check()
space = lambda f: {"type": "KEYDOWN", "key": "K_SPACE"}
ev = {1: [space(1)], 4: [space(4)], 7: [space(7)], 8: [{"type": "KEYDOWN", "key": "K_r"}], 10: [space(10)], 13: [space(13)],
      18: [space(18)], 21: [{"type": "KEYDOWN", "key": "K_r"}]}
Z, B = (255, 220, 0), (255, 255, 255)
r = c.pygame_run(frames=26, pixels=[(5, 5)], events=ev, colors=[B, B + (0, 0, 200, 40), Z, Z + (0, 80, 400, 60), B + (0, 150, 400, 40), B + (0, 200, 400, 40)])
if c.pg_no_error(r):
    v = lambda f: {t["text"] for t in (r.texts or []) if t["frame"] == f}
    c.add("Titulek je „Konec hry“", r.caption == "Konec hry", f"Titulek je {r.caption!r}.")
    c.add("Na začátku je zobrazeno „Skóre: 0“", "Skóre: 0" in v(0), f"V prvním snímku jsou vykreslené texty {sorted(v(0))}.")
    c.add("Stisk mezerníku zvýší skóre o 1", "Skóre: 1" in v(3) and "Skóre: 2" in v(6), f"Ve snímku 3: {sorted(v(3))}, ve snímku 6: {sorted(v(6))}.")
    c.add("Klávesa R v průběhu hry skóre nevynuluje", "Skóre: 3" in v(9), f"Ve snímku 9: {sorted(v(9))}. Klávesa R má fungovat jen ve stavu konec.")
    c.add("Před pátým bodem ještě není konec", "Konec hry" not in v(12) and "Skóre: 4" in v(12), f"Ve snímku 12: {sorted(v(12))}.")
    c.add("Pozadí hry je (0, 0, 30)", r.pixel((5, 5), 12) == (0, 0, 30), f"Pozadí ve hře je {r.pixel((5, 5), 12)}.")
    c.add("Po pátém bodu je zobrazen konec hry", {"Konec hry", "Skóre: 5"} <= v(16), f"Ve snímku 16: {sorted(v(16))}.")
    c.add("Při konci hry je zobrazeno „Stiskni R“", "Stiskni R" in v(16), "Obrazovka konce hry má obsahovat text Stiskni R.")
    c.add("Skóre ve hře je bílé, písmo 32, vlevo nahoře", r.color_count(B, 12, (0, 0, 200, 40)) == r.color_count(B, 12) and 330 <= r.color_count(B, 12) <= 410,
          f"Bílých bodů vlevo nahoře: {r.color_count(B, 12, (0, 0, 200, 40))} z {r.color_count(B, 12)} (čekáme asi 370). Text Skóre: N má být bílý, písmo 32, get_rect(topleft=(10, 10)).")
    c.add("„Konec hry“ je žlutý, písmo 64, na (200, 110)", r.color_count(Z, 16) == r.color_count(Z, 16, (0, 80, 400, 60)) and 2000 <= r.color_count(Z, 16) <= 2500,
          f"Žlutých bodů: {r.color_count(Z, 16)} (čekáme asi 2240, písmo 64, střed (200, 110)).")
    c.add("„Skóre: 5“ a „Stiskni R“ jsou bílé, písmo 32, na svých místech", 320 <= r.color_count(B, 16, (0, 150, 400, 40)) <= 410 and 440 <= r.color_count(B, 16, (0, 200, 400, 40)) <= 540,
          f"Bílých bodů v řádku skóre: {r.color_count(B, 16, (0, 150, 400, 40))}, v řádku Stiskni R: {r.color_count(B, 16, (0, 200, 400, 40))} (středy (200, 170) a (200, 220), písmo 32).")
    c.add("Pozadí konce hry je (60, 0, 0)", r.pixel((5, 5), 16) == (60, 0, 0), f"Pozadí při konci hry je {r.pixel((5, 5), 16)}.")
    c.add("Po konci hry mezerník skóre nezvýší", "Skóre: 5" in v(20) and not any(t.startswith("Skóre: 6") for t in v(20)), f"Ve snímku 20: {sorted(v(20))}.")
    c.add("Klávesa R po konci hry hru restartuje", "Skóre: 0" in v(24) and "Konec hry" not in v(24) and r.pixel((5, 5), 24) == (0, 0, 30), f"Ve snímku 24: {sorted(v(24))}.")
c.done()
