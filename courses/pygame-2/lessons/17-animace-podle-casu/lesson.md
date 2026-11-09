## Obrázky se střídají podle času

Robot může stát, běžet nebo blikat. Animace je posloupnost snímků a pravidlo, jak dlouho každý trvá. Měnit index při každém průchodu smyčkou by vedlo k jiné rychlosti na různých počítačích. Proto počítáme herní sekundy stejně jako u pohybu v předchozích hrách.

Tři ukázky porovnávají běžný průběh, dlouhý krok a restart. Náhled ukazuje několik zaznamenaných fází vedle sebe; samotný PNG se nepohybuje. Pracujeme se skutečnými Surface bez otevření okna, stejná součást potom poslouží živé hře. Prostředí z lekce 16 zůstává stejné, zvuk není potřeba.

## Celé kroky i zbylý čas

Při trvání snímku 0,25 s znamená krok 0,625 s dvě změny a zbytek 0,125 s. Jediné if by dohnalo jen jednu změnu; nastavení zbytku na nulu by animaci postupně zpomalovalo. Po celém oběhu index získáme zbytkem po dělení počtem snímků, tedy modulo.

```python
import math
cas = 0.3
trvani = 0.1
kroky = math.floor(cas / trvani + 1e-9)
zbytek = max(0, cas - kroky * trvani)
print('Celé kroky:', kroky, 'zbytek:', round(zbytek, 9))
```

Výsledek jsou tři kroky a nulový zbytek. Číslo 0,1 nemá v binárním float přesný zápis. Malá tolerance u podílu jen opravuje hranici intervalu, není to další viditelná doba snímku. Výsledný zbytek nedovolíme pod nulu. Výklad předpokládá trvání nejméně 0,001 s a konečné nezáporné dt.

## Smyčka, jednorázový efekt a pás obrázků

Chůze obíhá, výbuch či rozsvícení se přehraje jednou. Poslední obrázek jednorázové animace má také plné trvání. Tři snímky po 0,1 s proto končí až v 0,3 s, ne už při vstupu na index 2 v 0,2 s. Potom obraz zůstane a příznak hotovo dovolí hře například efekt odstranit.

Pás snímků (spritesheet) skládá více obrázků vedle sebe. Subsurface nabízí výřez stejné paměti; copy z něj vytvoří nezávislý snímek. Předem ověříme, že šířka pásu je dělitelná šířkou snímku, neodřízneme potichu poslední kousek.

## Objekt a jeho režim nejsou samotná animace

AnimovanySprite používá animátor jako součást. Při nové podobě musí přestavět rect, protože další snímek může být větší; zachová aktuální střed objektu, který se mohl mezitím posunout. To je kompozice, není třeba dědit Animace a Sprite současně.

StavoveAnimace vybírá pojmenovanou animaci, například klid či beh. Znovuzvolení stejného stavu ji nesmí pořád vracet na první obrázek. Při změně na jiný stav ale výslovně začneme od nuly. V úkolech 4/5 poskytuje animator.py ověřenou Animace z Úkolu 1, takže se soustředíte na propojení.

## Váš úkol: Animace ve smyčce

Vytvořte `Animace(snimky, trvani)` s vlastními kopiemi Surface v `snimky`, s `trvani`, `index=0` a `zbytek=0.0`. Vstup je neprázdný seznam; trvani je konečný počet sekund nejméně 0,001. Prázdný seznam a nekladné trvani odmítněte ValueError. `obraz()` vrací uložený aktivní Surface. `restart()` vynuluje index i zbytek.

`update(dt)` přičte konečný nezáporný čas do zbytku, spočítá všechny celé intervaly, posune index modulo počet snímků a ponechá nevyužitý čas. Zlomky nezahazujte a nespoléhejte na jediné if. Na hranici snímku tolerujte drobnou chybu float; vzor přidává 1e-9 k podílu před floor a zbytek omezuje nejméně na nulu. Jiné stejně přesné řešení je možné. Obraz se čte pro kreslení; při jeho úpravě si vytvořte kopii.

Další čtyři zadání přepnete tlačítky Úkol 2–5. U každého najdete vlastní možné řešení; jeho odkrytí nemění rozepsaný kód ani splnění.
