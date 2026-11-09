## Zásah, body a přesnost jsou různé údaje

Modrý hlídač má hodnotu 10 bodů, fialový kývač 20. Dva zásahy proto nemusí znamenat stejné skóre. Přesnost vyjadřuje podíl úspěšných kliknutí ze všech započítaných pokusů. Použijeme ji nezávisle na bodové hodnotě robotů.

Predchozi.py přináší obě pohyblivé třídy a kruhový výběr navrchu. Vlastní pravidla tohoto kroku patří do Lov. Herni_okno.py pouze ukáže jeho stav a předá skutečné události; nevede druhé vlastní skóre.

```python
zasahy = 2
pokusy = 3
skore = 10 + 20
print('Body:', skore)
print('Přesnost:', round(100 * zasahy / pokusy, 1), '%')
```

Výsledek je 30 bodů a přibližně 66,7 %. Dělit 30 třemi by nebyla přesnost. Na začátku nejsou žádné pokusy a místo dělení nulou vrátíme 0 %. Zaokrouhlení patří až do zobrazení; model vrací skutečný podíl.

## Jeden stisk se počítá jednou

Přijímáme jen MOUSEBUTTONDOWN s button=1. Uvolnění stejného tlačítka nesmí přidat druhý pokus. Pravé tlačítko, pohyb myši a klávesnice účetnictví nemění. Událost nemusí mít atribut button ani pos, proto nejprve ověřte typ a až pak čtěte další atributy.

Započítaný stisk vždy přidá jeden pokus. Pokud najdi_robota vrátí objekt, odebereme právě jeho, přidáme jeho body a jeden zásah. Při None ubereme jeden život. Při překrytí se chytí jen horní robot, spodní zůstane. Stisk na prázdném místě včetně oblasti mimo hrací plochu je minutí, pokud lov ještě obsahuje cíle. V této hře není zvláštní bezpečná oblast pro klikání do HUD.

## Vlastní skupina a sdílené objekty

Pygame.sprite.Group(roboty) vytvoří vlastní skupinu obsahující stejné objekty. Nekopíruje jejich obrázky ani polohy. Robot.kill odstraní konkrétního robota **ze všech skupin**, ve kterých je členem. Oproti tomu group.remove by odstranilo jen jedno členství. Chycený robot má zmizet všude, ostatní roboti a jejich polohy se nemění.

## Váš úkol: Lov(roboty,zivoty=3)

Do roboty uložte novou pygame.sprite.Group z předaných spritů. Přijměte i původní Group nebo prázdný seznam, objekty zachovejte. Uložte nezáporný celočíselný počet zivoty a počáteční skore=0, pokusy=0, zasahy=0. Instance nesmějí sdílet čítače ani vlastní skupinu.

**klik(udalost)** vrací chyceného robota, jinak None. Nejdřív odfiltruje jiný typ/tlačítko. Pokud už nejsou životy nebo cíle, nedělá nic, ani nezvýší pokusy. Jinak provede přesně popsané účtování, použije udalost.pos a najdi_robota, chycený objekt odstraní přes kill. Životy nemohou klesnout pod nulu. Skóre přičítá skutečné robot.body, nikoli pevnou desítku.

**presnost()** vrátí 100×zasahy/pokusy, při nule pokusů 0.0. Nemění čítače ani nezaokrouhluje výsledek.

Zkuste zásah, minutí, překryté cíle, pravé tlačítko a poslední život. Po pochytání všech tří robotů nebo ztrátě životů připravený obal zobrazí výsledek a dál dovolí okno zavřít. Automatické další vlny přidáme v příštím kroku. Výklad i případné jiné správné řešení mají splnit stejné chování, není povinné kopírovat přesný zápis vzoru.
