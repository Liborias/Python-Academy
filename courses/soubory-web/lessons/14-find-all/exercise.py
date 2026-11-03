from bs4 import BeautifulSoup

# Úkol (funkce dostávají HTML jako text; obchod.html je ve složce programu):
#   polozky(html, trida=None)  -> texty všech <li> (případně jen s danou třídou)
#   odkazy(html)               -> seznam (text, adresa) všech <a>, které mají atribut href (i prázdný)
#   tabulka(html)              -> řádky tabulky jako seznamy textů buněk <td>, hlavičku přeskočit
#   ceny(html)                 -> slovník {zboží: cena jako celé číslo} z tabulky
