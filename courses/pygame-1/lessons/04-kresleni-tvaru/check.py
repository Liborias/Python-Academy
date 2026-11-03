from dilna_check import check
c = check()
for tvar, kod in (("rect", "obdélníky"), ("polygon", "střechu"), ("circle", "slunce")):
    c.uses_call(tvar, f"Použijte pygame.draw.{tvar} na {kod}.")
body = {"obloha": ((20, 20), (135, 206, 235)), "tráva": ((20, 280), (34, 139, 34)), "zeď": ((200, 200), (160, 110, 60)),
        "střecha": ((200, 120), (200, 40, 40)), "slunce": ((340, 50), (255, 220, 0)),
        "obloha vedle slunce": ((340, 90), (135, 206, 235)), "horní okraj slunce": ((340, 23), (255, 220, 0)), "pod sluncem": ((340, 85), (135, 206, 235)), "obloha vedle střechy": ((100, 120), (135, 206, 235)),
        "tráva pod domem": ((200, 250), (34, 139, 34)),
        "zeď vlevo nahoře": ((150, 142), (160, 110, 60)), "zeď vpravo dole": ((249, 219), (160, 110, 60)),
        "obloha vlevo od zdi": ((149, 180), (135, 206, 235)), "obloha vpravo od zdi": ((250, 180), (135, 206, 235)),
        "tráva vlevo dole": ((0, 220), (34, 139, 34)), "tráva vpravo dole": ((399, 299), (34, 139, 34)), "obloha nad trávou": ((0, 219), (135, 206, 235)),
        "vrchol střechy": ((200, 95), (200, 40, 40)), "obloha nad střechou": ((200, 85), (135, 206, 235)),
        "střecha vlevo": ((150, 139), (200, 40, 40)), "střecha vpravo": ((250, 139), (200, 40, 40)),
        "obloha vlevo od střechy": ((130, 139), (135, 206, 235)), "obloha vpravo od střechy": ((270, 139), (135, 206, 235))}
r = c.pygame_run(frames=3, pixels=[p for p, _ in body.values()])
if c.pg_no_error(r):
    c.add("Okno má velikost 400 × 300", r.size == [400, 300], f"Okno má velikost {r.size}.")
    for jmeno, (bod, barva) in body.items():
        c.add(f"Správná barva: {jmeno}", r.pixel(bod) == barva, f"V bodě {bod} je barva {r.pixel(bod)}, čekáme {barva}.")
    c.add("Obrázek se kreslí v každém snímku (smyčka)", len(r.drew("circle")) >= 2, "Kreslení patří dovnitř herní smyčky.")
c.done()
