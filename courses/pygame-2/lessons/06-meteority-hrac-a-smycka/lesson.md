## Z obrázku bude pohybující se hra

První modul připravil herní objekty bez okna. Teď postavíme Meteority: lodí uhýbáte padajícím kamenům. Lekce 6–10 jsou jeden návazný projekt. Každá přidává konkrétní část a vlastní možné řešení, další nesouvisející varianty nepřepínáme. Ověřené dřívější části budou v dalších lekcích přiložené, takže cizí chyba v minulém kroku nezastaví celé pokračování.

## Prostředí a spuštění

Použijte stejnou .venv a pygame-ce z první kapitoly. `python tools/setup_env.py --courses pygame-2` připraví balíček do projektového prostředí, v kódu se píše import pygame. Vyberte stejný interpreter ve VS Code, VSCodium nebo PyCharm. Ověřená kombinace je Python 3.14.8 a pygame-ce 2.5.8; nepřibyly další balíčky.

**Tato kapitola otevírá skutečné okno.** Vznikne na počítači, kde běží Python/start.py, nikoli uvnitř prohlížeče. Pro hraní potřebujete místní grafickou plochu a klávesnici; zvuk zatím nepoužíváme. Na vzdáleném serveru bez plochy nelze živé okno vidět. Náhledy z minulé kapitoly a kontrola modelů tam ale fungují.

Stiskněte Spustit ukázku a ovládejte loď šipkami. Zavřením jejího okna program skončí a do aplikace se vrátí poslední snímek meteority.png ke stažení. V pracovním editoru zůstane PNG na disku. Tlačítko Stop ukončí proces přímo, proto nemusí snímek uložit. Podklady.py kreslí loď a kameny kódem, Herni_okno.py obsahuje společný vzhled a smyčku, Sestava.py dočasné sestavení tohoto kroku; soubory se přiloží vedle reseni.py. Žádné obrázky ze sítě nepotřebujete.

## Jedna iterace smyčky

Ve společném herni_okno.py se děje stále totéž: Clock.tick(60) omezí frekvenci, event.get přečte události, get_pressed zjistí držené klávesy, model.update změní svět, kreslení připraví plochu a display.flip ji ukáže. Události zpracováváme v každé iteraci. Kreslení a pohyb jsou oddělené, takže lze pravidla modelu ověřit i bez čekání na obrazovku. Set_clip(hranice) omezí kreslení objektů na herní plochu: kameny při příchodu neschovají horní informační pruh. Potom se původní výřez obnoví. Ořez mění viditelné pixely, nikoli polohu objektu nebo pravidlo kolize.

Tick vrací milisekundy. Dělení 1000 převede výsledek na sekundy. Smyčka omezuje dt nejvýše na 0,05 s, aby návrat po dlouhém přepnutí aplikace neudělal velký skok. Při takové prodlevě vědomě nezapočítá celou reálnou dobu; nejde o přesnou fyzikální simulaci. V běžném plynulém běhu se čas počítá podle skutečné délky snímku.

```python
import pygame
smer = pygame.Vector2(1, -1).normalize()
dt = 16 / 1000
posun = smer * 240 * dt
print('Délka posunu:', round(posun.length(), 2))
```

Délka je 3,84 pixelu, stejně jako pro vodorovný pohyb rychlostí 240 px/s. Vektor (1, −1) bez normalizace by měl větší délku a diagonála by byla rychlejší. Desetinnou pozici uchováme, rect se jen zaokrouhlí pro kreslení.

## Váš úkol: Hrac a precti_smer

Třída **Hrac(stred, hranice)** dědí pygame.sprite.Sprite a inicializuje rodiče. Použije dodanou funkci obraz_lodi() pro vlastní image 40 × 32, vytvoří vlastní rect se středem zaokrouhleným z předané pozice a nastaví radius=14. Do pozice uloží kopii Vector2, do hranice kopii Rect a do rychlost počátečních 240 px/s. Předaný střed je uvnitř dostatečně velkých hranic; může být desetinný. Rychlost lze později změnit na jiné nezáporné číslo.

**update(smer, dt)** zkopíruje směr, nenulový normalizuje a přičte rychlost × dt k pozici. Celý obrázek musí zůstat uvnitř hranic: x omezte na left + polovina šířky až right − polovina šířky, y obdobně. Omezujte přesnou pozici, ne jen rect, a pak nastavte rect.center přes round. Nulový směr a dt=0 jsou platné; dt je nezáporný konečný počet sekund. Vstupní vektory/Rect ani jiné hráče neměňte.

**precti_smer(klavesy)** dostane stav s přístupem klavesy[kód]. Vrátí Vector2: x = pravá − levá, y = dolní − horní šipka. Protější šipky se ruší. Get_pressed neposkytuje obyčejný slovník, proto používejte hranaté závorky, ne metodu get. Normalizace patří až do update, tato funkce jen přečte vstup.

Blok `if __name__ == "__main__"` spustí připravené okno; při importu se nesmí otevřít. Sestava dostává vaši třídu a čte její skutečný stav, nepohybuje jinou ukázkovou lodí. Nejprve zkuste jednu šipku, dvě současně a kraj plochy. Pak porovnejte své řešení s nabízeným vzorem.
