import requests
from bs4 import BeautifulSoup

# Úkol (všechny funkce dostávají celou adresu, např. "http://127.0.0.1:50321/index.html"):
#   stahni_text(url)    -> text stránky
#   stavovy_kod(url)    -> číselný stavový kód odpovědi (200, 404 ...)
#   nacti_json(url)     -> obsah JSON jako slovník nebo seznam
#   nadpis(url)         -> text prvního h1 na stránce, nebo None (když stránka h1 nemá)
