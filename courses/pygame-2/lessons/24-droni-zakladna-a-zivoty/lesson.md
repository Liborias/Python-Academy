## Přístav pomáhá, ale nechrání navždy

Štít má 2,5 herní sekundy. Uvnitř přístavu se spotřebovává, mimo něj se obnovuje rychlostí 0,5 sekundy ochrany za sekundu. Chráněn je pouze celý obrázek hráče uvnitř zóny. Prázdný štít nepomůže ani uprostřed přístavu.

Drony při kontaktu nezmizí. Dávka současných kontaktů ubere nejvýše jeden ze tří životů a zapne 0,9 s nezranitelnosti. Ta chrání také mimo zónu a je oddělená od energie štítu.

```python
energie = 2.5
energie = max(0, energie - 1.0)
print('Po sekundě uvnitř:', energie)
energie = min(2.5, energie + 2 * 0.5)
print('Po dvou sekundách mimo:', energie)
```

Výsledky jsou 1,5 a 2,5 s. Obnova energie nedoplňuje životy. Kapacita je strop, ne nový plný štít každým snímkem.

## Váš úkol: StitZakladny

StitZakladny(kapacita=2.5, obnova=0.5) uloží kapacita, obnova a energie=kapacita; parametry jsou konečné nezáporné. update(dt,uvnitr) uvnitř vrátí True pouze při původní energii větší než nula a alespoň dt, potom energii odečte a omezí na nulu. Zbývá-li méně než celý krok, považujeme jej za nechráněný. Mimo zónu dobije podle obnova do kapacity a vrátí False. Při dt=0 prázdný štít stále nechrání.

## Váš úkol: Kolo(seed=23)

Dědí Svet a inicializuje jej. Odstraní tréninkové drony ze všech členství, vytvoří Vlny(seed) a drony nastaví na **tutéž Group**. Má kopii ZONA, stit=StitZakladny(), chraneno=False, zivoty=3, nezranitelnost=0.0, zbyva=10.0, konec=False a duvod=''. Hráč/data/skóre/čas zůstávají od rodiče.

update(smer,dt) po konci nic nemění. Pro herní 0 ≤ dt ≤ 0,05 s dodržte pořadí:

1. Přičtěte cas, posuňte hráče a nastavte chraneno ze stit.update(dt, zona.contains(hrac.rect)).
2. Odečtěte nezranitelnost nejméně na nulu. Aktualizujte vlny a posuňte drony.
3. Kruhový kontakt používá kreslené středy a součet radius, přesný dotyk platí. Při zásahu bez štítu a bez nezranitelnosti uberte jeden život a nastavte 0,9 s ochrany. Drony nemažte.
4. Při nule životů ihned skončete s duvod='zivoty'; smrtelný zásah už nesbírá data. Jinak zavolejte seber_data.
5. Odečtěte zbyva, omezte na nulu a zbytek menší než 1e-9 s považujte za nulu. Na konci vlny 1/2 zavolejte vlny.zahaj a nastavte 10 s. Přebytek kroku do nové vlny nepřenášíme. Životy, štít, data a skóre se neobnovují.
6. Po třetí vlně skončete: skore≥6 znamená duvod='uspech', jinak 'data'. Konec zmrazí celý model i náhodu.

Smyčka převádí tick(60) z ms na sekundy a omezuje dt na 0,05. Dlouhou prodlevu nezapočítá celou, jde o herní čas. Pravidla už tvoří celou misi, nový pokus zatím spustíte zavřením a dalším během. Příště přidáme pauzu a restart přímo v okně.
