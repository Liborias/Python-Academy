def nadpis(html):
    zacatek = html.find("<h1>")
    if zacatek == -1:
        return ""
    zacatek += len("<h1>")
    konec = html.find("</h1>", zacatek)
    return html[zacatek:konec]


def pocet_polozek(html):
    return html.count("<li>")


def odkazy(html):
    adresy = []
    znacka = 'href="'
    pozice = html.find(znacka)
    while pozice != -1:
        zacatek = pozice + len(znacka)
        konec = html.find('"', zacatek)
        adresy.append(html[zacatek:konec])
        pozice = html.find(znacka, konec)
    return adresy
