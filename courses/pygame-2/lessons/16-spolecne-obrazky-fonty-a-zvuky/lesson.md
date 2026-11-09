## Zdroj načteme jednou, objektům dáme správná data

Když má hra sto robotů, nemusí stokrát číst stejný obrázek z disku. Banka prostředků si načtený vzor zapamatuje v cache. To je slovník již připravených výsledků: první požadavek zdroj vytvoří, další jej využijí. Nejde o trvalé uložení na disk, cache žije s danou instancí v paměti.

Lekce 16–20 jsou laboratoř samostatných součástí. Každá má **tři ukázky a pět úkolů**, všechny s možným řešením. Ukázky a úkoly skončí obrázkem soucasti.png; porovnáte v něm skutečné Surface, masky a stavy. PNG není animované herní okno. V závěru 20/5 je navíc volitelná živá ukázka režimů.

## Stejné prostředí, vlastní podklady

Použijte projektovou .venv s pygame-ce: `python tools/setup_env.py --courses pygame-2`. Ve VS Code, VSCodium i PyCharm vyberte stejný interpreter. Ověřeno Python 3.14.8/pygame-ce 2.5.8; další balíčky nepřibývají. Základní pokusy nepotřebují displej ani zvukové zařízení. Podklady.py kreslí vlastní obrázky a vytváří krátký tón přes standardní wave/struct. Funkce priprav_media vytvoří vedle pomocného souboru složku media s vlastními BMP a WAV, existující soubory nepřepisuje. Path vychází z __file__, takže umístění nezávisí na právě zvoleném adresáři terminálu.

Spustit ukázku zobrazí PNG ke stažení. V místním editoru zůstane ve pracovní složce. Pomocné soubory musí být vedle uloženého reseni.py; aplikace je při uložení do workspace přiloží podle vybraného úkolu. Při přepínání úkolů se mění i dostupné podklady, například zdroje.py u Úkolu 5.

## Kopie obrázku a sdílení fontu

Pouhé `b = a` nedělá nový obrázek. Obě proměnné pak odkazují na tentýž Surface. Kopie přes copy chrání cache i další objekty, když si jeden obrázek obarvíte nebo upravíte. Naopak font stejné velikosti můžeme vědomě sdílet, pokud po získání neměníme jeho nastavení. Změny velikosti obrázku cachujeme pod dvojicí rozměrů a vždy vycházíme z původního obrazu.

```python
import pygame
a = pygame.Surface((3, 2))
a.fill((80, 180, 255))
b = a.copy()
b.fill((230, 110, 90))
print('Zdroj:', tuple(a.get_at((0, 0)))[:3])
print('Kopie:', tuple(b.get_at((0, 0)))[:3])
```

Zdroj zůstane modrý (80,180,255), kopie bude oranžová (230,110,90). Surface není soubor: pygame.image.load převede soubor na objekt v paměti, copy pracuje s tímto objektem. Convert_alpha může po otevření displeje optimalizovat formát pro kreslení; v pokusech bez displeje jej záměrně nepotřebujeme.

## Zvuk nesmí být povinnou podmínkou

Mixer je zvuková část pygame. Její inicializace otevírá zařízení, neprovádíme ji při importu modelů. Běžné ukázky zvuk nevydávají. Pro místní volitelnou zkoušku spusťte `python prehraj_ton.py --play` z uložené pracovní složky. Přehraje krátký vlastní tón při nízké hlasitosti. Bez --play jen vypíše návod. Zkouška zařízení běží v samostatném procesu s limitem pěti sekund, aby nereagující ovladač nezastavil práci.

Sound.play vrací kanál nebo None, když žádný není volný. Ani přijatý kanál není důkaz slyšitelnosti: záleží na zařízení, hlasitosti a zvoleném výstupu. Pygame.error znamená problém knihovny či zařízení a zde nabídneme tichý režim. Výjimky programových chyb nezakrýváme širokým except. Automatická zkouška s ovladačem dummy ověřuje dekódování a ovládání mixeru, nikoli fyzický zvuk.

## Váš úkol: Banka obrázků s vlastními kopiemi

Vytvořte `BankaObrazu(nacti)` s metodou `obraz(jmeno)`. `nacti` je předaná funkce, která dostane neprázdné textové jméno a vrátí Surface. Pro jedno jméno ji zavolejte jen při prvním úspěšném načtení v dané bance. Načtený obrázek si uložte jako vlastní kopii a při každém požadavku vraťte další vlastní kopii. Úprava zdroje ani jednoho výsledku tak nepoškodí další požadavky. Dvě banky mají oddělenou cache. Chybu načítání neukrývejte a neukládejte neúspěšný výsledek.

Slovník mapuje jméno na načtený vzor. `Surface.copy()` kopíruje pixely, pouhé přiřazení by sdílelo stejný objekt. Zachovejte připravený blok __main__, který výsledek vykreslí.

Další čtyři zadání přepnete tlačítky Úkol 2–5. U každého najdete vlastní možné řešení; jeho odkrytí nemění rozepsaný kód ani splnění.
