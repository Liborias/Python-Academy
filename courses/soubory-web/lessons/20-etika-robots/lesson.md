## Robot není člověk

Program dokáže za sekundu stáhnout stovky stránek, a to může cizí web zpomalit nebo shodit. Proto platí několik pravidel dobrého chování.

## Pravidla

1. **Nejdřív zkuste oficiální cestu.** Mnoho služeb nabízí **API** (oficiální rozhraní, kterým se programy ptají na data a dostávají je v čisté podobě, nejčastěji JSON) nebo hotová data ke stažení, a to je lepší než vytahovat údaje z HTML stránek (tomu se říká **scraping**).
2. **Řiďte se `robots.txt`.** Je to soubor na adrese `/robots.txt`, kde provozovatel píše, co roboti smějí a nesmějí. Dodržovat ho není vždy zákonná povinnost, ale je to běžná slušnost, kterou weby očekávají; roboty, které ji porušují, často blokují.
3. **Dělejte pauzy.** Mezi dotazy počkejte aspoň sekundu (`time.sleep`) a stránky nestahujte víckrát, než je třeba.
4. **Představte se.** Hlavička `User-Agent` říká, kdo se ptá. Pošlete vlastní jméno programu a kontakt na učitele nebo školu, např. `Skola-Python/1.0 (ucitel@skola.example)`; **nikdy ne vlastní e-mail**. Provozovatel vás pak může požádat o ukončení, místo aby vás zablokoval.
5. **Čtěte podmínky.** Texty, fotografie i databáze jsou chráněné autorským právem a některé weby scraping zakazují.
6. **Osobní údaje.** Jména, e-maily a fotografie lidí jsou chráněné zákonem (GDPR). Neukládejte je bez důvodu.

## robots.txt v Pythonu

```
User-agent: *
Disallow: /soukrome/

User-agent: zlybot
Disallow: /
```

V souboru je pro každého robota (`User-agent`, hvězdička je „kdokoli“) seznam zakázaných cest. Čte ho `urllib.robotparser` ze standardní knihovny:

```python
from urllib.robotparser import RobotFileParser

pravidla = RobotFileParser()
pravidla.parse(text.splitlines())            # text robots.txt rozdělený na řádky
pravidla.can_fetch("dilna", "http://127.0.0.1:8000/soukrome/tajne.html")   # False
```

Když `robots.txt` neexistuje (404), je dovoleno vše.

## Vlastní hlavičky

Hlavičky se posílají parametrem `headers`: `requests.get(url, headers={"User-Agent": "Skola-Python/1.0"})`. Server `/_hlavicky` vám vrátí v JSON, co přesně dostal.