import time
import requests


def stahni_bezpecne(url, timeout=2):
    try:
        odpoved = requests.get(url, timeout=timeout)
        odpoved.raise_for_status()
    except requests.RequestException:
        return None
    return odpoved.text


def stahni_s_opakovanim(url, pokusy=3, pauza=0.1):
    for cislo in range(pokusy):
        text = stahni_bezpecne(url)
        if text is not None:
            return text
        if cislo < pokusy - 1:
            time.sleep(pauza)
    return None
