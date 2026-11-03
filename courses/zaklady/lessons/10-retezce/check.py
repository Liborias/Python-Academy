from dilna_check import check
c = check()
c.uses_call("input", "Větu načtěte pomocí input().")
c.uses_call("split", "Slova spočítejte pomocí split().")
c.no_hardcoded("ahoj", "Nepište větu natvrdo, načtěte ji.")
for veta in ("ahoj světe pythone", "dobrý den", "jedna dva tři čtyři"):
    r = c.run(stdin=veta + "\n")
    if c.no_error(r, f"Běh pro „{veta}“"):
        c.output_contains(r, veta.upper(), f"Chybí věta velkými písmeny: {veta.upper()}")
        c.output_has_line(r, f"Znaků: {len(veta)}", f"Očekávám „Znaků: {len(veta)}“. Máte: {c._short(r.out)}")
        c.output_has_line(r, f"Slov: {len(veta.split())}", f"Očekávám „Slov: {len(veta.split())}“. Máte: {c._short(r.out)}")
        c.output_contains(r, veta.replace(" ", "-"), f"Chybí věta s pomlčkami: {veta.replace(' ', '-')}")
c.done()
