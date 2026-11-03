from bs4 import BeautifulSoup

# Úkol (funkce dostávají HTML jako text; produkty.html je ve složce programu):
#   nazvy(html)               -> názvy produktů (h3 uvnitř .produkt)
#   ceny(html)                -> ceny produktů jako celá čísla ("12 Kč" -> 12), bez patičky
#   skladem(html)             -> názvy produktů bez třídy vyprodano
#   odkaz_produktu(html, id_) -> adresa odkazu v produktu s daným id, nebo None
