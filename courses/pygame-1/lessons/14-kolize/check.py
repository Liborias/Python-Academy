from dilna_check import check
c = check()
c.uses_call("colliderect", "Dotyk obdélníků zjistíte metodou colliderect.")
c.uses_call("collidepoint", "Kliknutí do hvězdy zjistíte metodou collidepoint.")
ZELENA, POZADI = (0, 60, 0), (0, 0, 30)
klik = lambda pos: {"type": "MOUSEBUTTONDOWN", "pos": list(pos), "button": 1}
r = c.pygame_run(frames=85, pixels=[(10, 10), (300, 100)], held={1: ["K_RIGHT"], 52: ["K_LEFT"]}, mouse={2: [300, 100], 4: [50, 150], 6: [310, 110], 8: [330, 100]},
                 events={3: [klik((300, 100))], 5: [klik((50, 150))], 7: [klik((310, 110))], 9: [klik((330, 100))]})
if c.pg_no_error(r):
    c.add("Na začátku je pozadí (0, 0, 30)", r.pixel((10, 10), 0) == POZADI, f"V prvním snímku je pozadí {r.pixel((10, 10), 0)}.")
    c.add("Před dotykem je pozadí (0, 0, 30)", r.pixel((10, 10), 20) == POZADI and r.pixel((10, 10), 35) == POZADI, "Pozadí se má změnit až při dotyku.")
    c.add("Při dotyku je pozadí zelené (0, 60, 0)", r.pixel((10, 10), 50) == ZELENA, f"V 50. snímku se raketa dotýká hvězdy, ale pozadí je {r.pixel((10, 10), 50)}.")
    c.add("Po odjezdu od hvězdy se pozadí vrátí na (0, 0, 30)", r.pixel((10, 10), 55) == ZELENA and r.pixel((10, 10), 84) == POZADI,
          f"Raketa se hvězdy už nedotýká, pozadí má být (0, 0, 30), ale je {r.pixel((10, 10), 84)}. Barvu vybírejte v každém snímku znovu (if / else).")
    c.add("Kliknutí do hvězdy vypíše „Zásah!“ (2×)", r.out.count("Zásah!") == 2, f"Program vypsal {r.out.count('Zásah!')}× Zásah!, čekáme 2× (dvě kliknutí do hvězdy, dvě mimo).")
c.done()
