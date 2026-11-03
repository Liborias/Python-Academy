import time
import requests
from urllib.robotparser import RobotFileParser
from dilna_web import spust

adresa = spust()

text = requests.get(adresa + "/robots.txt", timeout=3).text
pravidla = RobotFileParser()
pravidla.parse(text.splitlines())                   # pravidla ze souboru robots.txt

print(pravidla.can_fetch("dilna", adresa + "/index.html"))             # True: tohle smíme
print(pravidla.can_fetch("dilna", adresa + "/soukrome/tajne.html"))    # False: zakázáno všem
print(pravidla.can_fetch("zlybot", adresa + "/index.html"))            # False: tomuto robotovi je zakázáno vše

hlavicky = {"User-Agent": "Skola-Python/1.0"}                          # představíme se serveru
print(requests.get(adresa + "/_hlavicky", headers=hlavicky, timeout=3).json()["user-agent"])

for cislo in (1, 2):
    print(requests.get(f"{adresa}/clanky/{cislo}.html", timeout=3).text.strip())
    time.sleep(0.2)                                 # slušná pauza mezi dotazy
