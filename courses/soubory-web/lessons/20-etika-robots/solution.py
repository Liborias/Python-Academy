import time
import requests
from urllib.robotparser import RobotFileParser


def smi_stahovat(adresa, cesta, agent="dilna"):
    odpoved = requests.get(adresa + "/robots.txt", timeout=3)
    if odpoved.status_code == 404:
        return True
    pravidla = RobotFileParser()
    pravidla.parse(odpoved.text.splitlines())
    return pravidla.can_fetch(agent, adresa + cesta)


def stahni_jako(url, agent):
    odpoved = requests.get(url, headers={"User-Agent": agent}, timeout=3)
    return odpoved.text


def stahni_slusne(urls, pauza=1.0):
    texty = []
    for cislo, url in enumerate(urls):
        if cislo > 0:
            time.sleep(pauza)
        texty.append(requests.get(url, timeout=3).text)
    return texty
