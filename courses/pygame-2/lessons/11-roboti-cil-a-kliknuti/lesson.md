## Roboti utekli z dílny

V Meteoritech rozhodovaly šipky a srážky objektů. Ve hře **Chyť robota** rozhoduje místo kliknutí: do třiceti herních sekund se pokusíte pochytat co nejvíce robotů. Modří hlídači se odrážejí od stěn, fialoví kývači mají jiný pohyb a vyšší hodnotu. Minutí stojí život. Nejde o střílení; roboty vracíme do dílny.

Lekce 11–15 jsou jeden návazný projekt. Každý krok má jednu ukázku, zadání, kontrolu a možné řešení. Ověřené části předchozích kroků se přikládají jako predchozi.py, takže můžete pokračovat, i když své starší řešení ještě upravujete. Další nesouvisející varianty projektu nepřepínáme.

## Prostředí a spuštění

Použijte stejnou .venv jako pro Meteority. `python tools/setup_env.py --courses pygame-2` připraví pygame-ce; v programu píšeme `import pygame`. Ve VS Code, VSCodium i PyCharm vyberte tentýž Python z projektové .venv. Ověřeno Python 3.14.8/pygame-ce 2.5.8, žádné nové balíčky, zvukové soubory ani síťová data nepřibývají.

Spustit ukázku otevře **samostatné okno 720×520 na počítači s Pythonem**. K hraní je potřeba místní grafická plocha a myš; okno ze vzdáleného serveru se nepřenáší do webové stránky. Klikněte levým tlačítkem do robota. Esc nebo zavření okna ukončí běh a uloží roboti.png. Aplikace poslední snímek zobrazí a nabídne ke stažení, v editoru zůstane v pracovní složce. Tlačítko Stop ukončí proces přímo a uložení PNG nezaručuje.

Podklady.py kreslí naše vlastní roboty. Herni_okno.py řeší zobrazení a jedinou smyčku; sestava.py dočasně dodává části, které sami napíšeme později. Souborům z files pomůže aplikace do stejné pracovní složky jako reseni.py. Při ručním kopírování do jiného projektu vezměte i je. Import modelu nesmí otevřít okno; to dělá až připravený blok __main__.

## Událost uchovává místo kliknutí

MOUSEBUTTONDOWN znamená stisk tlačítka myši, button=1 levé tlačítko a pos souřadnice právě tohoto stisku v okně. MOUSEBUTTONUP je jiná událost. Pozdější pygame.mouse.get_pos může už vracet jiné místo, proto z něj zásah nepočítáme. Pro pouhé kreslení zaměřovače je aktuální pozice v pořádku. Souřadnice z webové stránky do nativního herního okna nepřenášejte.

## Kruh a jeho průhledné rohy

Obrázek je čtvercový, viditelný cíl je kruh. Rect.collidepoint by přijal i některé průhledné rohy. Porovnáme proto druhou mocninu vzdálenosti od viditelného středu s radius²:

```python
import pygame
stred = pygame.Vector2(100, 100)
for bod in ((122, 100), (121, 121)):
    rozdil = pygame.Vector2(bod) - stred
    print(bod, rozdil.length_squared() <= 22 ** 2)
```

První výsledek je True (přesná hrana se počítá), druhý False (roh). Length_squared nepočítá odmocninu a zde dává stejné rozhodnutí. Osa x roste doprava, y dolů. Záporné souřadnice nejsou zvláštní případ; rozhoduje stejná vzdálenost.

## Váš úkol: Robot a najdi_robota

**Robot(stred, polomer=22, body=10)** dědí pygame.sprite.Sprite a inicializuje rodiče. Má třídní barva=(55,205,177), radius=polomer, body, vlastní Vector2 pozice z předaného středu, vlastní image=obraz_robota(polomer,self.barva) a rect se středem zaokrouhleným z pozice. Poloměr je celé číslo nejméně 8, body nezáporné celé číslo, vstupní souřadnice konečné. Vstupy neměňte. Při stejné pozici musí jít o různé nezávislé sprity.

**obsahuje(bod)** vrátí bool pro vzdálenost od **rect.center**, tedy skutečně kresleného středu, nejvýše radius. Nemění bod ani robota. Připravená metoda update(dt,hranice) zatím nedělá nic: stojící robot už ale přijímá stejné argumenty jako budoucí pohyblivé typy.

**najdi_robota(roboty,bod)** vrátí právě jeden původní objekt nebo None. Skupina kreslí v pořadí sprites(); při překrytí vyberte posledního zasaženého, protože je nakreslený navrchu. Proto projděte obrácené pořadí, použijte obsahuje a vraťte první shodu. Žádný sprite zatím nemažte a nepřerovnávejte skupinu. Prázdná skupina vrací None.

Vyzkoušejte střed, kruhovou hranu, průhledný roh a prázdné místo. Připravený obal už umí vybraného robota chytit a ukázat body; samotné účtování napíšete v lekci 13. Po pochytání tří robotů okno dál přijímá zavření, další pokus zatím spustíte novým během.
