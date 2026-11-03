from bs4 import BeautifulSoup

with open("stranka.html", encoding="utf-8") as soubor:
    soup = BeautifulSoup(soubor.read(), "html.parser")    # HTML jako text, druhý parametr je rozbor

print(soup.find("h1").get_text())                         # text prvního nadpisu: Zvířata v ZOO

info = soup.find("p", class_="info")                      # class_ s podtržítkem, class je v Pythonu vyhrazené
print(info.get_text(strip=True))                          # strip=True smaže mezery okolo textu

odkaz = soup.find("a")
print(odkaz["href"], "/", odkaz.get("title"))             # get vrátí None, pokud atribut chybí
