def pridej_ukol(ukoly, text):
    ukoly.append({"text": text, "hotovo": False})
    return ukoly


def dokonc_ukol(ukoly, cislo):
    if cislo < 1 or cislo > len(ukoly):
        return False
    ukoly[cislo - 1]["hotovo"] = True
    return True


def procento_hotovo(ukoly):
    if not ukoly:
        return 0
    hotovo = 0
    for ukol in ukoly:
        if ukol["hotovo"]:
            hotovo += 1
    return hotovo / len(ukoly) * 100


def zpracuj_prikaz(ukoly, prikaz):
    casti = prikaz.split(" ", 1)
    slovo = casti[0]
    if slovo == "seznam" and len(casti) == 1:
        if not ukoly:
            return "Žádné úkoly."
        radky = []
        for cislo, ukol in enumerate(ukoly, 1):
            znacka = "x" if ukol["hotovo"] else " "
            radky.append(f"{cislo}. [{znacka}] {ukol['text']}")
        return "\n".join(radky)
    if slovo == "pridej" and len(casti) == 2:
        pridej_ukol(ukoly, casti[1])
        return "Přidáno: " + casti[1]
    if slovo == "hotovo":
        try:
            cislo = int(casti[1])
        except (IndexError, ValueError):
            return "Neplatné číslo."
        if dokonc_ukol(ukoly, cislo):
            return "Hotovo: " + ukoly[cislo - 1]["text"]
        return "Neplatné číslo."
    return "Neznámý příkaz."


def hlavni_smycka(ukoly):
    while True:
        prikaz = input("> ").strip()
        if prikaz == "konec":
            break
        print(zpracuj_prikaz(ukoly, prikaz))


if __name__ == "__main__":
    hlavni_smycka([])
