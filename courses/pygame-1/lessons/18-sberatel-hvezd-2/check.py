import ast
from dilna_check import check
c = check()
c.uses_call("Sound", "Efekt načtěte: pygame.mixer.Sound(\"cinknuti.wav\").")
Z = (255, 220, 0)
r = c.pygame_run(frames=272, pixels=[(5, 495), (46, 34), (200, 450)], held={210: ["K_LEFT"], 220: []}, events={192: [{"type": "KEYDOWN", "key": "K_r"}], 262: [{"type": "KEYDOWN", "key": "K_r"}]},
                 colors=[(255, 255, 255, 0, 0, 200, 40), (255, 255, 255, 0, 30, 200, 40), Z, (255, 220, 0, 0, 170, 400, 60), (255, 255, 255, 0, 240, 400, 40), (255, 255, 255, 0, 290, 400, 40)])
if c.pg_no_error(r):
    v = lambda f: {t["text"] for t in (r.texts or []) if t["frame"] == f}
    c.add("Titulek je „Sběratel hvězd“ a okno 400 × 500", r.caption == "Sběratel hvězd" and r.size == [400, 500], f"Titulek {r.caption!r}, okno {r.size}.")
    c.add("Na začátku jsou 3 životy a skóre 0", {"Skóre: 0", "Životy: 3"} <= v(100), f"Ve snímku 100 jsou texty {sorted(v(100))}.")
    c.add("Chycená hvězda neubírá život", "Životy: 2" in v(180) and "Skóre: 0" in v(160), f"Ve snímku 180: {sorted(v(180))}.")
    c.add("Hvězda 0 spadla pod okno: 2 životy, skóre 0", {"Životy: 2", "Skóre: 0"} <= v(175), f"Ve snímku 175: {sorted(v(175))}.")
    c.add("Hvězda 2 chycena: skóre 1, životy zůstaly", {"Skóre: 1", "Životy: 2"} <= v(190), f"Ve snímku 190: {sorted(v(190))}.")
    c.add("Klávesa R v průběhu hry nic nedělá", {"Skóre: 1", "Životy: 1"} <= v(196), f"Ve snímku 196: {sorted(v(196))}. Klávesa R má fungovat jen ve stavu konec.")
    c.add("Hvězda 1 spadla pod okno: 1 život", {"Životy: 1", "Skóre: 1"} <= v(205), f"Ve snímku 205: {sorted(v(205))}.")
    c.add("Před posledním životem ještě není konec", "Konec hry" not in v(240), f"Ve snímku 240: {sorted(v(240))}.")
    c.add("Po ztrátě všech životů je konec hry", {"Konec hry", "Skóre: 1", "Stiskni R"} <= v(258), f"Ve snímku 258: {sorted(v(258))}.")
    c.add("Pozadí konce hry je (60, 0, 0)", r.pixel((5, 495), 258) == (60, 0, 0), f"Pozadí při konci hry je {r.pixel((5, 495), 258)}.")
    c.add("Po restartu jsou 3 životy a skóre 0", {"Skóre: 0", "Životy: 3"} <= v(268) and "Konec hry" not in v(268), f"Ve snímku 268: {sorted(v(268))}.")
    c.add("Po restartu hvězdy začínají znovu odshora", r.pixel((46, 34), 268) == Z, f"V bodě (46, 34) má být 6 snímků po restartu střed hvězdy 0, ale je tam {r.pixel((46, 34), 268)}. Při restartu vraťte hvězdy na počáteční místa.")
    c.add("Po restartu je raketa zase uprostřed dole", r.pixel((200, 450), 268) == (80, 160, 255), f"V bodě (200, 450) je {r.pixel((200, 450), 268)}. Při restartu vraťte střed rakety na (200, 450).")
    c.add("Po restartu je pozadí hry (0, 0, 30)", r.pixel((5, 495), 268) == (0, 0, 30), f"Pozadí po restartu je {r.pixel((5, 495), 268)}.")
    if c.tree is not None:
        if_stav = [n for n in ast.walk(c.tree) if isinstance(n, ast.If) and ("stav" in ast.unparse(n.test) or "zivoty" in ast.unparse(n.test))]
        c.add("Pohyb a kolize jsou jen ve stavu hra", any(c.calls_in(n, "colliderect") for n in if_stav),
              "Dotyk rakety a hvězdy (colliderect) zjišťujte jen uvnitř if, který testuje stav hry (nebo počet životů).")
    snd = r.sounds or []
    cink = [s for s in snd if s["file"].endswith("cinknuti.wav")]
    c.add("Zvuk cinknuti.wav se přehrál při chycení hvězdy", len(cink) == 1 and 181 <= cink[0]["frame"] <= 186, f"Přehrané zvuky: {snd}. Hvězda 2 se chytá kolem snímku 183.")
    m = r.music or []
    c.add("Hraje hudba.wav pořád dokola při hlasitosti 0.3",
          any(x["call"] == "load" and x["args"] and x["args"][0].endswith("hudba.wav") for x in m)
          and any(x["call"] == "play" and any(a in ("-1", "loops=-1") for a in x["args"]) for x in m)
          and any(x["call"] == "set_volume" and x["args"] and float(x["args"][0]) == 0.3 for x in m),
          "Načtěte hudba.wav, nastavte hlasitost 0.3 a spusťte ji s -1.")
    zl, bi = r.color_count((255, 255, 255), 100, (0, 0, 200, 40)), r.color_count((255, 255, 255), 100, (0, 30, 200, 40))
    c.add("Skóre a životy jsou bílé, písmo 32, na (10, 10) a (10, 40)", 330 <= zl <= 410 and 330 <= bi <= 430, f"Bílých bodů v řádku skóre: {zl}, v řádku životů: {bi} (čekáme asi 360 a 370).")
    c.add("„Konec hry“ je žlutý, písmo 64, na (200, 200)", r.color_count(Z, 258) == r.color_count(Z, 258, (0, 170, 400, 60)) and 2000 <= r.color_count(Z, 258) <= 2500, f"Žlutých bodů: {r.color_count(Z, 258)} (čekáme asi 2240, střed (200, 200)).")
    c.add("„Skóre“ a „Stiskni R“ na obrazovce konce jsou bílé, písmo 32, na (200, 260) a (200, 310)", 320 <= r.color_count((255, 255, 255), 258, (0, 240, 400, 40)) <= 410 and 440 <= r.color_count((255, 255, 255), 258, (0, 290, 400, 40)) <= 540, f"Bílých bodů: {r.color_count((255, 255, 255), 258, (0, 240, 400, 40))} a {r.color_count((255, 255, 255), 258, (0, 290, 400, 40))}.")
    c.add("Obrazovka konce se nemění", {t for t in v(259)} == {t for t in v(261)}, "Po konci hry se kreslí pořád stejná obrazovka.")
    c.add("Hra ve stavu konec nehýbe hvězdami (obrazovka konce se nemění)", r.pixel((5, 495), 250) == (60, 0, 0) and r.pixel((5, 495), 258) == (60, 0, 0), "Po konci hry se kreslí jen obrazovka konce hry.")
c.done()
