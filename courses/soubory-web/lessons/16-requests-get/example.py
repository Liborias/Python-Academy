import requests
from dilna_web import spust

adresa = spust()   # spustí místní server a vrátí jeho adresu

odpoved = requests.get(adresa + "/index.html")
print(odpoved.status_code)                 # 200: vše je v pořádku
print(odpoved.headers["content-type"])     # text/html; charset=utf-8: druh obsahu
print(odpoved.text[:15])                   # začátek textu stránky

data = requests.get(adresa + "/data.json").json()   # JSON se rovnou změní na slovník
print(data["mesto"], data["teplota"])

print(requests.get(adresa + "/neexistuje.html").status_code)   # 404: stránka není
