# Kód odděluje pravidla kvízu od vstupu a zdroje otázek.
# Připravené soubory se automaticky kopírují vedle programu.
import json
from html import unescape
from pathlib import Path
from kviz_model import Otazka


def preved_otazky(data):
    if not isinstance(data, dict) or type(data.get("response_code")) is not int or data["response_code"] != 0:
        raise ValueError("Zdroj nevrátil úspěšný výsledek")
    zaznamy = data.get("results")
    if not isinstance(zaznamy, list) or not zaznamy:
        raise ValueError("Chybí neprázdný seznam otázek")
    otazky = []
    for zaznam in zaznamy:
        if not isinstance(zaznam, dict) or zaznam.get("type") != "boolean":
            raise ValueError("Očekávám otázku pravda/nepravda")
        text = zaznam.get("question")
        odpoved = zaznam.get("correct_answer")
        if not isinstance(text, str) or odpoved not in ("True", "False"):
            raise ValueError("Neplatný text nebo odpověď")
        text = unescape(text).strip()
        if not text:
            raise ValueError("Prázdný text otázky")
        otazky.append(Otazka(text, odpoved == "True"))
    return otazky


def nacti_soubor(cesta):
    text = Path(cesta).read_text(encoding="utf-8")
    return preved_otazky(json.loads(text))


if __name__ == "__main__":
    otazky = nacti_soubor("otazky.json")
    print("Počet otázek:", len(otazky))
    print("První:", otazky[0].text)
    print("Správná odpověď:", otazky[0].spravne)
