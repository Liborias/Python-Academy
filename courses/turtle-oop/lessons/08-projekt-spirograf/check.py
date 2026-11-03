from dilna_check import check
import ast
import math
c = check()
near = lambda a, b, t=1.0: abs(a - b) <= t
c.uses_call("hideturtle|ht", "Schovejte želvu: t.hideturtle().")
c.uses_call("speed", "Nastavte rychlost: t.speed(0).")
r = c.turtle_run()
if c.turtle_no_error(r):
    c.add("Program končí příkazem turtle.done()", r.mainloop, "Na konec přidejte turtle.done(), aby okno zůstalo otevřené.")
    barvy = ["red", "orange", "yellow", "green", "blue", "purple"]
    c.add("Pozadí je černé", r.bgcolor == "black", f"Pozadí má být black, ale je {r.bgcolor!r}.")
    c.add("Je nakresleno 36 kruhů", r.called("circle") == 36, f"Kruhů je {r.called('circle')}, čekáme 36.")
    c.add("Použito je šest barev ze seznamu", r.colors() == set(barvy), f"Barvy čáry: {sorted(r.colors())}.")
    ds = [r.length(b) for b in barvy]
    c.add("Každá barva se použila stejně často (6 kruhů)", min(ds) > 0 and max(ds) / min(ds) < 1.01, f"Délky čar podle barev: {[round(d) for d in ds]}. Barvy se mají střídat cyklicky (barvy[i % 6]).")
    box = r.bbox()
    c.add("Obrazec je široký asi 320 a vysoký asi 320", box is not None and near(box[2] - box[0], 320, 6) and near(box[3] - box[1], 320, 6) and near((box[0] + box[2]) / 2, 0, 4) and near((box[1] + box[3]) / 2, 0, 4),
          f"Obrazec má mít kruhy poloměru 80 pootočené po 10° kolem bodu (0, 0), tedy rozměr asi 320 × 320 se středem v (0, 0). Má rozměr {box}.")
    kr = [s for s in r.segments if s[7] == "circle"]
    n = len(kr) // 36 if kr else 0
    stredy = [(sum((s[0] + s[2]) / 2 for s in kr[i * n:(i + 1) * n]) / n, sum((s[1] + s[3]) / 2 for s in kr[i * n:(i + 1) * n]) / n) for i in range(36)] if n and len(kr) == 36 * n else []
    cekane = [(80 * math.cos(math.radians(90 + 10 * i)), 80 * math.sin(math.radians(90 + 10 * i))) for i in range(36)]
    c.add("Každý kruh je pootočený o 10° (středy kruhů leží na kružnici)", bool(stredy) and all(math.hypot(a[0] - b[0], a[1] - b[1]) < 3 for a, b in zip(stredy, cekane)),
          "Po každém kruhu se pootočte doleva o 10° (t.left(10)), takže se středy kruhů postupně posouvají po kružnici kolem bodu (0, 0).")
    c.add("Rychlost je 0", bool(r.turtles) and r.turtles[0]["speed"] == 0, "Nastavte nejrychlejší kreslení: t.speed(0).")
    c.add("Tloušťka čáry je 2", r.widths() == {2}, f"Tloušťka čáry má být 2, ale je {sorted(r.widths())}.")
    h = r.turtles[0]["heading"] if r.turtles else 99
    c.add("Želva je schovaná a míří doprava", bool(r.turtles) and not r.turtles[0]["visible"] and (h < 0.5 or h > 359.5),
          "Po 36 otočkách o 10° se želva dívá zase doprava. Schovejte ji příkazem hideturtle().")
c.done()
