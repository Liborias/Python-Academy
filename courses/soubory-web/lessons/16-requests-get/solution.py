import requests
from bs4 import BeautifulSoup


def stahni_text(url):
    odpoved = requests.get(url)
    return odpoved.text


def stavovy_kod(url):
    odpoved = requests.get(url)
    return odpoved.status_code


def nacti_json(url):
    odpoved = requests.get(url)
    return odpoved.json()


def nadpis(url):
    odpoved = requests.get(url)
    soup = BeautifulSoup(odpoved.text, "html.parser")
    znacka = soup.find("h1")
    if znacka is None:
        return None
    return znacka.get_text(strip=True)
