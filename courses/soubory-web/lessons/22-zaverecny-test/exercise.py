import json
import requests
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser

# Úkol: viz text lekce.
#   nejlevnejsi(knihy)                          -> slovník nejlevnější knihy, nebo None
#   prumerna_cena(knihy)                        -> průměr zaokrouhlený na 1 desetinné místo, nebo 0
#   sber_cen(adresa, nazev_json, cesta="/knihy.html")
#                                               -> slovník s výsledkem (a uloží ho do JSON), nebo None
