import time
import requests
from urllib.robotparser import RobotFileParser

# Úkol:
#   smi_stahovat(adresa, cesta, agent="dilna")
#       -> True/False podle souboru adresa + "/robots.txt" (např. smi_stahovat(A, "/index.html"));
#          když robots.txt neexistuje (404), je dovoleno vše
#   stahni_jako(url, agent)
#       -> text stránky; na server pošle hlavičku User-Agent s hodnotou `agent`
#   stahni_slusne(urls, pauza=1.0)
#       -> seznam textů všech stránek v pořadí; mezi dotazy počká `pauza` sekund
