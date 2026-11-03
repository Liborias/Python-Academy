import csv
import json
from bs4 import BeautifulSoup

# Úkol (soubor body.csv je u lekce):
#   body_podle_tridy(nazev_csv)     -> slovník {třída: součet bodů}; chybí-li soubor, {}
#   nejlepsi_zak(nazev_csv)         -> jméno žáka s nejvíce body; chybí-li soubor nebo je prázdný, None
#   uloz_jako_json(nazev_csv, cil)  -> načte CSV a uloží seznam slovníků do JSON (body jako čísla,
#                                      česky čitelně); vrátí počet žáků, chybí-li soubor, vrátí 0
#   odkazy(html)                    -> seznam adres (href) všech odkazů <a> na stránce, které mají href
