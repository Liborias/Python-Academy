## Jeden trvající zásah nesmí spotřebovat všechny životy

Detekce kolize se provádí v každém kroku. Při 60 snímcích za sekundu by naivní odečítání za každý průnik mohlo vyčerpat životy téměř okamžitě. Zdravotní stav proto po přijatém zásahu zapne krátkou nezranitelnost. Kromě toho odstraníme všechny kameny, které právě zasáhly loď.

Predchozi.py už obsahuje hráče, meteorit a proud z řešení 6–7. Herní obraz používá kruhové pravidlo: hráč radius=14, kámen svůj poloměr. Vzdálenost středů nejvýše součet radius je zásah, přesný dotyk kruhů se počítá. Některé průhledné rohy obdélníků se proto za zásah nepovažují.

## Odpočet v sekundách

```python
nezranitelnost = 1.0
for dt in (0.25, 0.5, 0.5):
    nezranitelnost = max(0, nezranitelnost - dt)
    print('Zbývá ochrany:', nezranitelnost)
```

Výsledky jsou 0,75; 0,25; 0 sekund. Max nedovolí záporný zbytek. Odmítaný zásah odpočet znovu nezapíná: jinak by dlouhý kontakt mohl ochranu stále prodlužovat. Jednotlivé odečtení musí být úměrné dt, nikoli vždy jedna sekunda nebo jeden snímek.

## Váš úkol: Zdravi

**Zdravi(pocet=3, ochrana=1.0)** je vlastní třída. Pocet je nezáporný celočíselný počet životů, ochrana kladný konečný počet sekund. Uloží zivoty=pocet, ochrana a nezranitelnost=0.0. Každá instance má vlastní stav.

**tick(dt)** odečte nezáporný čas a omezí nezranitelnost nejméně na nulu. **zasah()** vrátí True právě tehdy, když hráč ještě má život a nezranitelnost je nulová: ubere jeden život a nastaví odpočet na ochrana. Jinak vrátí False a nic nepřepisuje. Životy nikdy neklesnou pod nulu.

## Váš úkol: zpracuj_zasahy

Funkce **zpracuj_zasahy(hrac, proud, zdravi)** najde kruhové zásahy v proud.objekty a všechny zasažené kameny odstraní ze všech skupin přes kill. Pokud našla alespoň jeden, pokusí se přijmout zásah do zdravi. Vrátí bool, zda byl skutečně odečten život. Dávka více současných kamenů má odečíst nejvýše jeden, ostatní i během nezranitelnosti z plochy zmizí. Nezasažené, hráče ani proud.minulo neměňte. Srážka není úspěšné minutí a nedává bod.

Spritecollide s True provede kill a s callbackem pygame.sprite.collide_circle zvolí kruhy. Samotný seznam zásahů ještě neříká, zda lze odečíst život — o tom rozhoduje Zdravi. Oddělení detekce od pravidla dovolí obě části ověřit samostatně.

Společná sestava nejprve odpočítá ochranu, pak vyhodnotí nové zásahy. Oranžový tenký kroužek u lodě značí právě běžící ochranu. Při nule se svět zastaví, ale okno dál zpracovává události a lze jej zavřít. Nové kolo zatím spustíte zavřením a opětovným spuštěním ukázky; vlastní restart přidá lekce 10.
