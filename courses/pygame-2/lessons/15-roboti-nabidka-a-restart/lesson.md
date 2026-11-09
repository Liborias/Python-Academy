## Celá hra má nabídku i výsledek

Máme hotové Kolo s vlastním časem a pravidly. Teď vytvoříme **Hra**, která řídí čtyři stavy: nabidka, hra, pauza a vysledek. Bezi říká něco jiného: zda má ještě běžet celé okno. Po konci kola tedy bezi zůstane True a lze číst klávesy pro nový lov.

Predchozi.py obsahuje ověřené modely 11–14. Herni_okno.py jen zobrazuje aktuální stav a volá update/zpracuj. Nevytvářejte druhé okno ani druhou smyčku. Atribut nabidka_povolena=True připravenému zobrazení oznámí, že už podporujete nabídku a nové ovládání.

## Přehled přechodů

- Nabídka + Mezerník: nové Kolo a hraní.
- Hraní + levé tlačítko: pravidla Kolo.klik.
- Hraní + P: pauza. Pauza + P: pokračování stejného kola.
- Hraní, pauza či výsledek + R: nové Kolo a hraní.
- Výsledek + Mezerník: návrat do nabídky, kolo=None.
- Libovolný stav + Esc nebo QUIT: ukončení okna.

P v nabídce či výsledku nic nedělá. R v nabídce také nic nedělá, start je výslovně Mezerník. Uvolnění klávesy není nový stisk. Po bezi=False už žádný vstup ani update nesmí hru obnovit. Výjimkou je opakované QUIT, které dál jen ponechá bezi=False.

## Nový svět, zachovaný starý výsledek

```python
from predchozi import Kolo
prvni = Kolo(seed=11)
druhe = Kolo(seed=11)
print('Stejné kolo:', prvni is druhe)
print('Stejná skupina:', prvni.lov.roboty is druhe.lov.roboty)
print('Počáteční vlny:', prvni.cislo, druhe.cislo)
```

Objekty i skupiny jsou různé, obě čísla vln jsou 1. Při restartu nedoplňujeme životy do starého světa a nevyprazdňujeme staré skupiny. Vytvoříme nový Kolo(self.seed); ostatní proměnné mohou stále odkazovat na starý výsledek bez změn. Stejný seed při novém lovu zopakuje začátek náhodné posloupnosti, None zvolí nový náhodný začátek.

## Váš úkol: Hra(seed=11)

Konstruktor uloží seed, bezi=True, stav='nabidka', kolo=None a nabidka_povolena=True. Samotná nabídka ještě nespouští časovač a nevytváří Kolo.

**novy_lov()** vytvoří nové Kolo(self.seed) a nastaví stav='hra'. Sdílí ji start i restart. Staré kolo neměňte.

**zpracuj(udalost)** vždy přijme QUIT a jinak nejprve ověří, že program stále běží. KEYDOWN zpracuje podle přehledu; nejprve ověřte typ, až pak čtěte key. Ostatní události předává do kolo.klik pouze ve stavu 'hra'. Pokud tím kolo skončilo, ihned přepne na 'vysledek'. V nabídce, pauze a výsledku se kliknutí do hry neúčtuje.

**update(dt)** aktualizuje Kolo právě jednou pouze při bezi=True a stav='hra'. Jakmile kolo.konec, přepne na 'vysledek'. V pauze se nemění čas, polohy, body ani náhoda; vnější Clock a události dál běží, takže při pokračování nedoháníme celou pauzu. Nabídka a výsledek model také neposouvají.

## Vyzkoušejte celý postup

Spusťte ukázku, aktivujte herní okno a stiskněte Mezerník. Chytejte roboty levým tlačítkem. P pozastaví a zase obnoví stejný lov, R začne nový s čistým časem a čítači. Zkuste restart během pauzy, konec po třech minutích, nový lov po výsledku a návrat Mezerníkem do nabídky. Esc nebo křížek funguje ve všech stavech, i v pauze.

Po běžném zavření zůstane roboti.png, který aplikace zobrazí a nabídne ke stažení. Všech pět kroků má možné řešení, odkrytí nepřepisuje rozepsanou práci. Máte druhou samostatnou hratelnou hru Pygame 2; další modul prohloubí společné obrázky, animaci, kolize, kameru a herní režimy.
