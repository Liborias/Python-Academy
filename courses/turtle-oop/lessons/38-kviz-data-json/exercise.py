import json
from html import unescape
from pathlib import Path
from kviz_model import Otazka


def preved_otazky(data):
    # Ověřte celou odpověď a převeďte všechny otázky na objekty.
    pass


def nacti_soubor(cesta):
    # Čtěte UTF-8, dekódujte JSON a použijte preved_otazky.
    pass


if __name__ == "__main__":
    otazky = nacti_soubor("otazky.json")
    print("Počet otázek:", len(otazky))
    print("První:", otazky[0].text)
    print("Správná odpověď:", otazky[0].spravne)
