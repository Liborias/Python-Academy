with open("stranka.html", encoding="utf-8") as soubor:   # HTML je obyčejný text
    html = soubor.read()

zacatek = html.find("<title>") + len("<title>")            # find vrátí pozici, kde text začíná
konec = html.find("</title>")                               # pozice konce značky
print(html[zacatek:konec])                                  # řez textu mezi značkami: Zvířata v ZOO

print(html.count("<li>"))                                   # count spočítá výskyty: 3
print(html.find("neexistuje"))                              # -1: text tam není
