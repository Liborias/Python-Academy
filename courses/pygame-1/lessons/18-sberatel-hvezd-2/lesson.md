## Dokončíme hru

Jádro hry už máte z minulé lekce. Dnes je doplníme o to, z čeho se hra opravdu hraje: **životy, zvuky, konec hry a restart**.

Soubor `exercise.py` obsahuje hotovou hru z minulé lekce. Vy ji upravíte. U každé části vám pomůže lekce, kterou jste už prošli:

| Část | Z které lekce |
|---|---|
| zvuk a hudba | 8 |
| stav hry a restart | 16 |

## Nová pravidla

1. **Životy:** hráč začíná se **3 životy**. Když hvězda **spadne pod okno**, hráč jeden život ztratí. Chycená hvězda skóre zvýší, ale život nikdy neubere.
2. **Zvuk:** po chycení hvězdy se přehraje `cinknuti.wav`. Od začátku hraje v nekonečné smyčce hudba `hudba.wav` při hlasitosti **0.3** (hudbu pusťte přes `pygame.mixer.music`, efekt přes `pygame.mixer.Sound`).
3. **Texty:** vlevo nahoře **Skóre: N** a pod ním **Životy: N** (oba bílé, písmo 32, levé horní rohy v bodech `(10, 10)` a `(10, 40)`).
4. **Konec hry:** když životy klesnou na **0**, stav se změní na `"konec"`. Hra se zastaví (nic se nehýbe) a zobrazí se pozadí `(60, 0, 0)`, žlutý text **Konec hry** (písmo 64, střed v bodě `(200, 200)`), bílý text **Skóre: N** (střed `(200, 260)`) a bílý text **Stiskni R** (střed `(200, 310)`).
5. **Restart:** klávesa **R** při konci hry nastaví skóre na 0, životy na 3, stav na `"hra"`, raketu do výchozí polohy a hvězdy na jejich počáteční místa.

Pro vynulování hvězd se hodí cyklus přes indexy: `for i in range(len(hvezdy)): hvezdy[i].topleft = (30 + i * 90, -i * 80)`.

## Rady

- Pracujte po částech a po každé zkoušejte hru: nejdřív životy, pak zvuky, pak konec a restart.
- Pohyb, kolize i kreslení hry patří jen do stavu `"hra"`. Ve stavu `"konec"` se kreslí jen obrazovka konce hry.
- Přehraný zvuk neovlivňuje chod hry. Můžete ho zkusit i bez sluchátek.