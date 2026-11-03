from dilna_check import check
c = check()
c.uses_call("Sound", "Efekt načtěte pomocí pygame.mixer.Sound(\"cinknuti.wav\").")
c.uses_call("play", "Přehrání spustíte metodou play().")
r = c.pygame_run(frames=8, pixels=[(100, 100)], events={2: [{"type": "KEYDOWN", "key": "K_SPACE"}], 4: [{"type": "KEYDOWN", "key": "K_a"}], 6: [{"type": "KEYDOWN", "key": "K_SPACE"}]})
if c.pg_no_error(r):
    c.add("Pozadí je (30, 30, 30)", r.pixel((100, 100)) == (30, 30, 30), f"Barva pozadí je {r.pixel((100, 100))}.")
    m = r.music or []
    c.add("Hudba hudba.wav je načtena", any(x["call"] == "load" and x["args"] and x["args"][0].endswith("hudba.wav") for x in m), "Načtěte hudbu: pygame.mixer.music.load(\"hudba.wav\").")
    c.add("Hlasitost hudby je 0.5", any(x["call"] == "set_volume" and x["args"] and float(x["args"][0]) == 0.5 for x in m), "Nastavte pygame.mixer.music.set_volume(0.5).")
    c.add("Hudba se opakuje pořád dokola", any(x["call"] == "play" and any(a in ("-1", "loops=-1") for a in x["args"]) for x in m), "Spusťte hudbu s -1: pygame.mixer.music.play(-1).")
    c.add("Hudba se spustí jen jednou", len([x for x in m if x["call"] == "play"]) == 1, "pygame.mixer.music.play patří před smyčku (jedno spuštění).")
    snd = r.sounds or []
    c.add("Efekt cinknuti.wav se přehraje při stisku mezerníku", len(snd) == 2 and all(s["file"].endswith("cinknuti.wav") for s in snd), f"Efekt se přehrál {len(snd)}×, čekáme 2× (dva stisky mezerníku, jeden stisk jiné klávesy).")
    c.add("Efekt se přehraje ve chvíli stisku", [s["frame"] for s in snd] == [2, 6], f"Efekt se přehrál ve snímcích {[s['frame'] for s in snd]}, čekáme [2, 6].")
c.done()
