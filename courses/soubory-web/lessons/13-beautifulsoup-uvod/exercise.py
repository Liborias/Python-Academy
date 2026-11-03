from bs4 import BeautifulSoup

# Úkol (funkce dostávají HTML jako text; stranka.html je ve složce programu).
# Ve všech funkcích použijte metodu find (kontrola to vyžaduje). Texty vracejte bez mezer na okrajích:
#   nadpis(html)             -> text prvního <h1> (bez mezer na okrajích), nebo None
#   prvni_odstavec(html)     -> text prvního <p>, nebo None
#   prvni_odkaz(html)        -> (text, href) prvního <a>; bez href je adresa None; bez odkazu None
#   text_s_id(html, id_)     -> text značky s daným id, nebo None
#   text_s_tridou(html, trida) -> text první značky s danou třídou, nebo None
