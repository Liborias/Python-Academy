## Hotová hra potřebuje konec i nový začátek

Máme svět Kolo, který umí pohyb, meteority, životy, body a štít. Obalíme jej třídou Hra: ta řídí životní cyklus aplikace. Rozlišujeme konec kola (hráči došly životy) a ukončení okna (program už nemá běžet). Při konci kola dál přijímáme klávesy, aby šel spustit nový let.

Predchozi.py obsahuje přesné ověřené části 6–9, včetně Kolo. Herni_okno.py nechává zpracování vstupu a rozhodnutí o aktualizaci na vaší třídě. Hra nevytváří vlastní druhé okno ani druhou souběžnou smyčku.

## Nové kolo není několik vynulovaných čísel

```python
from predchozi import Kolo
prvni = Kolo(seed=7)
druhe = Kolo(seed=7)
print('Stejný svět:', prvni is druhe)
print('Stejná skupina:', prvni.proud.objekty is druhe.proud.objekty)
print('Počáteční skóre:', prvni.skore, druhe.skore)
```

Svět ani skupina nejsou stejné, obě skóre začínají nulou. Přesně takový nový model chceme při restartu: nestačí obnovit životy a ponechat na ploše staré kameny, časovače či štít. Starý model přitom nemusíme vyprazdňovat — jiná proměnná na něj může dál odkazovat pro porovnání.

## Váš úkol: Hra(seed=7)

Uložte seed, nové Kolo(seed), bezi=True, pauza=False a restart_povolen=True. Poslední atribut umožní společnému zobrazení nabídnout skutečně podporované ovládání. Model se při konstrukci ani importu nesmí pokoušet otevřít okno, to patří až do spustit pod __main__.

Metoda **zpracuj(udalost)** nejprve zjistí typ:

- QUIT vždy nastaví bezi=False, i během pauzy nebo po konci kola.
- U KEYDOWN, pokud hra ještě běží, Escape také ukončí program.
- Klávesa R kdykoli za běhu vytvoří **nové Kolo se stejným seed** a zruší pauzu. Funguje při hraní, v pauze i po konci kola; starý svět neměňte.
- P přepne pauzu, pouze pokud aktuální kolo ještě má životy.
- KEYUP a ostatní události či klávesy nic nemění. Po bezi=False už R ani P hru neobnoví.

Metoda **update(smer, dt)** předá aktualizaci do kola právě jednou, jen pokud bezi, není pauza a zivoty>0. Jinak svět zůstane stejný. Při pauze pořád běží vnější smyčka s Clock a event.get, jen model neposune čas. Po zrušení pauzy se proto nedohání celá doba čekání jedním krokem.

## Vyzkoušejte celý let

Šipky ovládají loď, P pozastaví/pokračuje, R začne nový let, Escape nebo zavření okna ukončí program. Zkuste pauzu během pohybu, restart s aktivním štítem, nový let po posledním životu a zavření okna v pauze. Všechna tato rozhodnutí musí používat skutečný stav téže hry.

Při výchozím seed=7 restart zopakuje začátek náhodné posloupnosti. To se hodí pro trénink; změnou parametru Hra(seed=...) zvolíte jiné semeno, s None nový náhodný začátek. Žádná varianta ale nepředstavuje kryptografické losování.

Po běžném ukončení se uloží meteority.png. V prohlížeči nabídne poslední stav, pro hru znovu spusťte program. Možné řešení ukazuje jeden ověřený návrh. Příští modul postaví jinou hru, Chyť robota, s myší a pohybujícími se cíli; toto kolo Meteority už tvoří hotový hratelný celek.
