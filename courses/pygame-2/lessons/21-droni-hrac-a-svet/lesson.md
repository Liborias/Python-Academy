## Datový kurýr v hlídaném poli

Sesbíráte alespoň šest zelených datových bodů a přežijete tři desetisekundové vlny dronů. Modrý kurýr je rychlejší, soupeři však přibývají. Přístav poskytne krátkou ochranu, která se obnovuje mimo něj. Samotné čekání misi nesplní: ochrana je omezená a potřebujeme také data.

Lekce 21–25 jsou **jeden návazný projekt** s úkolem, kontrolou a možným řešením každého kroku. Nesouvisející varianty nepřepínáme. Ověřené předchozí části budou v predchozi.py; cizí chyba v minulém kroku vás nezastaví. Dnes připravíme svět a sběr dat, příště pohyb soupeřů a od kroku 24 životy.

## Prostředí a spuštění

Použijte stejnou .venv s pygame-ce. `python tools/setup_env.py --courses pygame-2` připraví závislost, v programu píšeme import pygame. Ve VS Code, VSCodium i PyCharm vyberte tentýž interpreter. Ověřeno Python 3.14.8/pygame-ce 2.5.8, žádné další balíčky ani zvuk nejsou potřeba.

Spustit ukázku otevře **samostatné okno 720×540 na počítači s Pythonem**. Ovládají je šipky nebo WASD, Esc/křížek ukončí běh. Potřebujete místní grafickou plochu a klávesnici, okno ze vzdáleného serveru se nepřenáší do prohlížeče. Běžné zavření uloží droni.png pro náhled/stažení; v editoru zůstane v pracovní složce. Stop ukončuje proces přímo a uložení nezaručuje.

Podklady.py kreslí vlastní grafiku. Zdroje.py obsahuje BankaObrazu/BankaFontu z lekce 16: obrázkové vzory chráníme kopiemi a fonty sdílíme. Herni_okno.py dodává jedinou smyčku, sestava.py obal rozpracovaných kroků. Pomocné soubory musí být vedle reseni.py, kam je aplikace při uložení přiloží. Import modelu neotevírá okno ani mixer. Smyčka používá tick(60), převede milisekundy na sekundy a dt omezí na 0,05 s. Dlouhou prodlevu vědomě nezapočítá celou; jde o herní čas.

```python
import pygame
smer = pygame.Vector2(3, 4).normalize()
posun = smer * 240 * 0.05
print('Posun:', tuple(round(p, 2) for p in posun))
print('Délka:', round(posun.length(), 2))
```

Posun je (7,2; 9,6) pixelu, délka 12. Normalizace nastaví délku směru na 1 a nezrychlí diagonálu. Nulový směr nenormalizujeme. Vector2 zachová desetinnou polohu, rect dostane zaokrouhlený střed pro kreslení a zásahy.

## Váš úkol: Hrac a Dron

**Hrac(stred, hranice)** dědí Sprite a inicializuje rodiče. Má vlastní image z `OBRAZY.obraz('hrac')` (32×32), radius=14, vlastní Vector2 pozice, kopii Rect hranice, rychlost=240 a rect vystředěný přes round(pozice.x/y). Střed je uvnitř dost velkých hranic. update(smer,dt) zkopíruje a normalizuje nenulový směr, přičte rychlost×dt, omezí přesnou polohu na hranice s odstupem **16 px pro celý obrázek** a aktualizuje rect. Rychlost je nezáporná, dt konečné nezáporné sekundy. Vstupy neměňte.

**Dron(stred, rychlost=95)** je Sprite s třídním vzhled='dron'. Použije `OBRAZY.obraz(self.vzhled)` (28×28), radius=12, vlastní Vector2 pozice, předanou rychlost a zaokrouhlený rect. **cil(hrac)** vrátí novou kopii hrac.pozice; zatím určuje cíl, ne posun. Instance nesmějí sdílet měnitelnou polohu ani image.

## Váš úkol: Svet

Svet() vlastní kopii HRANICE, hráče v (360,300), Group se třemi Dron v (110,140), (610,140), (610,430), data=DatovyBod(DATOVE_BODY[0]), skore=0 a cas=0.0.

seber_data() porovná kreslené středy: vzdálenost nejvýše součet radius je sběr. Starý bod odstraní přes kill, zvýší skore, vytvoří nový DatovyBod na `DATOVE_BODY[skore % len(DATOVE_BODY)]` a vrátí True. Bez sběru vrátí False a nic nemění. Posloupnost pěti míst se opakuje, jedno volání sbírá nejvýše jeden bod. update(smer,dt) přičte čas, posune hráče a zkusí sběr. Drony dnes stojí a kontakty neubírají životy. Dvě instance světa jsou nezávislé.
