from bs4 import BeautifulSoup


def nadpis(html):
    soup = BeautifulSoup(html, "html.parser")
    znacka = soup.find("h1")
    if znacka is None:
        return None
    return znacka.get_text(strip=True)


def prvni_odstavec(html):
    soup = BeautifulSoup(html, "html.parser")
    znacka = soup.find("p")
    if znacka is None:
        return None
    return znacka.get_text(strip=True)


def prvni_odkaz(html):
    soup = BeautifulSoup(html, "html.parser")
    odkaz = soup.find("a")
    if odkaz is None:
        return None
    return odkaz.get_text(strip=True), odkaz.get("href")


def text_s_id(html, id_):
    soup = BeautifulSoup(html, "html.parser")
    znacka = soup.find(id=id_)
    if znacka is None:
        return None
    return znacka.get_text(strip=True)


def text_s_tridou(html, trida):
    soup = BeautifulSoup(html, "html.parser")
    znacka = soup.find(class_=trida)
    if znacka is None:
        return None
    return znacka.get_text(strip=True)
