# Předávací dokument: Dílna Pythonu

## Aktuální v0.73 (11. 11. 2026): Ověření a předání, Pygame 2 dokončen

Na pokyn „pkračuj“ dokončen závěrečný modul 26–30 podle plánu. Kurz má
všech 30 lekcí, stav draft do připomínek studentů, obtížnost 4/4 (úvod 3/4).
Témata 26–29: tři ukázky/pět úkolů, každé zadání vlastní šablona/kontrola/možné
řešení. Závěr 30: jeden návazný projekt s řešením, bez nesouvisejících variant.
Nově 13 ukázek/21 úkolů; celý kurz 58 ukázek/86 úkolů. Globálně 240 hlavních
+ 324 doplňkových řešení = 564, doplňkových ukázek 162. Celkem 255 lekcí včetně 15
průvodců. Starší ID, obsah, klíče postupu a rozepsaná práce se nemění.

Nové ID:
- 26-rizene-herni-scenare
- 27-vlastni-testy-hry
- 28-vysledky-v-json
- 29-priprava-a-baleni-hry
- 30-kuryrska-smena-a-predani

Lekce 26: řízený replay skutečného Kolo z 25, snímek počátku i každého kroku,
rozdělení času, držené vstupy, celá dráha proti vzdálenosti začátku/konce,
nezávislé stopy. Seed opakuje losování pouze ve stejném modelu se stejnými
vstupy a kroky; None není opakovatelný seed. Snimek vytváří hodnotový slovník.

Lekce 27: vlastní unittest pro hráče, štít, zásahy/priority konce, vlny,
pauzu/restart/QUIT, seed/skupiny/hlídače/zmrazení. Sestav_sadu vrací novou
TestSuite. Kontrola přijme správný model a vyžaduje odhalení každé známé vady
přes změněné veřejné chování. Nehodnotí jména metod ani text implementace;
prázdná, přeskočená, vždy úspěšná ani vždy selhávající sada nestačí.
Hlavní blok provede sadu a vrátí její návratový kód, unittest může psát stderr.

Lekce 28: JSON verze přesně int 1, seznam výsledků se jménem 1–24 znaků po strip,
body nezáporný přesný int (bool ne), uspech přesný bool. Čisté kopie, pořadí
úspěch/body sestupně/casefold jméno a stabilní shody, limit. Chybějící/rozbitý
JSON/UTF-8 či verze vrátí [], jiný OSError se předává. Samotné čtení původní
bajty nemění. Zápis přes jedinečný dočasný soubor ve stejném adresáři, zavření
před os.replace a úklid ve finally. Chyba nahrazení zachová starší soubor.
Jednoduché pořadí není úložiště pro souběžné procesy ani české slovníkové řazení.

Lekce 29: kořen podle __file__/sys.executable při frozen, kontrola souborů,
seznamy argumentů se stejným Pythonem pro běh, volitelnou stavbu a unittest.
Funkce pouze připravují hodnoty, neinstalují/nespouštějí/nepíší soubory.
Podklady mají skutečnou hra.py z 25, requirements, testy a NAVOD.md.
Over_projekt.py funguje i při spuštění odjinud díky správnému cwd.
Sestavit.py v 29/4 importuje studentovu prikaz_baleni z reseni.py a staví hra.py;
v 30 hotová cesty.py staví studentovu reseni.py. PyInstaller 6.22.3 volitelný,
--onedir/--console/--clean/--noconfirm a vlastní dist/build/spec. Vysvětlené
příkazy pro .venv, instalaci, testy, spuštění i všechny přepínače balení.
Předává se celá distribuční složka, nová stavba nahrazuje starý výstup:
vlastní výsledky před ní zkopírovat mimo dist. Nekopírovat cizí .venv.

Kurýrská směna 30: HraSPoradim(Hra), vlastní jméno/rychlost (výchozí 260)
a nejlepších pět dokončených pokusů. Zbytek pravidel z 25 beze změny, stejně
Mezerník/šipky/WASD/P/R/Esc. Konstruktor načte, novy_let vytvoří nový svět
a nastaví rychlost, update po rodiči jednou na identitu kola uloží i prohru,
kresli deleguje a přidá profil/stav/tabulku. Chyba čtení/zápisu má zprávu
a nezničí původní tabulku, neopakuje se každý snímek. Různé rychlosti nemají
oddělené pořadí, slouží k vlastnímu experimentu. V nabídce je vidět všech pět
řádků i nejdelší povolené jméno, ověřeno skutečným renderem.

Model_hry.py obsahuje přesné definice z 21–25, stejné banky/cache/zásobník.
Vysledky.py/podklady a cesty.py jsou AST kopie řešení 28/29. Import neotevírá
displej/mixer ani nezapisuje výsledky. Konzolová témata 26–29 nepotřebují plochu,
30 je GUI/preview_images/limit 600 s, droni.png při normálním QUIT.
Pro trvalé výsledky je nutné uložit pracovní složku a v editoru spustit její
reseni.py: data/vysledky.json vedle programu. Webový běh je dočasný, okno patří
hostiteli Pythonu, nepřenáší se ze serveru do webu. Stop nezaručuje PNG.
Stejný Python 3.14.8/pygame-ce 2.5.8, žádné nové povinné knihovny nebo audio.

Osm skupin test_predani_hry prošlo: 50 chybných variant/sad odmítnuto, navíc
chybějící GUI vstup; jiné správné zápisy přijaty. Kontroly skutečného modelu
a disku, řízená chyba os.replace, sady proti vadám, AST návaznost, přesná
řešení, 32 konzolových běhů+úryvek 30, čistá kopie s over_projekt ze cizího cwd
a skutečný SDL vstup/PNG/read-only helpery. Cílený validátor 30 lekcí:
0 chyb/upozornění. Celková unittest sada na Pythonu 3.14.8/Linux:
**354 testů OK bez přeskočených, 1032 s**, včetně celkové validace 255 lekcí.
Starší ResourceWarning z pomocných procesů/souborů nejsou selhání; místní
HTTP/SMTP testovací servery byly povolené. Po sjednocení vstupu hra.py se
společným modelem a odstranění nesouvisejících pomocníků sestavení z 26/27
prošlo znovu všech osm cílených skupin (17 s). Obě varianty balení 29/4 a 30
byly skutečně sestaveny a binárky prošly skriptovaným SDL během/QUIT/PNG.

Chromium e2e_predani_hry prošlo 13 ukázek/21 úkolů, odmítnuté šablony/
přijaté vzory, lazy řešení bez změny práce/postupu, skutečné běhy včetně
unittest a SDL/PNG/stažení, workspace s testy/NAVOD, reload/splnění,
plán/přípravu 30/30 a mobil 380/320. Opraven dlouhý prostý text události v 27/4
pro úzký mobil. Prošly e2e_droni a e2e_solutions (200 ostatních lekcí);
druhý test nyní čeká na titul právě požadované lekce, ne na zbylý editor
předchozí stránky při přepnutí hash routy. Serverové API/JS/CSS beze změny.

PyInstaller 6.22.3 skutečně sestavil onedir na Linuxu/Pythonu 3.14.8 pro 29/4 i 30.
Binárka 30 běžela s reálným SDL offscreen, fonty, Clock a PNG. Testovací C helper
LD_PRELOAD pouze přidává SDL klávesy/QUIT, nemění model, čas, render ani disk;
krátký běh/pauza/restart/normální zavření, celá čekající mise do prohry,
jediný zápis a znovunačtení ve druhém procesu prošly. Finální render doplněn
o všech pět řádků pořadí; binárka znovu sestavena a zkoušena s plnou tabulkou.
Fyzická klávesnice, Windows/macOS a instalace příjemce tím nejsou ověřeny.
Xvfb/xdotool ani sudo zde nejsou; nic se neinstalovalo, použito SDL offscreen.
Snímky menu/plné tabulky/pauzy i mobilních řešení/PNG prohlédnuté.
Logy a snímky mimo repo v /workspace/scratch/pygame2-finish-work.

Aktualizované katalog/kurz/plán 30/30, příprava všech editorů, dokumentace
a počty v testech. Dodávka commit/push do main bez ZIPů a bez publikace
cloudového prostředí. Na další pokyn lze zahájit další plánovaný kurz
**Databáze a projekty**, první blok SQLite: prostředí/databáze, tabulka,
parametrizované dotazy, čtení a transakce. Základ využít sqlite3 ze standardní
knihovny, více ukázek/úkolů s možnými řešeními u samostatných témat;
navazující projekty ponechat souvislé. Historické zápisy nejsou nové zadání.

## Aktuální v0.72 (11. 11. 2026): Hon na dronech 21–25

Na pokyn „pokračuj“ dokončen m05 Pygame 2 jako jeden souvislý projekt:
21 hráč/svět/data, 22 pronásledování/hlídači/rozestupy, 23 řízené vlny,
24 životy/štít přístavu/konec mise, 25 nabídka/let/pauza/výsledek/restart.
Každý krok má jednu ukázku, úkol se šablonou/kontrolou/možným řešením a tři
kvízové otázky; bez nesouvisejících variant navazující hry. Kurz draft,
dostupných 25/30, celkem 45 ukázek a 65 úkolů. Globálně 235 hlavních
+ 308 dalších řešení = 543; doplňkových ukázek 154. Celkem 250 lekcí
včetně 15 průvodců. Obtížnost 4/4, úvod 3/4. Starší obsah, ID a úložné
klíče se nemění, dříve rozepsaná práce a splnění se zachovají.

Nové ID:
- 21-droni-hrac-a-svet
- 22-droni-pronasledovani-a-rozestupy
- 23-droni-rizene-vlny
- 24-droni-zakladna-a-zivoty
- 25-droni-hra-pauza-a-vysledek

Kind gui, preview_images=true, limit 600 s, skutečné okno 720×540.
Šipky/WASD, závěr Mezerník start/nabídka, P pauza, R nový let, Esc/křížek
konec. N zahájí další vlnu pouze v tréninku 23. Běžné zavření ukládá droni.png;
Stop může proces ukončit bez obrázku. Okno běží na hostiteli Pythonu,
nepřenáší se do webové stránky. Stejná .venv/Python 3.14.8/pygame-ce 2.5.8,
žádné nové balíčky, povinný zvuk, cizí grafika nebo síťová data.

Podklady jsou samostatné stejné kopie podklady.py/zdroje.py/zasobnik.py/
sceny.py/sestava.py/herni_okno.py u každé lekce. Predchozi.py v 22–25
kumuluje přesné definice předchozích řešení. Cache obrázků/fontů z 16/1–2
a skutečný zásobník z 20/1 jsou převzaté beze změny definic; AST test hlídá
návaznost. Import modelu neotevírá okno ani mixer. Renderer kreslí skutečný
model, aktuální zónu a vrstvy; fonty se mezi běhy po pygame.quit obnoví.

Hráč zachovává desetinný pohyb a normalizuje diagonálu. Drony čtou společný
snímek původních poloh, poté všechny nové polohy zapíší; pořadí skupiny
nemění výsledek. Hlídač měří dosah od kotvy. Vlny vlastní Random(seed),
vybírají z osmi vstupů vzdálených nejméně 150 px, případně nejvzdálenější
bez losování; dohánějí celé intervaly a ponechají zbytek. Nová vlna zachová
Group a odstraní stará členství přes kill. Pohyb nových objektů je společný.

Cíl mise: nejméně šest cyklických dat a přežití tří desetisekundových vln,
tři životy. Přístav chrání jen celý obraz uvnitř zóny, energie 2,5 s,
obnova 0,5/s pouze mimo zónu; částečná energie nepokrývá celý krok.
Kontakty jsou kruhové včetně tečny, dávka odebere jeden život a spustí
0,9 s nezranitelnosti, drony zůstanou. Smrtelný kontakt předchází sběru
i úspěchu. Nová vlna neobnovuje životy, data, skóre či energii. Po konci
se zmrazí i náhoda. Konec rozlišuje úspěch, nedostatek dat a ztrátu životů.
Čekání v přístavu k výhře nestačí. Tick(60) převádíme na sekundy a dt
omezujeme na 0,05; pauza zastaví model/frontu/dobíjení bez dohánění času.

Menu/Let/PauzaLetu/Vysledek používají zásobník z 20: aktualizuje jen vršek,
kreslí odspodu. Pokračování obnoví stejný let, restart vytvoří nový svět
se seedem a původní model nemění. Neúspěšná konstrukce zachová starý stav.
Stejný seed opakuje začátek, None dává nový náhodný začátek.

Devět skupin test_droni prošlo: 36 chybných variant odmítnutých,
15 jiných správných zápisů přijatých, navíc odmítnuté chybějící GUI,
přesná řešení/helpery/AST, pět skutečných SDL běhů s PNG 720×540
a pět samostatných Python úryvků výkladu. Opakovatelná cesta se seedem 23
dokončí misi běžnými směry bez úprav životů; nečinný hráč nevyhraje.
Kontrola používá vlastní matematiku, čas, geometrii, RNG a skutečné pixely,
ne porovnávání zdrojového zápisu. Cílený validátor 25 lekcí: 0 chyb/upozornění.
Celková unittest sada na Pythonu 3.14.8/Linux: **346 testů OK bez přeskočených,
994 s**, včetně celkové validace 250 lekcí. Starší ResourceWarning z pomocných
procesů a souborů nejsou selhání; místní HTTP/SMTP testovací servery byly povolené.

Chromium e2e_droni prošlo pět odmítnutých šablon/přijatých řešení,
deset skutečných SDL běhů/PNG/stažení, přesný vzor bez přepsání práce,
workspace/číslování/readonly, kvízy, reload/splnění a mobil 380/320 včetně
otevřeného řešení. Ověřen i dlouhý běh/Stop a zachovaná starší lekce 20.
Prošly regrese e2e_soucasti (15 ukázek/25 úkolů) a e2e_solutions
(195 ostatních lekcí). Native offscreen smoke prošel všech pět skutečných
smyček, pohyb se skriptovaným vstupem, pauzu/pokračování, všechny tři
výsledky, nabídku, restart a QUIT v pauze. Snímky hry, pauzy, výsledku
a mobilního řešení prohlédnuty. Fyzická klávesnice a Windows/macOS vyžadují
vlastní zkoušku. Logy/snímky mimo repo v /workspace/scratch/drones-work.

Aktualizovány katalog/panel/plán 25/30, profil přípravy editorů,
README/PLAN/SCHEMA/instalace/spuštění a počty v testech. Serverové API,
JS, CSS a běhové limity se nemění. Dodávka commit/push do main bez ZIPů
a publikace cloudového prostředí.

Další krok na další pokyn: **Ověření a předání 26–30** — deterministické
scénáře, vlastní testy modelu, JSON skóre včetně chybějícího/poškozeného
souboru, čisté prostředí a volitelné balení pro vlastní OS, vlastní varianta
a návod k předání. Více příkladů u samostatných témat, navazující projekt
ponechat souvislý, vždy možné řešení. Odhad 15–20 tisíc tokenů.
Historické zápisy níže nejsou novým zadáním.


## Aktuální v0.71 (9. 11. 2026): Součásti větší hry 16–20

Na pokyn „pokračuj“ dokončen m04 Pygame 2. Pět samostatných témat: 16 cache
obrázků/fontů/velikostí, volitelný zvuk a sada zdrojů; 17 smyčka/jednorázová
animace/pás snímků/Sprite/stavové animace; 18 maska/offset/obnova/dvojice/tři
pravidla kolize; 19 sledování kamery/převody/viditelnost/clip; 20 zásobník/pauza/
tlačítko/nabídka/řidič přechodů. V každé tři ukázky, pět úkolů s vlastním zadáním,
šablonou/kontrolou/možným řešením a tři kvízové otázky. Projekty 6–15 zůstávají
souvislé. Kurz draft, dostupných 20/30, celkem 40 ukázek a 60 úkolů. Globálně
230 hlavních + 308 dalších řešení = 538, doplňkových ukázek 154. Obtížnost 4/4,
úvod 3/4. ID starších lekcí a úložné klíče zachovány.

Nové lekce kind console/preview_images=true, skutečné PNG soucasti.png 720×420,
bez automatické GUI smyčky nebo otevírání mixeru. Výklad to rozlišuje od živých
her: náhledy jsou zaznamenané fáze, PNG se nepohybuje. Vlastní Surface/BMP/WAV,
žádné cizí obrázky, síťová data či nové balíčky; stále pygame-ce 2.5.8/Python 3.14.8.
Podklady.py vytvoří media vedle helperu přes __file__, existující soubory neobnovuje
automaticky. Výstupní PNG je v pracovní složce. Každý úkol má úplné vlastní
podklady; potřebné starší definice v zdroje.py/animator.py/masky.py/kamera.py/
ovladace.py/rezimy.py jsou přesné AST kopie. Import modelu neotevírá okno/mixer.

Cache obrázků chrání načtený vzor i vracené výsledky kopiemi, fonty sdílíme
vědomě a velikosti obrazu cachujeme podle dvojice rozměrů. Zvuky mají injektovanou
továrnu, vypnutí bez volání, cache úspěšného načtení, hlasitost 0..1, kontrolu
kanálu a pouze pygame.error fallback. Volitelný prehraj_ton.py --play otevře
zařízení v potomkovi s limitem 5 s, bez --play nic nepřehraje. Skutečný dummy
mixer dekódoval vlastní mono PCM WAV a přijal kanál; fyzická slyšitelnost nebyla
ověřena. Nativní cloudový Pulse nemohl vytvořit /home/agent/.config/pulse a
nereagoval. Ohraničený helper se korektně ukončil za 5.03 s. Nic se kvůli tomu
neinstalovalo, tichý průchod kurzem funguje. První ruční neomezená diagnostika
byla ukončena, její proces už neběží.

Animace dohání celé intervaly a zachová zbytek, hranici float toleruje; jednorázová
končí po celém posledním intervalu. Výřezy vlastní pixely, Sprite zachová aktuální
střed při nové velikosti. Masky testují alfa > práh (včetně rovnosti), RGB colorkey
a asymetrické offsety; po změně obrazu obnoví rect i masku. Dvojice zachovají
identity/skupiny. Kamera drží světové polohy, počítá offset výhledu/desetinný
posun/malý svět, vyřazuje pro kreslení bez mazání a obnoví původní clip i při
chybě. Řidič režimů deleguje podle kompozice, mění svět až po úspěšné továrně.
Kolizní pokusy 18/2 a 18/5 navíc zobrazují společnou polohu kruhu a robota v otvoru.

Úkol 20/5 má po uložení reseni.py volitelnou ziva_dilna.py: jediné místní okno
720×420, klik na Spustit dílnu, P pauza/pokračování, M z hraní do nabídky,
Esc/křížek konec, normální zavření uloží rezimy-zive.png. Čte skutečný RidicScen
ze studentského souboru. Běžné tlačítko Spustit zůstává konzolovým PNG pokusem;
bonus vyžaduje místní grafickou plochu na hostiteli Pythonu a nepřenáší se do webu.

Devět skupin test_soucasti prošlo: 50 odmítnutých chybných variant, 25 přijatých
jiných zápisů, AST/přesná řešení, 40 běhů řešení/ukázek/pěti úryvků, skutečný
dummy mixer/WAV a bonusová SDL smyčka. Doplňující cílený test masek prošel i po
rozšíření hodnot alfa přesně na prahu. Validátor všech 20 lekcí Pygame 2 má
0 chyb/upozornění. Chromium e2e_soucasti prošlo všech 15 ukázek/25 úkolů,
šablony/vzory/PNG/stažení, soubory ve workspace, číslování, přepínání/reload,
zachování rozepsané lekce 15/splnění a mobil 380/320 u každého úkolu včetně
otevřeného řešení. Regrese e2e_roboti a e2e_solutions (190 ostatních lekcí) prošly.
Native offscreen smoke ověřil nabídku/klik/hraní/pauzu a zamrzlý čas/pokračování/
nabídku/nový svět/QUIT v pauze přes skutečný framebuffer a SDL frontu. Snímky
animace/kolizí/kamery, pauzy i mobilních panelů prohlédnuty. Fyzická myš/klávesnice,
slyšitelnost a Windows/macOS vyžadují vlastní zkoušku. Celá unittest sada:
**337 testů OK bez přeskočených, 970 s**, včetně celkové validace 245 lekcí.
Hlavní pokusy v 65 nových programech mají čitelnější samostatné řádky, ověřena
shoda AST před/po formátování. Podrobnosti viz poslední STATUS.md;
logy/snímky mimo repo v /workspace/scratch/components-work.

Aktualizovány katalog/panel/plán 20/30, profil přípravy všech editorů,
README/PLAN/SCHEMA/instalace/spuštění a počty v testech. Server/API/JS/CSS a limity
beze změny. Další krok na další pokyn: **Hon na dronech 21–25** podle plánu,
spolupracující Hra/Hrac/Dron, pronásledování/rozestupy, vlny, bezpečná zóna,
pauza/restart a ladění hratelného celku. Jeden souvislý projekt s řešením každého
kroku, bez nesouvisejících variant. Využít nové součásti podle potřeb hry, zvuk
může zůstat volitelný. Odhad 15–20 tisíc tokenů. Dodávka commit/push do main,
bez ZIPů a bez publikace cloudového prostředí. Historické zápisy nejsou nové zadání.

## Aktuální v0.70 (9. 11. 2026): Chyť robota 11–15

Na pokyn „pokračuj prosím“ dokončen další modul Pygame 2 podle plánu. Jeden
navazující projekt: 11 Robot/kruh/horní cíl a místo kliknutí, 12 Hlidac/Kyvac
a polymorfní pohyb, 13 Lov s body/životy/přesností, 14 Kolo s herním časem a
rychlejšími vlnami, 15 Hra s nabídkou/pauzou/výsledkem/restartem. Každý krok má
jednu ukázku, šablonu/úkol/kontrolu/možné řešení a tři kvízové otázky. Bez dalších
nesouvisejících variant. Kurz draft, dostupných 15/30, 25 ukázek/35 úkolů,
obtížnost celku 4/4 (úvod 3/4). Globálně 225 hlavních + 288 dalších řešení = 513.

Stále jen pygame-ce 2.5.8/Python 3.14.8 a stejná .venv pro terminál/editor.
Nové lekce kind gui/preview_images=true, místní okno 720×520, v závěru Mezerník
start/návrat z výsledku, P pauza, R nový lov, Esc/QUIT konec. Levé tlačítko chytá
podle udalost.pos, nikoli pozdějšího mouse.get_pos; při překrytí jen horní cíl.
Kruh používá viditelný rect.center, hrana se počítá. Kill odstraní chycený objekt
ze všech skupin, skóre používá jeho hodnotu a přesnost podíl zásahů/pokusů.
Bez životů či cílů se kliky neúčtují. Další vlna zachová čas a čítače, počet
nejvýše šest, rychlost nejvýše 220 px/s, perioda nejméně 0.7 s. Konec zmrazí model.

Předchozí modely jsou v files/predchozi.py jako přesné AST kopie, stejně jako
v Meteoritech. Sestava.py poskytuje obal rozpracovaným krokům, herni_okno.py
skutečný renderer/smyčku. Import modelu neotevírá GUI, smyčka běží pod __main__.
Update před událostmi zabrání bodování po vypršení času stejného snímku;
dt=min(tick(60)/1000,0.05) je herní čas, v pauze se neposouvá. Restart vytváří
nové Kolo(seed) bez změny starých skupin; seed=None může začít novou posloupnost.
Běžné zavření uloží poslední roboti.png před pygame.quit, web jej zobrazí/stáhne,
Stop to nezaručuje. Živé okno je na hostiteli Pythonu, vyžaduje místní plochu,
myš a klávesnici; nepřenáší se do webu. Vlastní grafika, bez zvuku/sítě/účtů.

Nový dilna_check/roboti.py prověřuje reálné typy, pixely, nezávislé geometrické
a časové vstupy i RNG orákulum, následně skutečný pgrun s kliknutím/zavřením/PNG.
Devět skupin test_roboti má 44 odmítnutých chybných variant a 16 správných
alternativ, AST návaznost a pomocné soubory, přesné řešení, pět Python úryvků
a test pořadí čas/klik ve skutečné smyčce. Cílená sada i validátor všech 15 lekcí
Pygame 2 prošly. Mobilní kontrola odhalila dlouhé vzorce v textu 12/14: opravené
mezery a inline kód, všechny nové lekce prošly šířkou 320 i s řešením.
Přehled přechodů je seznam, protože místní Markdown nepodporuje tabulky.
Samostatný SDL offscreen smoke všech pěti původních vstupních souborů s reálnou
frontou událostí/framebufferem prošel: klik, životy, normální ukončení/PNG a v
závěru nabídka/start/pauza/pokračování/oba konce/restart/návrat. Snímky prohlédnuty.
Fyzická myš/klávesnice, Windows/macOS a nativní editory tím nejsou ověřené.
Celá unittest sada: **328 testů OK bez přeskočených, 965 s**, včetně celkové
validace 240 lekcí. Prošly Chromium e2e_roboti, e2e_meteority a e2e_solutions
(185 ostatních lekcí). Podrobnosti viz poslední STATUS.md; logy/snímky mimo repo
v /workspace/scratch/robot-work.

Aktualizovány katalog/panel/plán 15/30, profil přípravy, instalace/spuštění,
README/PLAN/SCHEMA a testové počty. Původní ID a úložné klíče zachovány.
Další krok na další pokyn: **Součásti větší hry 16–20** — sdílené obrázky/fonty/
zvuky, animace s časem, přesnost kolizí, kamera a souřadnice, herní režimy.
Samostatným tématům přidat více smysluplných ukázek/úkolů s řešeními; návazné
projekty zachovat jako celek. Před zavedením audia ověřit zvuková zařízení a
kontrolu bez nich, žádné zbytečné nové knihovny. Odhad 15–20 tisíc tokenů.
Dodávka commit/push do main bez ZIPů a bez publikace cloudového prostředí.
Historické zápisy níže nejsou nové zadání.

## Aktuální v0.69 (9. 11. 2026): Meteority 6–10

Na pokyn „Pokračuj“ dokončen druhý modul Pygame 2, první souvislá živá hra.
06 Hrac a smyčka/šipky/dt/hranice celého obrázku, 07 Meteorit a proud s předaným
RNG/časovým zbytkem/odstraněním, 08 Zdravi a kruhové dávkové zásahy/nezranitelnost,
09 Kolo se skóre za minuté kameny a štítem, 10 Hra s pauzou/koncem/restartem.
Každý krok má jeden příklad, úkol se šablonou/kontrolou/možným řešením a tři
kvízové otázky; bez nesouvisejících variant. Kurz je draft, dostupných 10/30,
celkem 20 ukázek/30 úkolů, obtížnost dál 4/4 (úvod 3/4). Globálně 220 hlavních
+ 288 doplňkových řešení = 508. Starší ID, drafty a postup zůstávají stejné.

Nové lekce jsou kind gui, preview_images=true, bez nových závislostí (pygame-ce).
Skutečné okno 640×480 vzniká přes společné herni_okno.py na hostiteli Pythonu,
nikoli uvnitř prohlížeče. První modul dál funguje bez okna; pro hraní hry Meteority
je potřeba místní grafická plocha, zvuk nepotřebujeme. Od kroku 10 šipky/P/R/Esc.
Při normálním zavření se před pygame.quit uloží poslední meteority.png, který
web nabídne ke stažení. Stop ukončí proces bez záruky PNG. Smyčka zpracovává
události i při pauze a po ztrátě životů; dt=min(tick(60)/1000,0.05). Sprity se
kreslí s clip na hrací plochu, aby nový kámen nezakryl HUD. Podklady jsou vlastní
kresby; žádné účty, síťová data, externí obrázky ani zvukové soubory.

Files/predchozi.py obsahuje přesné předchozí modely (AST shodu hlídá test),
sestava.py dává rozpracovaným krokům společný obal. Pomocné soubory se kopírují
vedle studentského kódu. Import modelu neotevírá GUI; entrypoint pod __main__
spouští tutéž skutečnou hru. Proud nejprve posune staré kameny, potom vytvoří nové;
bonusy mají stejné pravidlo. Skóre=minulo, nikoli opakované přičítání. V jednom
kroku se nejprve sebere štít, potom vyhodnotí zásahy; během ochrany se štít
nespotřebuje. Restart vytváří nový Kolo(seed), staré skupiny neničí. Seed=7
zopakuje náhodnou posloupnost, None při novém kole žádá nový náhodný začátek.

Volitelný dilna_check/meteority.py ověřuje skutečné typy, geometrii/pixely,
desetinný čas/pohyb, libovolné hranice, předanou náhodu, pořadí aktualizací,
kill všech členství, dávkové zásahy, ochranu, bonusy, konec a nezávislý restart.
Následuje skutečný pgrun se vstupem, uzavřením a PNG. Osm testových skupin
obsahuje 40 odmítnutých chyb a 15 přijatých alternativ, pomocné soubory,
pět samostatných Python úryvků a 60snímkové běhy bez přesahu kamenů do HUD.
Validátor všech 235 lekcí prošel bez chyb/upozornění. Chromium e2e_meteority
prošlo všech pět šablon/řešení, deset skutečných SDL běhů s řízenými událostmi
a PNG/stažením, skutečný dlouhý běh a Stop, workspace, readonly, reload,
postup, plán/přípravu a mobil 380/320. Regrese e2e_pygame2_intro (15 ukázek,
25 úkolů) a e2e_solutions (180 ostatních lekcí) prošly. Samostatný SDL offscreen
smoke všech pěti kroků s reálnou SDL smyčkou/událostmi/framebufferem ověřil
normální ukončení, pauzu, konec a restart; snímky i mobil vizuálně prohlédnuty.
Fyzická klávesnice, nativní editory a Windows/macOS se tím netestují. Protokoly
a snímky jsou mimo repo v /workspace/scratch/meteority-work. Celá unittest sada:
**319 testů OK, bez přeskočených, 991 s**; podrobnosti v posledním STATUS.md.

Aktualizovány katalog, příprava, plán a dokumentace instalace/spuštění/schématu
i testové počty. Další krok na další pokyn: **Chyť robota 11–15** podle
courses/pygame-2/plan.md — cíle a myš z události, chování pohybu, kliknutí/body/
životy, čas/kola/obtížnost, nabídka a restart. Opět souvislý projekt s řešením
každého kroku, kind gui se smyčkou pod __main__, kontrolou modelů i skutečného
GUI běhu. Odhad 15–20 tisíc tokenů. Dodávka commit/push do main, bez ZIPů
a bez publikace cloudového prostředí. Historické zápisy níže nejsou nové zadání.

## Aktuální v0.68 (9. 11. 2026): Pygame 2, herní objekty 1–5

Na výslovný pokyn „Pokračuj prosím další kapitolou“ zahájen další plánovaný kurz v pořadí katalogu: Pygame 2. Hotov první pětilekcový modul Herní objekty, které jdou ověřit: 01 Sprite/image/rect, 02 Vector2 a dt, 03 Group/update/draw, 04 obdélníkové/kruhové kolize, 05 stav hry/pauza/časovač/restart. V každé jsou tři přepínatelné ukázky a pět samostatných úkolů se zadáním/šablonou/kontrolou/možným řešením a třemi kvízovými otázkami. Celkem 15 ukázek, 25 úkolů. Katalog i panel: draft, 5/30 dostupných, celek level 4, úvod 3. Aplikace má 215 hlavních + 288 doplňkových řešení = 503.

První modul je console s preview_images=true. Pracuje se skutečnými pygame Sprite/Surface/Vector2/Group a událostmi, místo nekonečné smyčky ukládá PNG 640×360 z posledního stavu. V aplikaci se zobrazí/stáhne, v editoru zůstane v pracovní složce. Nejde ještě o animované herní okno a výklad/příprava to výslovně říkají. Nahled.py kreslí vlastní mřížku/popisky a skutečné sprity. První blok nepotřebuje grafickou plochu, zvuk, cizí obrázky nebo síť. Profil instalace má Windows/macOS/Linux a VS Code/VSCodium/PyCharm; stále jen pygame-ce, ověřeno Python 3.14.8/pygame-ce 2.5.8. Opraven také starý text profilu OOP, který přes hotových 20 lekcí dosud tvrdil, že jde o koncept.

Files u každého úkolu jsou samostatné: zaklad.py, nahled.py a od třetí lekce pohyb.py s přesnou třídou PohyblivaLod z řešení 2/1. Shodu hlídá AST. Check.py přidává Path.cwd() do sys.path, protože kontrolní proces se spouští souborem z adresáře lekce a pomocné soubory jsou v jeho pracovní složce. Modely se načítají bez GUI, blok __main__ slouží vlastním ukázkám. Server se neměnil. Popisky existujících náhledů v UI jsou obecně obrázek (štítek, aria-label, alt), režim a limity PNG zůstávají stejné.

Volitelný pygame2_intro.py kontroluje reálné pixely/typy, identitu a nezávislost spritů, kopie vstupních vektorů/Surface, desetinné kroky a dt=0, normalizaci, hranice celé lodě, zvolenou krokovou aproximaci zrychlení a zastavení v cíli. Skupiny ověřuje na vlastních objektech v neabecedním pořadí i prázdné, s duplicitními polohami a sdíleným členstvím. Kill musí odstranit všechna členství, remove jen jedno. Kolize používají nezávislý výpočet průniků/vzdáleností a skutečné identity, dotyk Rect a kruhů mají výslovně různá pravidla. Stav zahrnuje opakovaný QUIT, KEYUP, pauzu, jednorázový časovač, nezáporné životy a tovární restart bez poškození staré skupiny. Kontrola nevyžaduje konkrétní AST implementace.

Sedm skupin test_pygame2_intro přijímá 25 odlišných správných variant a odmítá 36 chybných. Všech 25 vzorů běží i samostatně s PNG, dalších deset ukázek a pět Python úryvků výkladu také; celkem 40 skutečných běhů, vlastní soubory se nemění. Chromium e2e_pygame2_intro prošlo všech 15 ukázek a 25 úkolů: šablony odmítnuté/vzory přijaté, skutečné běhy/PNG/stažení, přesné řešení bez přepsání práce, workspace se soubory, číslování, přepínání a reload, zachovaný kód/splnění pandas 42 a mobil 380/320. Prošly regrese e2e_solutions (175 ostatních lekcí), e2e_pandas_plots a e2e_web. Náhled a mobilní řešení vizuálně prohlédnuty. Validátor všech 230 lekcí má 0 chyb/upozornění; konečný výsledek unittest viz nejnovější STATUS.md. Nativní editory, Windows/macOS ani skutečné herní okno se v tomto modulu netestují. Protokoly/snímky mimo repo v /workspace/scratch/pygame2-intro-work.

Aktualizovány README/PLAN/SCHEMA/instalace/spouštěcí pokyny, profil přípravy a počty v testech. Další krok na další pokyn pokračovat: **Meteority 6–10**, první živá hra podle courses/pygame-2/plan.md. Vstup/dt/hraniční poloha → vznik meteoritů → zásahy/životy/nezranitelnost → skóre/štít → pauza/konec/restart. Jeden návazný projekt, každý krok s řešením, bez nesouvisejících variant. Kind gui, herní smyčka pod __main__, headless kontrola přes pgrun (Clock.tick vrací 16 ms); skutečné okno a OS ověřit zvlášť. Odhad 15–20 tisíc tokenů. Dodávka commit/push do main bez ZIPů a bez publikace cloudového prostředí. Starší ID, uložený kód a klíče postupu zachovány.

## Aktuální v0.67 (9. 11. 2026): Čísla řádků a komentování v editoru

Na výslovné zadání uživatele dokončeno číslování řádků ve společném createEditor pro úkoly a ukázky včetně readonly. Samostatný levý sloupec není součástí textarea, má aria-hidden a nejde vybírat; kopírování obsahuje pouze kód. Počet zahrnuje prázdný koncový řádek, mění se při psaní/set/přepínání a šířka roste s počtem číslic. Čísla a zvýraznění se posouvají svisle společně, při vodorovném posunu zůstávají čísla vlevo; při přepočtu výšky se zachovává posun. Uložené klíče kódu a postupu se nemění.

Dosavadní Ctrl+/ podporuje řádek i blok; rozšířeno o Ctrl+Shift+7 podle fyzického Digit7 pro české klávesnice a stejné varianty s Cmd. Alt/AltGr se nezachytává. Komentování zachová odsazení, kurzor a směr výběru, přesně vynechá další řádek při výběru končícím na jeho začátku, zvládne prázdný první řádek i odsazený prázdný řádek. Prázdné řádky uvnitř bloku zůstanou; smíšený blok se celý zakomentuje, plně zakomentovaný odkomentuje. Opraven lineStart pro index 0 před úvodním newline. Používá stejný undo mechanismus execCommand jako ostatní chytré úpravy.

Tlačítko ? vysvětluje čísla a obě zkratky pro jeden/více řádků včetně Cmd. Na mobilu se tabulka nápovědy mění na jeden sloupec. Chromium e2e_editor_lines ověřuje skutečné klávesy, výběr/kurzor, komentáře, undo/redo, vložení i kopii více než 1000 řádků ze schránky, oba posuvníky a skutečné souřadnice čísel/zvýrazněného textu, přepínání ukázek/úkolů, readonly, reload/postup a šířky 1100/380/320. Velké Locator.fill dokončovalo vložení, ale vypršel jeho automatizační timeout; test proto používá běžné vložení ze schránky. Zarovnání porovnává skutečné glyphy: computed lineHeight je zaokrouhlený a po 999 řádcích vytvářel falešný rozdíl. Regrese e2e_editor a e2e_tasks prošly. Snímky editoru a mobilní nápovědy prohlédnuty; protokoly/snímky mimo repo v /workspace/scratch/editor-lines-work. Události Ctrl/Cmd ověřené v Chromiu/Linuxu, nativní macOS se tím netestuje.

Obsah kurzů pokračuje ve stavu v0.66 níže (Datová analýza 42/42). Dodávka commit/push do main bez ZIPů a bez publikace cloudového prostředí. Další práci určí připomínky uživatele; nový kurz automaticky nezačínat.

## Aktuální v0.66 (8. 11. 2026): Datová analýza 42/42, Analytická dílna

Hotov závěrečný modul pandas 36–42 jako jeden souvislý projekt: otázka a zdroje, čištění s auditem, spojování/souhrny, graf/zpráva, testy, volitelný notebook a předání. Každý krok má jednu ukázku, jedno zadání se šablonou/kontrolou/možným řešením a tři kvízové otázky. Projektové kroky nemají examples.json ani tasks.json. Ověřené předchozí funkce jsou vždy přiložené v predchozi.py; AST test hlídá přesnou návaznost a shodu s předaným projektem. Kurz nyní 42/42, 108 ukázek a 174 úkolů; aplikace 210 hlavních + 268 doplňkových řešení = 478. Stav draft zůstává pro připomínky studentů. Starší ID, uložený kód a klíče postupu se nemění.

Vlastní syntetická měření teplot mají 11 záznamů = 7 přijatých + 4 odmítnuté; přijaté se dělí na 6 spárovaných a 1 neznámý kód 999. Textové kódy 001/010/NA zůstávají textem, platné nuly/záporné teploty/opakovaná pozorování se neztrácejí. Audit uchová původní text, pořadí záznamu od 1 a první důvod podle priority chybi_kod > neplatne_datum > neplatna_teplota. Radek není fyzické číslo řádku CSV ani původní index DataFrame. Inf/NaN se odmítají přes isfinite. Left merge s indikátorem a validate many_to_one musí odmítnout i nepoužitý duplicitní katalogový klíč bez změny zdrojů.

Souhrny podle stanic jsou 001: 3 měření, průměr 28/3; 010: 2, průměr 1; NA: 1, průměr -2 °C. Celkový průměr je 28/6 = zobrazených 4,67 °C, nikoli průměr tří různě velkých skupin. Vytvor_vystupy vrací skutečné stanice.csv, prehled.xlsx se čtyřmi listy Stanice/Dny/Nespárovaná/Odmítnutá, teploty.png 720×480 a zprava.md. Graf nesmí skrýt záporné teploty nastavením y od nuly. Zpráva odděluje počet přijatých/odmítnutých/spárovaných/nespárovaných, prázdný průměr a omezení vlastních cvičných dat; nedokazuje příčinu ani klima. Excel nerozlišuje původní prázdný text od prázdné buňky; audit v paměti původní text zachovává.

Lekce 40 používá pandas.testing s tolerancí 1e-12 při zachování typů, pořadí a popisků a osm veřejných unittest testů. Lekce 41 vytvoří platný čistý notebook formátu 4.5: úvod a pět dodaných kódových buněk, unikátní id, prázdné výstupy, execution_count=None a metadata Python jádra. Skript bez_notebooku.py nabízí stejné kroky bez Jupyteru; v prohlížeči běží tato varianta. Lekce 42 přenese skutečné předané vstupy a podklad projekt do samostatného adresáře, doplní notebook a výstupy. Adresář obsahuje CLI analyza.py s volbami cest, vlastní pomocné funkce/testy, README, slovník, requirements.txt a .gitignore. README vysvětluje venv, instalaci, běh, ověření i každý základní Git příkaz. Celý projekt funguje po přenesení jinam bez importů Akademie; žádné automatické git init/push ani zveřejnění studentských dat.

Stažení zachovává CSV/XLSX jako výchozí režim s limitem 6 souborů. Pouze hlavní lesson.json může rozšířit download_formats o .md/.ipynb; server tyto formáty vybírá z pevného seznamu a limit je pak 12, stále 2 MB na soubor a 4 MB celkem. MD musí být UTF-8, IPYNB JSON se základní notebookovou strukturou. POST tělo rozšíření nevynutí, jiné přípony a symlinky se nestahují. V závěru jsou dostupné dokumenty i notebook, PNG zůstává samostatným náhledem/stažením. Lekce 40 negeneruje nový PNG, přesto má preview_images kvůli headless importům předchozích funkcí. Po reloadu se odkazy vytvoří novým během; kód a postup zůstávají. Token/Host/Origin, úklid a ostatní limity se neměnily.

Volitelný lib/dilna_check/pandas_final.py používá nezávislý Python výpočet čištění a souhrnů, kontroluje reálné CSV/XLSX/MD, obsah a rozsah grafu a notebook včetně skutečného provedení buněk. Předaný adresář zkopíruje mimo původní složku a spustí jeho CLI i veřejné testy bez PYTHONPATH Akademie. Test_pandas_final má deset skupin, 32 chybných a osm správných alternativ; přijímá jiné správné postupy, barvy i zdrojové řetězce buněk. Odmítá i neúplnou strukturu a JSON-neuložitelné hodnoty notebooku a soubor přejmenovaný na XLSX; špatný výsledek nemá způsobit chybu kontroly. Test_file_downloads má nově osm skupin včetně volitelných formátů, limitu 12 a ignorování neautorizovaného rozšíření z požadavku. Dosavadní pandas_tools/matplotlib_tools beze změny, základní kontrola nevyžaduje pandas.

Chromium e2e_pandas_final prošlo všech sedm kroků: ukázky, odmítnuté šablony, přijaté a skutečně spuštěné vzory, přesná řešení bez změny práce/postupu, soubory/PNG, workspace, reload, zachovaný předchozí projekt a mobil. Dlouhý výčet důvodů ve 37 byl rozdělen do odrážek kvůli mobilní šířce. Prošly regrese e2e_pandas_files a e2e_solutions (170 ostatních lekcí). Čerstvý pohled ověřil plán/přípravu 42/42, dokončený modul 36–42 a počty 108/174; mobilní řešení a soubory vizuálně prohlédnuty. Skutečné ipykernel Pythonu 3.14.8 provedlo všech 108 ukázek po buňkách # %% a notebook dvakrát po restartu skutečného jádra. Mezi lekcemi se musí znovu načíst měněné moduly predchozi/test_dilna/bunky/bez_notebooku; samotný reset proměnných nevymaže importní cache. Nativní VS Code/VSCodium/PyCharm se tím netestují. Celkové výsledky unittest/validátoru viz nejnovější STATUS.md.

Python 3.14.8/pandas 3.1.1/NumPy 2.5.4/Matplotlib 3.11.2/openpyxl 3.1.5/ipykernel 7.4.0, bez nových závislostí. Aktualizovány katalog, plány, příprava, README, schéma a instalační/spouštěcí pokyny. Protokoly/snímky mimo repo v /workspace/scratch/pandas-final-work. Další práce: obsahové korektury a připomínky studentů k hotovému kurzu; nový kurz nerozpracovávat automaticky. Dodávka commit/push do main bez ZIPů a bez publikace cloudového prostředí. Starší oddíly níže popisují historii, nikoli další zadání.

## Aktuální v0.65 (8. 11. 2026): Datová analýza 35/42 a stažení CSV/XLSX

Hotov sedmý modul pandas 31–35: čtení Excelu/textové kódy, export/ověření CSV, export Excelu/více listů, opakovatelný postup a měsíční projekt kavárny. Samostatné lekce 31–34 mají po třech ukázkách a pěti úkolech s vlastním zadáním/šablonou/kontrolou/možným řešením a třech kvízových otázkách. Projekt 35 tvoří jedna ukázka a jedno souvislé zadání se třemi funkcemi, řešením a pěti otázkami. Nově 13 ukázek a 21 úkolů; pandas 35/42, 101 ukázek a 167 úkolů. Aplikace 203 hlavních + 268 doplňkových řešení = 471. Projekty 20 a 35 mají výjimku z přepínatelných variant. Plán, příprava a dokumentace aktualizované. Python 3.14.8/pandas 3.1.1/NumPy 2.5.4/Matplotlib 3.11.2/openpyxl 3.1.5, závislosti beze změny. Microsoft Excel ani veřejná síť nejsou potřeba.

Lekce 31–35 mají download_files=true v hlavním lesson.json. API lesson vrací bool, run jej určí z hlavní lekce i pro doplňkový úkol, nikoli z POST těla. Po dokončení vrací chráněný poll files:[{name,mime,data}] s base64 jen pro UTF-8 CSV (také BOM) a XLSX se základní ZIP strukturou. Zahrnuje přiložené vstupy i vytvořené výstupy z podsložek; jiné přípony a symlinky se nepřebírají. Limity 6 souborů, 2 MB každý, 4 MB celkem, případné vynechání má file_notice. Projekt 35 současně používá náhled PNG z minulé verze. Server dál jen standardní knihovna, žádná nová povinná závislost. Runner čte bajty před odstraněním dočasné složky. Klient tvoří odkazy přes DOM, jména jako text; po přepnutí/novém běhu staré odkazy zmizí a opožděný poll je nemůže vrátit. Po reloadu kód/postup zůstávají, nové odkazy vytvoří spuštění.

Výklad vysvětluje sešit/list/hlavičku, sheet_name/usecols/skiprows, skutečný textový kód versus číselný formát 000, dtype a keep_default_na=False pro doslovné NA. CSV rozlišuje kódování, oddělovač/desetinnou čárku, uvozování speciálních znaků, index=False, text v paměti a UTF-8 BOM. BOM nezaručuje správnou interpretaci kódu v Excelu. ExcelWriter uzavírá jeden zápis více listů, nové načtení ověřuje obsah, ne jen existenci. Samostatné výstupy jsou v jiné cestě než zdroje.

Cisteni.py u každého úkolu 34 obsahuje přesné funkce řešení 34/1 a 34/2. Čištění ořízne mezery, vyřadí prázdná místa a neplatné/neznámé hodnoty, zachová doslovné NA, nuly i opakovaná měření. Čtyři čisté záznamy mereni.csv: Brno 1,5; Praha 2,5; NA 0; Brno 1,5. Pomocník u úkolů 3 a 5 dovoluje soustředit se na propojení kroků; zdrojové soubory se nemění. Kavarna.py ve files 35 má přesné funkce projektu 20, shodu hlídá AST test.

Projekt 35 vybere skutečný kalendářní měsíc v datetime64[us] bez NaT/pásma, zachová index/pořadí a z kopie vytvoří přehled. Výběr je [první den měsíce, první den dalšího měsíce), zvládá přestupný únor i prosinec. Agregace mají dosavadní formát podle_dnu/podle_produktu/celkem; potvrzený měsíc bez prodeje má prázdné tabulky a celkové nuly. Uloz_report vytvoří podle_dnu.csv, prehled.xlsx (Dny/Produkty/Celkem) a trzby.png (6×4 palce, 120 DPI, skutečné tržby podle produktů, y od nuly), vrací Path ve slovníku csv/excel/graf. Jiné soubory a přehled zachová. Dodaná data: únor 6 řádků, 10 kusů, 563 Kč; dny 270/45/248, produkty NA 0/caj 135/kava 428. Dvě stejné únorové položky se obě započítávají; leden/březen ne. Březnová tržba samostatně 10 Kč.

Volitelný pandas_files.py používá skutečné XLSX vytvořené openpyxl a nezávislé csv.reader/openpyxl porovnání exportů, textových typů buněk, hlaviček/listů a přesných hodnot. Časové souhrny projektu počítá nezávislý Python cyklus bez groupby. Při skutečném PNG uložení zachytí Figure a ověří artists, barvy/fonty nepředepisuje. Deset skupin test_pandas_files má 28 chybných a 23 správných alternativ, 21 samostatně spustitelných vzorů, pět Python úryvků výkladu, shodu helperů a skutečný projekt nad dvěma měsíci. Negativní testy doplnily skutečně neabecední názvy listů a opakované prodeje; jinak by nesprávné sort/drop_duplicates náhodou vycházely správně. Číselné případy obsahují i přesné desetinné hodnoty pro odhalení zaokrouhlení. Šest skupin test_file_downloads ověřuje opt-in/task/token, přesné bajty/MIME, limity, symlinky, zachování souboru po chybě a úklid podsložek. Pandas_tools ani Matplotlib_tools se neměnily.

Výsledky celkových unittest, validátoru, Chromium a skutečného Jupyter ověření viz nejnovější STATUS.md. Celkový test validátoru má pro rostoucí katalog limit 420 s (dosud 300); studentské běhy a CHECK_TIMEOUT beze změny. Celkové kontroly potřebují místní HTTP/SMTP sockety. Protokoly/snímky mimo repo v /workspace/scratch/pandas-files-work. Nativní editory nejsou automaticky otestované prohlížečem/Jupyterem.

Další blok 36–42: závěrečný projekt Analytická dílna podle courses/pandas/plan.md. Sedm kroků má tvořit souvislý projekt se zdroji, datovým slovníkem, přehledem čištění, spojováním/souhrny, grafem/zprávou, testy, volitelným notebookem a předáním; nerozdělovat na nesouvisející varianty. Každý krok musí mít možné řešení. Zásady: zdroje neměnit, kontrolovat konkrétní obsah i součty, jasně vysvětlit příkazy, nejprve obyčejné .py a notebook volitelně. Starší ID, kód a klíče postupu zachovat. Dodávka commit/push do main bez ZIPů a publikace prostředí. Historické pokyny níže nejsou aktuálním zadáním.

## Aktuální v0.64 (8. 11. 2026): Datová analýza 30/42 a náhledy grafů

Hotov šestý modul pandas 26–30: Figure/Axes a popisky, čárové/sloupcové grafy, scatter a omezení závěrů, histogram/četnosti/hustota, export PNG. Každá nová lekce má tři ukázky, pět úkolů s vlastním zadáním/šablonou/kontrolou/možným řešením a tři kvízové otázky. Nově 15 ukázek a 25 úkolů; celý pandas 30/42, 88 ukázek a 146 úkolů. Aplikace 198 hlavních + 252 doplňkových řešení = 450. Projekt 20 zůstává jeden celek. Příprava, plán a dokumentace aktualizované. Python 3.14.8/pandas 3.1.1/NumPy 2.5.4/Matplotlib 3.11.2; závislosti beze změny. Prvních 25 lekcí používá pandas, 26–30 také Matplotlib, vše bez veřejné sítě či grafické plochy.

Nové lekce jsou kind=console s preview_images=true. Server určuje režim z hlavního lesson.json i pro doplňkový úkol; nepřebírá příznak z POST těla. Běh nastaví Agg a zapisovatelnou cache workspace/_run/_matplotlib, běžný runner Matplotlib neimportuje. Skripty tvoří skutečný Figure přímo, bez plt.show, a ukládají PNG. V editoru vznikne obrázek v pracovní složce procesu. Náhledy se před úklidem dočasné složky včetně podsložek přečtou do paměti; chráněný poll je vrací jako images:[{name,data}] s base64 a případným image_notice. Max 6 PNG, 2 MB a 8 milionů pixelů každý, 4 MB celkem. Kontrola hlavičky/rozměrů nevyžaduje grafické závislosti serveru; symlinky se nepřebírají. Toto je limit náhledu, nikoli samostatného exportu z editoru.

Runner-client zobrazí obrázky a odkazy Stáhnout PNG přes DOM, jména jako prostý text. Náhledy neukládá do localStorage. Nový běh, přepnutí úkolu či příkladu galerii vyčistí, starý opožděný poll nemůže nahradit nový graf. Po reloadu kód a postup zůstávají, obrázky vzniknou novým spuštěním. Bílý podklad náhledu nemění alfa kanál staženého PNG. Příklady při přepnutí nově vyčistí i starý textový výstup. Odkrytí řešení nadále nic nevkládá do editoru ani nemění splnění.

Výklad odlišuje skutečné x od pořadí, NaN jako mezeru od nuly, vývoj od kategorií a nulovou základnu sloupců. Scatter zachovává skutečné dvojice; dropna jen x/y nesmí ztratit řádek kvůli jinému sloupci. Graf sám nedokazuje příčinu, výrazný bod se automaticky nemaže. S je plocha značky, equal vyžaduje stejnou jednotku. Histogram poslední pravou hranici zahrne, hodnoty mimo rozsah nepočítá. Density normalizuje plochy, nikoli součet výšek; rozdílné šířky a společné stupnice jsou výslovně vysvětlené. Palce/DPI/pixely, průhlednost, tight/pad a relativní cesty jsou vysvětlené před úkoly.

Volitelný matplotlib_tools.py porovnává skutečné Figure/Axes a artists, data a popisky, předepsané značky, měřítka a geometrii histogramů; barvu/písmo nevyžaduje. Zachování vstupů používá dosavadní pandas_tools, ten se neměnil. Úpravy existující Axes/export zvlášť kontrolují identitu, data a DPI. Exportní kontroly skutečně otevírají PNG, kontrolují rozměry, DPI, čáru, alfa kanál a tight rámeček. Cizí aktuální pyplot Figure odhaluje chybné plt.savefig. Prázdný sloupcový graf může mít automatické číselné značky os, proto se u nulového počtu kategorií nevynucuje prázdný seznam tick labels. Devět skupin test_pandas_plots odmítá 35 chybných variant a přijímá 25 správných alternativ, spouští všech 25 řešení samostatně a pět úryvků výkladu. Šest skupin test_plot_previews ověřuje skutečný běh/API, token, metadata hlavní lekce u task-5, PNG limity, symlinky, chybu po grafu a odstranění podsložek. Základní dilna_check/server nemají novou povinnou grafickou závislost.

Výsledky celkového unittest, validátoru, Chromium scénářů a skutečného ipykernel viz nejnovější STATUS.md. Protokoly/snímky mimo repo v /workspace/scratch/pandas-plots-work. Celkové testy/validátor potřebují oprávnění otevřít místní HTTP/SMTP sockety. Nativní VS Code/VSCodium/PyCharm se browser/Jupyter testy neověřují.

Další blok pandas 31–35: Excel přes openpyxl, export CSV/Excelu, funkce pro opakovatelný postup a mini-projekt měsíčního přehledu kavárny s tabulkou a grafem. U samostatných témat více příkladů/úkolů s možnými řešeními; návazný projekt tvoří jeden celek. U lekcí s PNG zapnout preview_images v hlavním lesson.json. Starší ID, uživatelský kód a klíče postupu neměnit. Dodávka commit/push do main bez ZIPů a publikace cloudového prostředí. Historické pokyny níže nejsou aktuálním zadáním.

## Aktuální v0.63 (8. 11. 2026): Datová analýza 25/42

Hotov pátý modul pandas 21–25: zarovnání/reindex/concat, merge podle jednoho i více klíčů, validate/indikátor/suffixes, časový index a denní/měsíční resample. Každá nová lekce má tři ukázky, pět úkolů s vlastním zadáním/šablonou/kontrolou/možným řešením a tři kvízové otázky. Nově 15 ukázek a 25 úkolů. Celý pandas 25/42, 73 ukázek a 121 úkolů; celá aplikace 193 hlavních + 232 doplňkových řešení = 425. Projekt 20 zůstává jeden souvislý celek. Příprava, plán, katalog a dokumentace aktualizované. Python 3.14.8/pandas 3.1.1/NumPy 2.5.4, závislosti beze změny; prvních 25 lekcí nevyžaduje nové instalace ani veřejnou síť.

Spojování rozlišuje indexové popisky od hodnotového klíče a left/inner/outer. Concat zachovává platné duplicity a počet řádků i bez společného sloupce. Validate musí odmítnout také nepoužitý duplicitní pravý klíč; obě tabulky se zachovají i při MergeError. Chybějící cena známého produktu není chybějící protějšek. Ukázka vysvětluje odlišné párování chybějících klíčů proti SQL NULL, úkoly mají známé klíče. Dva významově různé sloupce stav se rozliší suffixes.

Časové úkoly mají datetime64[us] bez NaT a pásma. Přesný úsek zahrnuje obě hranice, celý den poslední mikrosekundu před další půlnocí; shodné časy zachovají stabilní pořadí, v kontrole i 40 řádků. Reindex vytváří mřížku bez doplňování hodnot, resample agreguje. Min_count=1 odděluje neznámý součet od nuly, size/count odlišují záznamy a dostupné hodnoty, MS jsou kalendářní měsíce, nikoli ms/30D. Testy zahrnují přestupný den, mezery, půlnoci a opakovaná měření.

Test_pandas_joins má deset skupin: odmítá 34 chybných variant a přijímá 25 správných alternativ, spouští všech 25 solution.py a pět Python úryvků výkladu. Integrační test propojí ceník s časovým souhrnem a zachová neznámé ceny i zdroje. Pandas_tools.equivalent nově nevyžaduje odvozené výstupní freq (správný ručně sestavený časový index může mít None) ani typ prázdného indexu sloupců u tabulky bez sloupců. Skutečné časy, jednotky, popisky, dtype hodnot, názvy a pořadí dál kontroluje. Přesná ochrana vstupů zahrnuje i freq a typy prázdných indexů obou os. Obě konkrétní správné alternativy i chybné hodnoty/názvy/tvary jsou testované. Základní dilna_check se dál obejde bez pandas.

Chromium e2e_pandas_joins prošlo 15 ukázek, 25 odmítnutých šablon/přijatých řešení i skutečných běhů, workspace, přesný vzor bez změny práce/postupu, reload/drafty/procvičení a mobil. Rozepsaný kód a splnění projektu 20 zachovány. Prošly regrese e2e_pandas_summary a e2e_solutions (153 ostatních lekcí). Čerstvý pohled po aktualizaci dokumentace ověřil přípravu/plán 25/42, dokončený modul 21–25 a počty 73/121; snímky mobilu i řešení prohlédnuty. Skutečné ipykernel ze stejné .venv provedlo všech 73 ukázek po buňkách v čistém jmenném prostoru včetně CSV projektu. Nativní editory se tím netestují. Celkový výsledek unittest/validátoru viz nejnovější STATUS.md. Protokoly a snímky mimo repo v /workspace/scratch/pandas-joins-work.

Další blok pandas 26–30: Figure/Axes, čárové a sloupcové grafy, bodový graf, histogram a PNG i bez grafické plochy. Zachovat více příkladů/úkolů s možnými řešeními u samostatných témat, projekty jako souvislé celky. Starší ID, uživatelský kód a klíče postupu neměnit. Dodávka commit/push do main bez ZIPů a publikace cloudového prostředí. Historické pokyny níže nejsou aktuálním zadáním.

## Aktuální v0.62 (8. 11. 2026): Datová analýza 20/42

Hotov čtvrtý modul pandas 16–20: souhrny/axis/min_count/count/size, groupby s chybějícími klíči, více agregací a pojmenované výsledky, průměr/medián/rozpětí a projekt kavárny. Samostatné lekce 16–19 mají po třech ukázkách a pěti úkolech s možnými řešeními. Projekt 20 tvoří jeden celek se dvěma funkcemi, jednou ukázkou a pěti kvízovými otázkami; záměrně nemá nesouvisející varianty. Nově 13 ukázek a 21 úkolů, celý pandas 20/42, 58 ukázek a 96 úkolů. Celá aplikace 188 hlavních + 212 doplňkových řešení = 400. Příprava, plán a dokumentace počty i výjimku projektu vysvětlují. Závislosti beze změny, Python 3.14.8/pandas 3.1.1/NumPy 2.5.4.

Projekt má vlastní prodeje.csv a README v files/. Cena platí pro jednotlivý řádek; tržba je součet kusy*cena. Prehled_kavarny vrací podle_dnu, podle_produktu a celkem, over_soucty porovnává oba přehledy s celkem přesně pro počty a s malou tolerancí pro float. Platný zdroj už je čistý a bez NA; nulové množství a stejně vypadající prodejní řádky jsou platné, nemají se zahazovat. CSV: 7 položek, 15 kusů, 687 Kč, denní tržby 270/148/269 a produktové 282/305/100. Kontrola používá nezávislý Python cyklus bez groupby a poškozené přehledy. Souhlas součtů sám negarantuje správné skupiny; ověřuje se také obsah. Zdrojová CSV se nemění.

Test_pandas_summary má devět skupin, 39 chybných variant odmítnuto a 23 správných alternativ přijato; spouští všech 21 solution.py a ověřuje skutečný CSV výsledek, čtyři Python úryvky výkladu a fakta o průměru průměrů. Negativní test doplnil nesymetrická data pro medián: u dvou hodnot se průměr náhodou rovnal mediánu. Pandas_tools.equivalent nyní pro booleovský výsledek přijímá Python bool i NumPy bool_, stále odmítá číslo 1 jako bool a bool jako číselný počet. Konkrétní správný alternativní projekt vracející výsledek Series.all to vyžadoval; tento případ i odmítnutí return 1 jsou otestované. Základní dilna_check nadále pandas neimportuje.

Chromium e2e_pandas_summary prošlo 13 nových ukázek, 21 šablon/řešení i běhů, projektové soubory, přesný vzor, workspace, reload/drafty/procvičení a mobil. Starší rozepsaná lekce 15/splnění zachovány. Regrese e2e_pandas_cleaning a e2e_solutions (148 ostatních lekcí) prošly. Po úpravě textů znovu vizuálně ověřen aktuální plán i příprava 20/42 a modulu 16–20, protože první e2e kopie vznikla před dokončením dokumentace. Skutečné ipykernel provedlo všech 58 dostupných ukázek po buňkách v čistém jmenném prostoru včetně CSV projektu. Nativní editory tím nejsou testované. Validátor 203 lekcí bez chyb a upozornění, celá unittest sada viz nejnovější STATUS.md. Snímky a protokoly mimo repo v /workspace/scratch/pandas-summary-work.

Další blok pandas 21–25: zarovnání/concat, merge a klíče, validate/kardinality a kontrola počtů, časový index a resample. Zachovat více příkladů a úkolů s řešeními u samostatných témat, projekty jako souvislé celky. Neměnit starší ID, uživatelské kódy a klíče postupu. Dodávka commit/push do main bez ZIPů a publikace cloudového prostředí. Historické pokyny níže nejsou aktuálním zadáním.

## Aktuální v0.61 (8. 11. 2026): Datová analýza 15/42

Na zadání pokračovat hotov třetí modul pandas 11–15: chybějící údaje a pravidla doplnění/vynechání; číselné převody a Int64; datumové formáty, čas, přestupné roky a NaT; duplicity/klíče/četnosti; cílené čištění textu. Každá nová lekce má tři ukázky a pět úkolů s vlastním zadáním, šablonou, kontrolou a možným řešením. Kurz nyní 15/42, 45 ukázek a 75 úkolů; celá aplikace 183 hlavních + 196 doplňkových řešení = 379. Příkazy jsou vysvětlené před použitím, zdroje se zachovávají. Prvních 15 lekcí používá jen dosavadní pandas>=3,<4, žádné nové balíčky či síťová data. Ověřeno Python 3.14.8/pandas 3.1.1/NumPy 2.5.4.

Nové test_pandas_cleaning má osm skupin, 41 chybných variant odmítnuto a 25 správných alternativ přijato. Kromě jednotlivých funkcí ověřuje složení čištění textu, čísel a datumů nad jednou tabulkou i zachování originálu. Datumové úkoly výslovně vracejí datetime64[us] bez časového pásma; období pracuje s datumy o půlnoci, obě hranice včetně. Chybný existující text se odlišuje od původní chybějící hodnoty. V přehledu chybějících údajů se typ počtů výslovně sjednocuje na int64 i pro tabulku bez sloupců; důvod je ve výkladu. Value_counts má dropna=False/sort=False a definovaná jména. Jednotka se odstraňuje jen jako doslovná koncová přípona. Pandas_tools.py beze změny.

E2e_pandas_cleaning prošlo 15 nových ukázek, 25 šablon/řešení i skutečných běhů, workspace, přesný vzor, reload/drafty/procvičení a zachovaný kód/splnění lekce 10. Mobil odhalil dlouhý nerozdělitelný inline příkaz v lekci 15: opraveno v lesson.css pomocí overflow-wrap:anywhere jen pro code v odstavcích/seznamech prose. Bloky kódu zůstávají neposkládané s vlastním horizontálním posouváním; test ověřuje obojí. Prošly regrese e2e_pandas_selection a e2e_solutions (143 ostatních lekcí včetně mobilu). Skutečné ipykernel provedlo všech 45 dostupných ukázek po buňkách v čistém jmenném prostoru. Nativní editory tím nejsou testované. Validátor všech 198 lekcí bez chyb a upozornění; kompletní unittest výsledek v posledním STATUS.md. Agregovaný test validátoru má nyní limit 300 s pro rostoucí katalog, limity jednotlivých studentských běhů se nemění. Protokoly/snímky mimo repo v /workspace/scratch/pandas-cleaning-work.

Další blok pandas 16–20: souhrny/axis/count/size, groupby, více agregací a pojmenované výsledky, statistika a mini-projekt kavárny. Zachovat více ukázek a procvičení s řešeními u samostatných témat; navazující projekty tvoří celek. ID a postup starších lekcí neměnit. Dodávka přes commit/push do main, bez ZIPů a publikace cloudového prostředí. Starší pokyny níže nejsou aktuální zadání.

## Aktuální v0.60 (8. 11. 2026): Datová analýza 10/42

Pokračování pandas na zadání uživatele. Hotov druhý modul 6–10: sloupce a rozdíl Series/DataFrame, výběr na obou osách loc/iloc, bool masky (&/|/~ a isin), stabilní sort_values/více klíčů/NaN/reset_index a nové sloupce či cílené změny přes loc v pandas 3. Každá nová lekce má tři přepínatelné ukázky a pět úkolů s vlastním zadáním, kontrolou a možným řešením. Kurz nyní 10/42, 30 ukázek a 50 úkolů; celá aplikace 178 hlavních + 176 doplňkových řešení = 354. Všechny nové příkazy se vysvětlují před použitím. Závislosti zůstávají stejné, stačí dosavadní pandas>=3,<4 v projektové .venv. Ověřeno na Pythonu 3.14.8/pandas 3.1.1/NumPy 2.5.4.

Nových osm skupin test_pandas_selection odmítá 38 chybných variant a přijímá 25 správných alternativ všech 25 úkolů. Kontrolují i zachování vstupní tabulky/masky, přiřazení podle popisků, stabilní shody, NaN a samotný Copy-on-Write ve skutečném pandas. Stabilitu prověřují také 40prvkové vstupy; krátký příklad může náhodou dát stejné pořadí i s nestabilním algoritmem. Všech 25 solution.py se spouští také samostatně. Nové ukázky nepotřebují pomocné soubory ani síť. Volitelný pandas_tools.py se neměnil, základní checker se dál obejde bez importu pandas.

E2e_pandas_selection prošlo všech 15 nových ukázek, 25 šablon/řešení i samostatných běhů, workspace, přesné odkrytí vzoru, drafty, procvičení, reload a mobil. Kód/splnění předchozí lekce CSV zůstaly zachované. Prošly regrese e2e_pandas_intro (první modul) a e2e_solutions (138 ostatních lekcí). Skutečné ipykernel provedlo všech 30 ukázek prvních dvou modulů po buňkách v čistém jmenném prostoru. Nativní VS Code/VSCodium/PyCharm tím nejsou otestované. Celkový validátor: 193 lekcí, 0 chyb a upozornění; výsledek celé unittest sady v posledním STATUS.md. Snímky/protokoly mimo repo v /workspace/scratch/pandas-selection-work.

Další blok 11–15: isna/fillna/dropna, převody čísel a datových typů, to_datetime, duplicity a čištění textů. Nadále více ukázek/úkolů a možná řešení u samostatných témat; navazující projekty tvoří celek. Zachovat starší ID a postup. Dodávka commit/push do main bez ZIPů a publikace cloudového prostředí. Historické pokyny níže nejsou aktuálním zadáním.

## Aktuální v0.59 (8. 11. 2026): Datová analýza 5/42

Uživatel výslovně zahájil Datovou analýzu s více příklady/procvičováním a možnými řešeními od začátku. Tím pro pandas nahrazuje starší pokyn nezačínat nový kurz automaticky. Hotovo prvních pět lekcí: Series/popisky, výpočty/zarovnání, loc/iloc, DataFrame a místní CSV. Každá má tři přepínatelné ukázky a pět úkolů s kontrolou a možným řešením. Celkem 15 ukázek/25 úkolů; v celé aplikaci 173 hlavních + 156 doplňkových řešení = 329. Kurz je draft s úplnou osnovou 42 lekcí v plan.md/panelu; další témata zatím nejsou dostupná. Úvod 2/4, celek 3/4.

Příprava nabízí tři editory. Obyčejné .py s # %% běží v prohlížeči/terminálu; notebook je volitelný. Ověřeno Python 3.14.8, pandas 3.1.1, NumPy 2.5.4. Instalace obsahuje i matplotlib 3.11.2/openpyxl 3.1.5/ipykernel 7.4.0 pro další části. Setup_env a course.json vyžadují pandas>=3,<4. Nové vlastní UTF-8 CSV jsou v files/ a také u jednotlivých doplňkových úkolů: ty kořenové soubory automaticky nedědí. Nový volitelný lib/dilna_check/pandas_tools.py porovnává dtype, jména, popisky, pořadí, NaN a přesné zachování vstupů/souborů. Neimportovat globálně do základního checkeru. Prázdný výsledný index bez popisků toleruje rozdíl odvozeného typu, dtype hodnot a jména zůstávají kontrolované.

Testy přijímají 25 správných alternativ a odmítají 31 chybných variant. Odhalily a opravily zaokrouhlování, záměnu sort_values/sort_index a příliš přísný typ prázdného indexu. Chromium ověřilo 15 skutečných ukázek a 25 šablon/řešení, odkrytí správného vzoru, CSV/workspace, reload, drafty/postup a mobil. Skutečný ipykernel provedl všech 15 ukázek po buňkách; nativní VS Code/VSCodium/PyCharm tím nejsou ověřené. Regrese solutions (133 ostatních lekcí), preparation (10 profilů) a progress (6 skupin) prošly. Kompletní výsledek sady/validátoru viz nejnovější STATUS.md. Protokoly a snímky jsou mimo repo v /workspace/scratch/pandas-start-work.

Další krok pandas 6–10: sloupce, tabulkové loc/iloc, masky, sort_values a cílené změny přes loc/Copy-on-Write. Zachovat více ukázek/úkolů a řešení u samostatných témat; navazující projekty nerozdělovat na nesouvisející varianty. ID ani postup starších kurzů se nemění. Dodávka přes commit/push do main, bez ZIPů a publikace prostředí. Historické pokyny níže neposuzovat jako aktuální zadání.

> **Aktuální v0.58 (8. 11. 2026):** Uživatel výslovně vybral revizi a vylepšení hotové aplikace. Opraveno přepisování postupu starým snímkem z jiné karty: store.js před každým zápisem čte poslední stav, reaguje na storage a zachovává původní dilna-python-v1. Normalizace přijímá platné položky done/tasks/checks/theme, ignoruje vadné typy a ponechá neznámá pole kořene; čtení samo uložený text nepřepisuje. Mapy mají nulový prototyp. Při odmítnutém zápisu drží vlastní operace v paměti a zkusí je uložit při další změně postupu; při opakování je aplikuje nad novými daty ostatních karet. App.js bez překreslení editoru aktualizuje vzhled a oznámení storage-warning s role=status, které po úspěchu zmizí. Nová zkouška reprodukovala původní ztrátu první lekce po druhém označení v jiné kartě a pád přehledu při done:null; obojí opraveno. Také renderPreparation zachytí chybu načtení uvnitř svého panelu a nabídne nový pokus, takže HTTP 503/404 nepřepíše celý kurz chybovou stránkou. Osm prohlížečových skriptů prošlo: nový e2e_progress se šesti skupinami (dvě karty, opožděná oznámení, poškozená data, kvóta/obnovení, nepřístupné úložiště, vymazání) a web/lesson/tasks/preparation/setup/editor/solutions. Ověřeno také zachování kódu, kurzoru, checklistů, procvičení a všech 128 nových panelů řešení. Dva starší testy používají dostupné systémové Chromium místo povinné cache Playwrightu. Snímky mobilních hlášek prohlédnuty, mimo repo v /workspace/scratch/progress-review. Python ani obsah lekcí a 304 vzorů se nemění, nic dalšího se neinstaluje. Po git pull obnovit otevřené karty, aby nemíchaly staré a opravené ukládání. Další práce jsou revize dle uživatele; jiný kurz nyní neotevírat. Dodávka přes GitHub/main bez ZIPů a publikace prostředí.

> **Aktuální v0.57 (8. 11. 2026):** Na žádost uživatele je panel „Zobrazit možné řešení“ zpřístupněn ve všech šesti praktických kurzech, nejen Základech: všech 168 hlavních zadání + 136 doplňkových, celkem 304 vzorů. Nové vzorové soubory nebylo potřeba tvořit; odstraněno omezení cid==zaklady v server/content.py pro has_solution a solution_view. Stávající frontend je obecný a zůstává beze změny: kód se načte až po rozbalení, je pouze pro čtení, jeden možný postup, přepnutí úkolu či reload panel skryje. Nic se nevkládá do editoru a nemění se postup. Průvodci přípravy ani plánované kurzy nemají programový vzor a panel se nezobrazuje. Zachované lesson_dir a Host/Origin kontroly, prázdný/chybějící vzor nebo neplatná volba vracejí 404. Pět unit skupin ověřuje dostupnost, shodu všech 304 souborů, HTTP napříč všemi kurzy, chyby/guardy a čtení bez zápisu workspace. Celá unittest sada: 218 testů OK bez přeskočených (326 s). Chromium e2e_solutions.py prošlo všech 128 nově zpřístupněných lekcí i starší varianty Úkol 1–5, s přesným obsahem, nezměněným localStorage před/po odkrytí, chybou/zpožděním, přechodem mezi kurzy, klávesnicí a mobilem. Všech sedm e2e_tkinter bloků bylo upraveno na přítomný skrytý panel a prošlo. Obsah lekcí a vzory se nemění. Snímky mimo repo v /workspace/scratch/all-solutions-work, panel prohlédnut na desktopu i mobilu. Další práce podle připomínek uživatele; tkinter-api dál obsahově 28/28, draft. Dodávka přes GitHub/main bez ZIPů a publikace prostředí, zachovat ID a studentský postup. Přesné výsledky v posledním STATUS.md.

> **Aktuální v0.56 (8. 11. 2026):** Celý tkinter-api je obsahově hotový, 28/28, dál draft pro vyzkoušení studenty, obtížnost 3/4. M07: 25 pět vlastních unittest scénářů nad modelem/pracovníkem, kontrola je zkouší proti osmi dočasným chybám; 26 čistý plán argumentů pro volitelné balení bez automatické instalace/stavby; 27 data podle __file__, uživatelské dialogy a Ctrl+S/O/Enter s vlastní vazbou i na Text; 28 konzolová zkouška jednoho skutečného SMTP předání a kompletní projekt ve files. Finální okno je aplikace.py, jsou přiloženy test_projekt.py, README, SCENARE, requirements, ukázkový koncept, baleni.py a sestavit.py. Souhrn čte skutečně přijatou obálku/MIME, nejistý stav je chyba i při zprávě již v záchytu, žádný retry. Tk_run má novou akci focus s kind/name; jeho omezená náhrada třídní vazby Text neprovádí, proto se zkouší skutečné Tk. Test hlídá 39 nových pomocných kopií dřívějších řešení/shared, při změně zdroje aktualizovat návaznosti. Kontroly odmítly 32 chybných a přijaly 12 správných alternativ. Celá unittest sada: 218 testů OK bez přeskočených (324 s); validátor všech 183 lekcí bez chyb/upozornění, Chromium nové i předchozí projektové lekce a zachování postupu. Skutečný Tk 9.0/Python 3.14.8/Linux ověřil finální okna 27/28, Ctrl z těla, chyby zdroje, jiné cwd, původní snímek a nejistý přenos. PyPI potvrdilo podporu 3.14 u PyInstalleru 6.22.3, nainstalován v uživatelské .venv a skutečně sestaven. Spuštěný linuxový balíček z /tmp načetl přibalené data a přes tlačítko předal jednu zprávu místnímu záchytu. Vlastní sestavit.py ve 28 navíc ověřen s kopiemi README/SCENARE do výsledku. Balíčky jsou pouze ve scratch, do Gitu patří zdroj a návody, žádný ZIP či publikace prostředí. Windows/macOS a jejich balíčky nově neověřeny. Další doporučený krok je revize a připomínky k hotovému kurzu; jiný podkurz nezačínat automaticky. Zachovat starší ID a postup. Dodávka přes GitHub/main; externí zprávy pouze na výslovné zadání. Přesné výsledky v posledním STATUS.md.

> **Aktuální v0.55 (8. 11. 2026):** Tkinter-api má hotový m06, celkem 24/28, draft a obtížnost 3/4. Projekt Korespondenční dílna: 21 nový čtyřpoložkový koncept zachovávající neúplný text, 22 ChybaPole a sestavení zprávy s konkrétním polem/fokusem, 23 přenos hotového snímku v pracovníkovi, 24 uložený koncept JSON. Během SMTP lze dál psát, dokončení novou práci nepřepíše. EmailMessage obsahuje předem načtené bytes přílohy; po předání ji aplikace nemění (není to neměnný datový typ). Při nejistém výsledku další pokus vyžaduje ruční kontrolu záchytu; načtení jiného konceptu tuto podmínku nemaže. JSON verze 1 je skutečný int bez bool, obsahuje čtyři původní texty a pouze nativní absolutní cestu přílohy; ne její obsah, nastavení či stav SMTP. Neexistující příloha ani nedopsaná adresa nebrání uložení/načtení. Uloz_koncept používá zavřený dočasný soubor ve stejné složce, os.replace a úklid; chyba před nahrazením zachová starší cíl. Nacti_koncept ověří vše před změnou formuláře, zrušení/chyba zachová pole/přílohu/náhled. Tk_run nově vybírá fill/fill_text přes volitelné name z konstruktoru widgetu; bez něj platí stará jednoznačnost, read-only stav zůstává. Shodu 18 pomocných kopií hlídá test, detaily v SCHEMA.md. Nové kontroly odmítly 31 chybných a přijaly 12 správných alternativ; celá unittest sada 210 testů OK bez přeskočených (303 s). Skutečný Tk 9.0/Python 3.14.8/Linux ověřil všechna čtyři okna, SMTP obsah při změně formuláře/souboru, odmítnutí i nejistý výsledek v 23/24. Chromium ověřil nové lekce, původní SMTP a zachování kódu/postupu; validátor všech 179 lekcí bez chyb/upozornění. Další dávka 25–28: vlastní testy modelu/spolupráce/GUI, cesty a předání, volitelný PyInstaller až po ověření podpory Pythonu 3.14.8 a cílového OS. Windows/macOS nově neověřeny. Zachovat ID a postup; dodávka přes GitHub/main bez ZIPů a publikace prostředí. Externí zprávy jen na výslovné zadání uživatele. Přesné výsledky viz poslední STATUS.md.

> **Aktuální v0.54 (8. 11. 2026):** Tkinter-api má hotový m05, celkem 20/28, draft a náročnost 3/4. Lekce 17: EmailMessage, ověření jedné ASCII adresy, české tělo, hlavičky, MIME a dekódovaný náhled bez přenosu. Lekce 18: SMTP pouze do 127.0.0.1, timeout a obálka proti hlavičkám; skutečný místní záchyt bez přeposílání. Lekce 19: binární příloha do 1 000 000 B, MIME a jméno souboru; nový výběr nahradí předchozí přílohu, zrušení/chyba zachová zprávu. Lekce 20: konfigurace z prostředí, Thread/Queue/after bez Tk v pracovníkovi, odmítnutí a nejisté potvrzení. Záchyt může zprávu uložit před timeoutem klienta: kontrola před ručním opakováním, žádný automatický retry. Od 18 potřeba aiosmtpd>=1.4.6,<2; 1.4.6 skutečně ověřeno na Pythonu 3.14.8. Python 3.14 nemá smtpd. Helper shared/cvicna_posta.py má dvě přesné kopie; _Controller._trigger_server řeší port=0 přes neveřejný bod knihovny, při upgradu ověřit skutečný start/přenos/stop. Zpravy.py ve files 18–20 a odesilani.py ve 20 jsou přesné kopie řešení 17/18, všech šest kopií hlídá test. Tk_run extra_env mění pouze podproces; běžný runner DILNA_SMTP_* nepředává, pokusy s nimi spouštět přímo v terminálu/editoru a po změně restartovat program. Ověřeno 29 chybných a 12 správných alternativ, 202 unit testů, validátor 175 lekcí bez chyb/upozornění. Chromium ověřil 17–20, původní API blok i zachování kódu/postupu. Skutečný Tk 9.0/Linux ověřil obě okna, souborové chyby i skutečné SMTP, odezvu, odmítnutí a timeout s již zachycenou zprávou; Windows/macOS neověřeny. Další dávka 21–24: Korespondenční dílna, model konceptu, validace a náhled, snímek zprávy pro pracovníka, uložení/načtení bez ztráty konceptu při chybě. Žádné externí zprávy bez výslovného zadání uživatele. Zachovat ID a postup; dodávka přes GitHub/main bez ZIPů a publikace prostředí. Podrobnosti v posledním STATUS.md a courses/SCHEMA.md.

> **Aktuální v0.53 (8. 11. 2026):** Tkinter-api má hotový m04, celkem 16/28, draft. Lekce 13/14 jsou konzolový backend: requests GET/params/timeout/raise_for_status/JSON a over_kurz s měnou, konečným kladným číslem bez bool, přesným kalendářním datem a zdrojem. Vrací nový slovník, příliš velký int překládá na ValueError. Lekce 15/16 jsou GUI: skutečný pracovník/Queue/after, veškeré Tk jen v hlavním vlákně, disabled po dobu načítání, nový pokus po chybě. Převodník měn má dva explicitně smyšlené místní zdroje: API EUR25/USD20 dne 2026-01-15, JSON EUR24/USD19 dne 2026-01-14. Vždy zobrazuje zdroj a datum, změna volby i neúspěšné načtení zneplatní kurz, částku zachová. Cvicne_api.py je ve shared a čtyřech přesných kopiích files, kurzy.py v 15/16 je kopie řešení 14. Místní helper dočasně doplní pouze loopback do NO_PROXY/no_proxy a vrátí původní hodnoty; bez této výjimky cloud posílal i 127.0.0.1 do proxy a vracel 403. Od 13 je potřeba requests. Tk_run nyní umí after/cancel, omezené čekání na stav, skutečná vlákna a měření callbacků; odmítá i zachycený přístup k Tk z pracovníka. Volitelné řízené HTTP pro GUI vrací reálné requests.Response, skutečný backend se testuje zvlášť místním HTTP. Ověřeno 35 chybných a 12 správných alternativ, 195 unit testů, validátor 171 lekcí bez chyb/upozornění, Chromium nové lekce i předchozí úkolníček. Skutečné Tk 9.0/Python 3.14.8/Linux ověřilo obě nová okna včetně odezvy při reálném pomalém HTTP, zdrojů, chyby 503 a nového pokusu; Windows/macOS nově neověřeny. Další dávka 17–20: EmailMessage/náhled, SMTP jen do místního záchytu, přílohy a zrušený dialog, nastavení služby a chyby. Python 3.14 nemá smtpd: ověřit pomocnou závislost nebo vlastní omezený testovací záchyt. Žádnou externí zprávu neposílat bez výslovného zadání uživatele. Zachovat ID i postup, dodávka přes GitHub/main bez ZIPů a publikace prostředí. Podrobnosti v posledním STATUS.md.

> **Aktuální v0.52 (7. 11. 2026):** Tkinter-api má dokončený m03, celkem 12/28, draft. Lekce 9–12: Listbox a oddělený model, mazání podle indexu i mezi stejnými názvy; Text s end-1c, počty a obousměrným Scrollbar; poznámka v JSON s dialogy a UTF-8; projekt úkolníčku. Model 12 je seznam {nazev:str, hotovo:bool}, startuje prázdný; dokončení nastavuje True, odstranění používá index. Listbox obsahuje jen zobrazené značky [ ]/[hotovo], neukládat je do názvů. Text detailu je disabled a aktualizuje se po <<ListboxSelect>> i výslovně po obnovení výběru. Souborové funkce jsou importovatelné bez okna. Nacti_ukoly ověří všechny záznamy před změnou stavu; prázdný seznam je platný, opakované názvy zachová, extra klíče může ignorovat. Načtení nahrazuje přes ukoly[:], zrušení/chyba zachová model, výběr i detail. Jednoduchý přímý zápis JSON nezaručuje obnovu předchozího souboru po přerušení; v lekci vysvětleno. Tk_run rozšířen o Listbox, Text, Scrollbar, řádky mřížky, select/fill_text/scroll a frontu odpovědí filedialog. Není to plné Tk ani pixelové posouvání; nepodporované funkce doplnit před další lekcí. Skutečný Tk 9.0/Python 3.14.8/Linux ověřil všech dvanáct ukázek, výběr, posuvníky, souborové operace a zachování stavu při chybě; volba souboru v reálném GUI testu je řízená testem, vzhled nativního dialogu se neověřoval. Chromium ověřil všechny tři bloky a zachování Tk/OOP postupu. Úplné výsledky v posledním STATUS.md. Další dávka 13–16: místní REST API/requests, stavové kódy a chyby, after/worker/fronta bez změn widgetů mimo hlavní vlákno, převodník měn 2.0. Před kontrolami rozšířit Tk běh o plánování událostí a předvídatelné místní síťové scénáře. API/e-maily zatím nejsou realizované, nic se neodesílá externě. Zachovat ID i postup, dodávat přes GitHub/main bez ZIPů a publikace prostředí.

> **Aktuální v0.51 (7. 11. 2026):** Kurz tkinter-api má hotové m01 a m02, celkem 8/28, draft. Nové lekce 5–8: Frame a roztažení vstupu přes více rodičů, Enter/bind/focus s nepovinným argumentem události, IntVar/Checkbutton a společná StringVar/Radiobutton, projekt převodníku kilometrů a metrů. V 8 je modulová funkce preved_vzdalenost(hodnota, smer), směry km-m/m-km, číslo bez zaokrouhlení; odmítá záporné, NaN/inf, přetečení a neznámý směr přes ValueError. Okno vzniká jen ve funkci hlavni volané z hlavního bloku. Callback přijímá desetinnou čárku/tečku, zobrazuje .3f s jednotkou a po chybě dovolí opravu bez ztráty vstupu. Tk_run rozšířen o Frame columns, fokus, bind/widget+root pro Return, Checkbutton/Radiobutton a selected. Není to celé Tk, třídní vazby ani vykreslování. Calls s run_name=student dovolují ověřit oddělený výpočet bez spuštění hlavního bloku; výsledky jsou JSON value/error. Nové kontroly odmítají 34 chybných a přijímají 12 správných alternativ. Skutečný Tk 9.0/Python 3.14.8/Linux ověřil všech osm ukázek, klávesnici i opravy po chybách. Chromium ověřil nové i první čtyři lekce, pracovní soubory, mobil a zachování staršího Tk/OOP postupu. Úplné výsledky v posledním STATUS.md. Další dávka 9–12: Listbox s modelem dat, Scrollbar/Text, JSON a zrušitelné dialogy, projekt úkolníčku. Před kontrolami doplnit náhradu Tk a ověřit skutečné widgety. API/e-maily jsou dál plánované. Zachovat ID a postup všech kurzů, dodávat přes GitHub/main, bez ZIPů a publikace prostředí.

> **Aktuální v0.50 (7. 11. 2026):** Uživatel výslovně vybral „Okenní aplikace, API a e-maily“. Kurz tkinter-api má první čtyři lekce m01: hlavní okno a mainloop, Label a pack, Button a callback, Entry a grid. Celkem 4/28, draft, obtížnost celku 3/4; úplný plán je v courses/tkinter-api/plan.md i panelu kurzu. Každá lekce má výklad příkazů před použitím, komentovanou ukázku, šablonu, řešení, kontrolu chování a tři kvízové otázky. Příprava vysvětluje ověření Tk ve stejné .venv a umístění skutečného okna na počítači s Pythonem. První blok používá jen tkinter/ttk, requests přijde později. Nový c.tk_run spustí omezenou náhradu Tkinteru v podprocesu, zachytí widgety a provede kliknutí/vyplnění; c.tk_no_error popíše chybu. Nejde o celé Tk: před lekcemi 5–8 doplnit potřebné metody a ověřit proti skutečnému Tk. Validátor nyní Tk ukázky provede místo pouhé kompilace. Ověřeno 32 chybných a 12 správných alternativ, 163 unit testů, validátor 159 lekcí bez chyb/upozornění, Chromium nové lekce a regrese řešení/plánu/katalogu. Skutečný Tk 9.0 na Pythonu 3.14.8/Linux ověřil všechny čtyři ukázky, tlačítka, vstup a roztažení formuláře; Windows/macOS nově netestovány. Další dávka 5–8: Frame/rozměry, bind/Enter/focus, proměnné a volby, převodník jednotek. API a e-maily jsou zatím plánované, později testovat místně. Zachovat starší ID i postup. Pracovat v /workspace/Python-Academy, dodávat přes GitHub/main, bez ZIPů a bez publikace prostředí.

> **Aktuální v0.49 (7. 11. 2026):** Uživatel přešel k úpravám Základů. Nový panel „Zobrazit možné řešení“ pod úkolem zpřístupní existující solution.py právě vybraného zadání, 40 hlavních + 136 doplňkových úkolů, včetně projektů a závěrečného programu. Označeno jako jeden možný postup, syntaxe zvýrazněná a kód pouze k prohlížení. API lesson má has_solution; nový čtecí GET /api/solution je omezen na zaklady, validuje lekci/task a vrací code až na žádost. Kontroly ani řešení se do původního obsahu zadání nevkládají. Panel se při přepnutí zavře, vymaže starý obsah a odmítá opožděné odpovědi; načtení se opakuje po chybě. Rozepsaný kód, příklady, značky splnění a uložený postup se nemění. Web/js/solutions.js nemá zápisy do store/editoru. Testy ověřují všech 176 zdrojů, API, chyby/zpoždění, klávesnici, mobil i zachování práce a postupů. Dodatečná revize opravila počty banan v lekcích 19/37, shodu hranice 0 v lekci 4, typy výsledků řetězcových metod v 10, return/tuple v 16 a české řazení v 20. Ověřeno 40 hlavních a 68 dalších ukázek, 64 úryvků výkladu s potřebným kontextem a validátor 40 lekcí bez chyb. Přesné výsledky v posledním STATUS.md. OOP má dál 20/20 a Turtle/OOP 40/40. Další práce podle připomínek uživatele k Základům. Dodávat přes GitHub/main, bez ZIPů a bez publikace prostředí.

> **Aktuální v0.48 (7. 11. 2026):** Samostatný oop je obsahově dokončený, 20/20, status draft pro revizi a zpětnou vazbu. M05 (17–20) propojí NakupniObjednavka, RezervacniSklad, ExpedicniCentrum a konzolový ovladač. Nákup skládá starší Objednavka/Polozka, agreguje kódy, vrací kopii požadavku a po rezervaci se uzavře. Sklad dědí původní Sklad, eviduje kopii množství podle čísla a rezervovana/stornovana; storno vrací jen vlastní kusy jednou, jiné a anonymní rezervace ponechá. Centrum ověří dopravu před skladem, uloží záznam až po úspěchu a deleguje dopravu/poznámky/storno; souhrn je kopie včetně poznámek. Cyklodoprava potřebuje zónu a oceňuje do 2000 g včetně za 59 Kč. Konzole 20: stav, nova ČÍSLO KNIHY OBALY GRAMY, prehled, doprava odber/kuryr/kolo, poznamka, storno, konec. Cvičně 5 knih/2 obaly, 250/30 Kč, nové spuštění obnoví paměť. Ve workspace jsou všechny moduly, README a test_centrum.py se čtyřmi testy. Lekce 20 má run_timeout 600 s pro ukázku i vlastní kód; API normalizuje volitelný limit 1–600, výchozí konzole 20/GUI 600. Ověřeno 37 chybných a 12 správných alternativ; přesné výsledky v posledním STATUS.md. Shodu 32 pomocných kopií hlídá test, při změně staršího rozhraní aktualizovat návaznosti. Původní Turtle/OOP má 40 lekcí, nic se nepřesouvá. Další doporučený krok: revize dokončeného OOP a zpětná vazba, nový kurz nezačínat automaticky. Pracovat v `/workspace/Python-Academy`, dodávat přes GitHub/main bez ZIPů a bez publikace cloudového prostředí.

> **Aktuální v0.47 (7. 11. 2026):** Samostatný oop má hotový m04, lekce 13–16, celkem 16/20, draft. PopsanyBalik dědí z původního Balik, str deleguje na popis a repr zachovává kód včetně uvozovek/úniků. Adresa(ulice, mesto, psc) má shodu všech tří původních textů stejného konkrétního typu; pro jiný typ __eq__ vrací NotImplemented (nikoli výjimku). ExpedicniStitek je dataclass s poli kod/adresa/poznamky, default_factory vytváří vlastní seznam; výslovně předaný seznam a adresa zůstávají původními odkazy. Pridej_poznamku zachová pořadí/duplicity a vrátí počet. Lekce 16 učí alespoň čtyři vlastní unittest testy TestExpedice nad skutečnými moduly z 9–12: odběr, cenové hranice, úspěšnou a odmítnutou změnu. Kontrola je spustí nad správným modelem i osmi záměrnými chybami; prázdné či vynechané ověřování nestačí. Připravený hlavní blok používá unittest.main(verbosity=2), běžný výstup unittest na stderr je ve výkladu vysvětlený. Pomocné moduly jsou přesné kopie dřívějších řešení, shodu hlídá test. Ověřeno 36 chybných a 13 správných alternativ; úplné výsledky v posledním STATUS.md. Dál 17–20, závěrečný projekt: vlastnictví rezervací, bezpečné storno, doprava a konzolový ovladač s testy. Zachovat rozhraní i ID starších lekcí. Turtle/OOP má dál 40 lekcí. Pracovat v `/workspace/Python-Academy`, dodávat přes GitHub/main bez ZIPů.

> **Aktuální v0.46 (7. 11. 2026):** Samostatný oop má hotový m03, lekce 9–12, celkem 12/20, draft. Balik/KrehkyBalik učí dědění bez kopírování metod. Doprava, OsobniOdber a Kuryr přepisují cena(balik); ceny_dopravy zachová pořadí/duplicity a používá společné rozhraní. Odběr potřebuje místo a stojí 0; kurýr adresu, limit standardně 10000 g a sazbu 99 do 5000 g včetně / 149 nad ni. ExpresniKuryr přes super inicializuje stejný objekt a rozšíří skutečnou základní cenu; přidá termín dopoledne/odpoledne, příplatek standardně 50 a limit 5000 g. Expedice skládá původní balík a dopravu, nabídku zjišťuje aktuálně a změnu uloží až po ověření nové ceny. Odmítnutí zachová původní volbu; funguje i nová doprava bez společného předka. Nabídky nic neodesílají, nerezervují ani nemění spolupracovníky. Pomocné balik.py/doprava.py/expres.py jsou kopie předchozích řešení a shodu hlídá test. Ověřeno 39 chybných a 11 správných alternativ; úplné výsledky v posledním STATUS.md. Dál oop 13–16: __str__/__repr__, identita/rovnost, dataclass a unittest. Vlastnictví rezervací a storno zůstává pro projekt 17–20. Turtle/OOP má dál 40 lekcí. Pracovat v `/workspace/Python-Academy`, dodávat přes GitHub/main bez ZIPů.

> **Aktuální v0.45 (7. 11. 2026):** Samostatný oop pokračuje m02, lekce 5–8: zapouzdření/rozhraní, pravidla stavu před změnou, property a dostupnost, revize skladu s úplnou rezervací. Celkem 8/20, status draft. Lekce 5 pracuje s platnými operacemi, 6 přidá validaci, 7 rozliší fyzické/rezervované/dostupné kusy a 8 ověří celý slovníkový požadavek před první rezervací. Vstupy počtů jsou skutečný int; bool se odmítá tam, kde je validace. Přehled skladu je nový slovník čísel, ne interní karty. Pomocný skladova_karta.py je přesná kopie řešení 7. Kontroly přijímají jiné názvy privátních údajů i pořadí slovníků a ověřují veřejné rozhraní karet. Ověřeno 33 chybných a 10 správných alternativ, nové i původní lekce v prohlížeči a mobilní panel; úplné výsledky v posledním STATUS.md. Dál oop 9–12: dědění, polymorfismus, super a doprava jako spolupráce. Turtle/OOP zůstává dokončený se 40 lekcemi. Pracovat v `/workspace/Python-Academy`, dodávat přes GitHub/main bez ZIPů.

> **Aktuální v0.44 (5. 11. 2026):** Uživatel nově požádal „pokračujme s lekcí OOP“. To autorizuje realizaci dříve pouze navrženého samostatného `oop`; zákaz implementace v historických záznamech níže je překonaný. Hotové lekce 1–4 v m01: první instance zásilky, konstruktor položky, metody a průběh volání, objednávka s položkami/referencemi/kopií přehledu. Celkem 4/20, status draft, obtížnost celku 3/4, začátek 2/4. Panel už neoznačuje kurz za nerealizovaný koncept a zobrazuje 4 z 20 připravených lekcí; celá osnova zůstává dostupná. Dosavadní Turtle/OOP má dál 40 lekcí a obsah se nepřesouvá. Ověřeno 29 chybných a 9 správných alternativ, Chromium včetně odděleného uloženého postupu a mobilního panelu. Úplné výsledky v posledním STATUS.md. Dál samostatné OOP 5–8 podle courses/oop/plan.md, nikoli další rozšíření Turtle. Pracovat v `/workspace/Python-Academy`, dodávat GitHub/main bez ZIPů.

> **Aktuální v0.43 (5. 11. 2026):** Původní Turtle/OOP je obsahově dokončen, 40/40 lekcí. Nový m08 (37–40) má dataclass Otazka/model Kviz, validaci JSON a HTML entit, urllib klienta s offline zálohou a hotový konzolový kvíz. Ukázka lekce 40: Enter pro česká offline data, a/n odpovědi, q konec; api výslovně volí anglickou Open Trivia DB. Ukázka 39 simuluje úspěch/výpadek lokálními daty. Kontroly používají náhrady síťového přenosu a místní HTTP server, nikoli veřejný internet. Ověřeno 35 chybných a 8 správných alternativ; Chromium potvrdil skutečný konzolový vstup 5/5 i předčasný konec a zachování postupu. Úplné výsledky v posledním STATUS.md. Samostatný oop zůstává pouze konceptem. Další doporučený krok: obsahová revize dokončeného kurzu a zpětná vazba; další podkurz se v tomto kroku nezačal. Dodávky GitHub/main, bez ZIPů, pracovní kořen `/workspace/Python-Academy`.

> **Aktuální v0.42 (5. 11. 2026):** Dokončen m07, lekce 33–36: potrava/růst, kolize s tělem, skóre/stav Partie a hotový Snake s restartem Enter. Kurz má 36/40 lekcí, projekt Snake je hratelný v ukázce lekce 36. Zachovány průchozí okraje, jedna čekající zatáčka a jediný řetězec pohybu. Restart zvyšuje generaci a staré callbacky ignoruje; po update se navíc kontroluje, zda během překreslení nenastal další restart. Pomocné soubory navazují na vzorová řešení a jejich shodu hlídá test_snake_finish.py. Ověřeno 40 chybných a 9 správných alternativ, Chromium a skutečné Tk/Turtle se sběrem, skóre, prohrou, výhrou a opakovaným Enter. Úplné výsledky v posledním STATUS.md. Dál lekce 37–40: kvíz/API s offline daty, nikoli další rozšiřování Snake. Samostatný oop zůstává pouze konceptem. Pracovat v `/workspace/Python-Academy`, doručovat přes GitHub/main, bez ZIPů.

> **Aktuální v0.41 (5. 11. 2026):** Na pokračování uživatele vznikl m06 původního Turtle/OOP, lekce 29–32: model Snake, zobrazení, časovač a šipky. Celkem 32/40 lekcí. Průchozí okraje jsou záměrné pravidlo, nikoli budoucí kolize se stěnou; dosud bez potravy/růstu/kolize s tělem/skóre/restartu. Další dávka 33–36 tyto části doplní; 37–40 patří kvízu/API. Pomocné moduly ve files/ jsou přesné kopie předchozích vzorových řešení, jejich shodu hlídá test_snake_start.py. Při další změně rozhraní je nutné aktualizovat navazující soubory. Ověřeno 39 chybných a 10 správných alternativ, Chromium a skutečné Tk/Turtle včetně časovačů a kláves; úplné výsledky v posledním STATUS.md. Samostatný kurz `oop` zůstává pouze konceptem. Dodávky přes GitHub/main, bez ZIPů, pracovní kořen `/workspace/Python-Academy`.

> **Aktuální v0.40:** Na uživatelovo „pokračuj“ dokončen m05 původního Turtle/OOP, lekce 25–28: speciální metody, identita/rovnost, MRO a dataclass. Kurz má 28/40 lekcí. Nový samostatný `oop` nadále pouze koncept — nepřesouvat do něj dosavadní obsah a neimplementovat ho bez nového zadání. Další blok původního kurzu je Snake (orientačně 29–36), pak kvíz/API (37–40); pracovat po dávkách přibližně čtyř lekcí. Nové kontroly zkouší 35 chybných a 8 správných alternativ, v prohlížeči ověřeny ukázky, řešení i zachování kódu a postupu. Úplné výsledky jsou v posledním STATUS.md. Pracovat v `/workspace/Python-Academy`, dodávat přes GitHub/main, bez ZIPů.

> **Aktuální v0.39:** Původní Turtle/OOP pokračuje lekcemi 21–24 (pravidla stavu, property, dědění, super), celkem 24/40. Nově je v katalogu **samostatný koncept OOP** s id `oop`, plán 20 lekcí a obtížnost 3/4, nezávislý na Turtle a hrách. Praktické téma je Chytré expediční centrum, text v courses/oop/plan.md, panel zatím bez výukové implementace. Uživatel výslovně upřesnil: stávající OOP lekce ponechat a nový kurz pouze navrhnout. Nepřesouvat dosavadní obsah a nový koncept zatím neimplementovat. Pracovat v `/workspace/Python-Academy`, změny doručovat přes GitHub/main, bez ZIPů. Ověřeno: 101 testů OK, validátor 119 lekcí bez chyb a 4 prohlížečové testy OK. Viz poslední STATUS.md.


> **Aktuální v0.38:** Uživatel obnovil pokračování Turtle/OOP/Snake. Nový modul m03 má lekce 17–20 (instance, konstruktor, metody/stav, vlastní seznamy), celkem 20/40 lekcí kurzu. Další dávka: zapouzdření a dědění/super(); Snake zatím nevznikl. Obsahové názvy prvních ukázek jsou v example_title místo tlačítka „Původní ukázka“, id original zůstává. Doplněna ICO favicona vedle SVG a verze odkazů. Ověřeno: 95 testů OK, validátor 115 lekcí bez chyb, prohlížečové testy OOP a ukázek OK. Viz poslední STATUS.md. Pracovat v `/workspace/Python-Academy`, změny doručovat přes GitHub/main, nevytvářet ZIPy. Historický zákaz pokračování tohoto kurzu níže je překonán nynějším zadáním; jiné kurzy zůstávají mimo rozsah.


> **Aktuální v0.37:** Uživatel chce odteď verzovat přímo v GitHubu a nevyžaduje další ZIPy. Ve 34 běžných lekcích Základů doplněny čtyři nové úkoly (136 celkem), přepínání Úkol 1–5 s vlastními zadáními, kontrolami, drafty a pracovními soubory. Původní úkoly i jejich uložená data zůstaly zachované. Značky procvičení jsou samostatné. Viz poslední STATUS.md, courses/SCHEMA.md a nový modul web/js/tasks.js. Používejte `/workspace/Python-Academy`. Nové změny určené uživateli commitovat a pushnout do main podle jeho autorizace. Původní obsahový plán je pozastaven; neprovádět historické pokyny k ZIPům níže bez nové žádosti.


> **Git repozitář:** Projekt v0.36 je nyní vložen přímo do kořene `Liborias/Python-Academy`. V cloudu používejte existující checkout `/workspace/Python-Academy`; starší cesty do rozbalených ZIPů níže jsou historické. Změny určené pro místní `git pull` je potřeba commitnout a odeslat do tohoto repozitáře; publikace cloudového prostředí je jiný krok. Uživatel nyní výslovně autorizoval první nahrání aplikace na GitHub. Návod pro lokální kopii a korektury je v `docs/lokalni-projekt-git.md`.


> **Aktuální v0.36:** Na schválení uživatele doplněna vysvětlení příkazů ve všech původních průvodcích přípravy a nová devátá lekce `09-server-a-token`. Úvodní koncept má nyní 15 průvodců. Tři spustitelné soubory v jejím files/ ukazují pevný main.py, server v .venv a ověření tokenu klienta. V lekci jsou přesné postupy pro dva terminály, očekávaný výstup a chybové stavy. Nejde o veřejný server ani automatické nasazení. Původní id dalších lekcí zachována. 87 testů OK, validátor 111 lekcí bez chyb, prohlížečový test přípravy OK. Viz poslední STATUS.md. Nic nepublikováno, původní plán dalších kurzů nepokračuje.


> **Aktuální předání v0.35 (3. 11. 2026):** Na žádost uživatele je v katalogu první koncept „Začínáme: prostředí, projekt a Git“ (`priprava`, 14 průvodců s `kind: guide`, 5 modulů). Není to hotový automaticky kontrolovaný kurz instalace. Každý podkurz má před lekcemi přípravu pro Windows/macOS/Linux a volbu VS Code/VSCodium/PyCharm. Společné návody rozšířeny, volitelné pip balíčky jsou pod `--extras`. Viz poslední STATUS.md a `docs/koncept-priprava.md`. 81 unit testů OK, validátor 110 lekcí bez chyb (96 původních běhově, 14 koncepčních strukturálně), 3 prohlížečové testy OK. Původní plán OOP nepokračoval; čeká se na připomínky ke konceptu. Nic nebylo publikováno. Historické pokyny a omezení pouze na VSCodium níže neplatí proti tomuto novému zadání; aktuální jsou tři editory.


> **Aktuální předání v0.34 (3. 11. 2026):** Uživatel pozastavil pokračování podle plánu a požádal o více přepínatelných příkladů pouze v základním kurzu. Hotovo: 68 nových příkladů v lekcích 01–31 a 37–39; tlačítka nad upravitelným editorem ukázky, oddělené rozepsané varianty, obnova původního kódu. Mini-projekty a navazující kurzy nezměněny. Přečtěte poslední záznam STATUS.md a aktualizované courses/SCHEMA.md. Validátor: 96 lekcí, 0 chyb; 77 unit testů OK; e2e přepínání OK, studentský kód na Pythonu 3.14.8. Neprovádět historické pokyny „další krok“ níže bez nového zadání. Nový kořen rozbaleného projektu v cloudu je `/workspace/dilna-pythonu-v0.33/dilna-pythonu`; původní absolutní cesty v tomto dokumentu jsou historické.


Určeno pro dalšího agenta (nový chat). Stav k **26. 10. 2026, verze v0.14**. Piš česky. Nejdřív přečti tento soubor, pak `STATUS.md` (historie a poučení) a `PLAN.md` (celkový plán).

## 1. Zadání od uživatele (v kostce)
Česká výuková aplikace na procvičování Pythonu postavená z 7 učebnic (zip `bdd6c544-U_ebnice_python.zip`, převedené do markdownu ve scratchpadu původního chatu, `py-md/b1.md` až `b7.md`: b1 Datová analýza, b2 Pygame, b3 soubory a web scraping, b4 Tkinter/API/e-maily, b5 začátečník, b6 středně pokročilé, b7 Tkinter a databáze). Požadavky:
- Projekt je stažitelná složka s odděleným html/css/js/py (ne jeden soubor), spouští se `python start.py`.
- Každá učebnice je samostatný podkurz, bez povinného pořadí. Lekce od jednoduchých ke složitým.
- Kód se píše ve **VSCodium** (ne PyCharm). Pro rozšíření, která tam nefungují, jsou alternativy (BasedPyright místo Pylance, Ruff, debugpy).
- Žádné hry s Harry Potterem ani jinými cizími postavami, grafika her jen kódem.
- **Kroky plánovat tak, aby stačil volný limit tokenů (uživatel má free plán).** Po každém kroku napsat, co je hotovo a co bude dál. Uživatel píše „pokračuj“. **Nespouštět více agentů najednou** (revize vždy jedním agentem po druhém, ~100–130 tis. tokenů každý). Uživatel jednou ztratil várku, protože došel limit relace: dělat menší várky a po každé uložit stav.

## 2. Co existuje
Kořen projektu: `/home/claude/dilna-pythonu/` (v novém chatu ho obnov z přiloženého zipu `dilna-pythonu-v0.12.zip`: `unzip`, pak `cd dilna-pythonu`). Pokud zip nepřiložen, najdeš `STATUS.md` a `PLAN.md` také v Projektu (`claude/STATUS-dilna-pythonu.md`, `claude/PLAN-dilna-pythonu.md`, `claude/HANDOVER-dilna-pythonu.md`).

| Podkurz | Stav |
|---|---|
| `zaklady` (Základy Pythonu) | 40 lekcí hotovo a nezávisle zrevidováno (1–15 ve v0.5, 16–40 ve v0.11). Status „draft“, čeká na zpětnou vazbu skutečného studenta |
| `soubory-web` | **22 z 22 lekcí HOTOVO** (m01: 01–06, m02: 07–11, m03: 12–22), kurz celý nezávisle zrevidován (v0.17–v0.19), zbývá zpětná vazba studenta a ověření ve VSCodium/Windows |
| `pygame-1` | **18 z 18 lekcí HOTOVO** (m01: 01–05 okno, smyčka, barvy, tvary, obrázky; m02: 06 Rect, 07 Fonty, 08 Zvuky, 09 Projekt Pohlednice; m03: 10–16 pohyb, klávesy, myš, odrazy, kolize, více objektů, skóre a konec hry; m04: 17–18 Sběratel hvězd). Nezávisle zrevidováno a opraveno (v0.24–v0.26), čeká na zpětnou vazbu a ověření okna a zvuku ve VSCodium. Plán viz oddíl 8 |
| `turtle-oop` | **rozpracováno, 16 z 40 lekcí** (m01 „Kreslení želvou“ hotov: 01 první čára, 02 čtverec a cyklus, 03 mnohoúhelníky a funkce, 04 barvy a tloušťka, 05 vyplněné tvary, 06 kruhy a oblouky, 07 souřadnice, `goto` a dvojice, 08 projekt spirograf). m02 „Zpět k základům“ hotov (09 čísla a typy, 10 řetězce: indexy a řezy, 11 řetězce: metody, 12 seznamy: metody a kopie, 13 řezy seznamů a kopie, 14 dvojice, rozbalování, `enumerate`, `zip`, 15 množiny `set`, 16 projekt analýza textu; kind `console`, kontrola přes `c.returns`). Plán dál: m03 OOP (třída, konstruktor, atributy, metody), čtyři pilíře, dědění, `super()`, dunder metody, MRO, `@property`, `@dataclass`, Snake a kvíz s API (viz `PLAN.md`, C). Lekce `kind: gui`, kontrola přes `turtle_run`. Zrevidováno agentem (lekce 01–16, v0.30 a v0.33) |
| `pandas`, `tkinter-api`, `pygame-2`, `databaze` | prázdné složky, plán v `PLAN.md` a `courses/catalog.json` (status „planned“) |

Další dokumenty: `README.md`, `docs/instalace.md`, `docs/vscodium.md`, `docs/reseni-problemu.md`, `courses/SCHEMA.md` (formát lekce).

## 3. Architektura (stručně)
- `start.py` spustí lokální `http.server` na 127.0.0.1 (jen stdlib), token v `?t=`, kontrola Host a Origin. Student kód běží v podprocesech s timeoutem, limitem výstupu a očištěným prostředím.
- `server/`: `app.py` (API), `runner.py` (spouštění), `checker.py` (kontrola lekce v podprocesu), `content.py` (katalog, pracovní složka), `security.py`, `lessonfiles.py` (kopírování `files/` lekce).
- `lib/dilna_check/__init__.py`: knihovna pro `check.py` lekcí (viz oddíl 5).
- `web/`: ES moduly (router, katalog, lekce, vlastní chytrý editor s našeptávačem a zvýrazněním f-řetězců, kvíz, nastavení).
- `tools/`: `validate_courses.py` (povinná kontrola), `setup_env.py` (venv a balíčky podle podkurzu), `install_extensions.py`, `doctor.py`, `make_zip.py`.
- `tests/`: 62 unittest testů (`python3 -m unittest discover -s tests -q`) a Playwright e2e skripty (`e2e_pilot.py`, `e2e_web.py` atd., spouštět jednotlivě, `timeout 300 python3 tests/e2e_pilot.py`).

## 4. Formát lekce
`courses/<kurz>/lessons/NN-nazev/`: `lesson.json` (`title`, `minutes`, `kind`), `lesson.md`, `example.py` (min. 2 vysvětlující komentáře, musí běžet bez chyby, volitelně `example.stdin`), `exercise.py` (výchozí kód, **nesmí projít kontrolou**), `check.py`, `solution.py` (**musí projít**), `quiz.json` (`q`, `options`, `answer` = index, `why`; možnosti se při zobrazení míchají), volitelně **`files/`** (pomocné soubory, kopírují se vedle kódu při spuštění, kontrole i do pracovní složky; podsložky povolené). Lekce se přidá do `courses/<kurz>/course.json` (moduly). Po každé dávce: `python3 tools/validate_courses.py` (kontroluje soubory, kvíz, komentáře, běh příkladu, že vzorové řešení projde a výchozí kód neprojde).

Kontrola se spouští **v samostatném podprocesu**: `server.checker.run_check(lesson_dir, kód, lib_dir, workdir)`. Student kód je `reseni.py` v dočasné složce (cwd), do které se zkopíruje `files/`. Proměnné prostředí: `DILNA_STUDENT`, `DILNA_RESULT`, `DILNA_DATA`.

## 5. Knihovna dilna_check (co umí)
`c = check()`; `c.load()` (spustí kód studenta s `__name__ = "student"`, takže blok `__main__` se neprovede, vrací jmenný prostor); `c.returns(ns, "f", (args), očekávané)`; `c.returns_close(...)` (desetinná čísla s tolerancí); `c.raises(ns, "f", (args), ValueError)`; `c.call(ns, "f", (args), kwargs, stdin="...")` vrací `(ok, hodnota)` a vypsaný text je v `c.last_output`; `c.run(stdin=...)` pustí soubor jako program; `c.no_error`, `c.output_contains`, `c.output_has_line` (řádek KONČÍ textem); `c.uses(ast.For, hint)`, `c.uses_call("name")`, `c.function("f")` (AST funkce), `c.calls_in(node, "name")`, `c.imports("math")`, `c.utf8()` (každé textové `open`/`read_text`/`write_text` má `encoding`), `c.add(name, ok, msg)`, `c.done()` (nutné na konci).

**Želva bez okna (od v0.27):** `r = c.turtle_run(keys=["Up"], clicks=[(x, y)], ticks=3)` spustí program s náhradou modulu `turtle` (`lib/dilna_check/turtlerun.py`), která si pamatuje kreslení a nic nezobrazuje (kruh je mnohoúhelník jako v pravé želvě). `TurtleResult`: `segments` (`[x1, y1, x2, y2, barva, tloušťka, želva, zdroj]`, zdroj `move`/`goto`/`circle`), `fills`, `dots`, `texts`, `stamps`, `calls`, `turtles` (konečný stav každé želvy), `bgcolor`, `title`, `handlers`, `mainloop`, `ended`, `error`, `out`; metody `called(jméno)`, `length(barva)`, `colors()`, `widths()`, `covers(bod, tol, barva)`, `bbox()`, `corners()` (rohy mezi navazujícími úsečkami; uzavřený n-úhelník jich má n−1, protože za poslední stranou nic nenavazuje), `fill_area(barva)`. Barvy jsou jména malými písmeny nebo `#rrggbb`; RGB trojice se po `colormode` převedou na `#rrggbb`. `c.turtle_no_error(r)`. Klávesy a časovač se spustí při `done()`/`mainloop()`. `c.uses_call("forward|fd", ...)` přijímá alternativy přes `|`. Validátor spouští `example.py` s `import turtle` přes turtlerun. Test: `tests/test_turtlerun.py`. Náhrada od v0.30: barvy se vrací jménem, pokud jde o základní barvu (`#ffff00` → `yellow`), RGB mimo rozsah `colormode` vyhodí `TurtleGraphicsError`, `pos()` vrací `Vec2D`, `t.screen`, `clear`/`reset` mažou, úsečky nulové délky se nezapisují, `speed` se mapuje jako v pravém turtle. Pozor: skutečný turtle potřebuje tkinter (na Linuxu `python3-tk`).

**Pygame bez okna (od v0.20):** `r = c.pygame_run(frames=5, pixels=[(x, y)], colors=[(r, g, b)], events={snímek: [{"type": "KEYDOWN", "key": "K_LEFT"}, {"type": "QUIT"}, {"type": "MOUSEBUTTONDOWN", "pos": [x, y], "button": 1}]}, held={od_snímku: ["K_LEFT"]}, mouse={od_snímku: [x, y]})` spustí program studenta v podprocesu (`lib/dilna_check/pgrun.py`, SDL `dummy`, žádné okno ani zvuk). Program se zastaví po `frames` snímcích (volání `display.flip`/`update`). Hodiny jsou zrychlené (`Clock.tick` vrací 16 ms, zapisuje požadované FPS do `r.fps`). Výsledek `PgResult`: `r.frames`, `r.ended` (program skončil sám), `r.error`, `r.timed_out`, `r.size`, `r.caption`, `r.pixel((x, y), snímek=-1)`, `r.color_count((r, g, b), snímek, region=(x, y, š, v))` (v `pygame_run` pak `colors=[(r, g, b, x, y, š, v)]`), `r.drew("circle")` (volání `pygame.draw`), `r.rendered("text")`, `r.images` (načtené soubory), `r.sounds`, `r.music`, `r.out` (stdout). `c.pg_no_error(r)` zapíše kontrolu „program běží bez chyby“ s užitečnou hláškou. Snímky se číslují od 0; událost ve snímku k dostane program při (k+1). průchodu smyčkou. Barvy kontrolovat na pixelech uvnitř tvarů, ne na hranách. Pozadí lekcí s průhlednými obrázky nesmí být černé, jinak se `convert()` nepozná od `convert_alpha()`. `PYGAME_HIDE_SUPPORT_PROMPT` se nastavuje jen v kontrole; v aplikaci se banner pygame ve výstupu zobrazí.

## 6. Poučení z revizí (dodržuj při psaní nových lekcí)
1. **Pojem nesmí být použit dřív, než je vysvětlen** (i ve vzorovém řešení). Před psaním grepni `lesson.md` předchozích lekcí. Ve skutečnosti se opakovaně přehlédlo: `%`, `//`, `**`, `if __name__`, `enumerate`, `str()`, `is None`, `key=`, `pass`, `isalpha` a podobně.
2. **Kontroly musí odmítnout výsledek zapsaný natvrdo** (více vstupů, krajní případy: prázdný vstup, jedna položka, velká/malá písmena, diakritika). Požadované konstrukce (`try`, `raise`, `seed`, `sorted`) kontrolovat **uvnitř konkrétní funkce** přes AST, ne kdekoliv v souboru.
3. Kontroly nesmí odmítnout správné alternativní řešení (např. nevyžadovat `append`, když jde použít `+`).
4. Náhodné funkce kontrolovat statisticky (pokrytí celého rozsahu, více volání), vzorové řešení ověřit 20× za sebou. U her dosadit tah počítače: `ns["nahodny_tah"] = lambda: "nůžky"`.
5. Pořadí souborů z disku (`glob`, `iterdir`) není zaručené: výsledek testovat s `sorted` a kontrolovat jeho použití přes AST.
6. Každou dávku **zkus špatnými řešeními** (skript volající `run_check` s upravenými vzorovými řešeními) a výchozí kód nesmí projít.
7. Po větším bloku (cca 15–20 lekcí) nezávislá revize jedním agentem (prompt viz minulé revize: dát mu seznam předchozích lekcí, co už je vysvětleno, a pokyn nic needitovat, ověřovat spuštěním).
8. Ve vzorových datech ověřovat fakta spuštěním (chybně označený palindrom, špatný počet samohlásek se chytil až při validaci).
9. Nepoužívej `pkill -f` s vzorem, který se vyskytuje v samotném příkazu (zabije shell). Používej absolutní cesty ve skriptech.
10. Nikdy nespoléhej na to, že kroky ve VSCodium (F5, Ruff, `codium`) fungují: nejsou ověřeny na skutečném VSCodium, formuluj je jako návod a vždy nabídni záložní postup.

## 7. Plán zbývajících lekcí podkurzu `soubory-web` (06–22)
Dávky po 5 lekcích (~20 tis. tokenů). Balíčky `requests` a `beautifulsoup4` jsou v `tools/setup_env.py` pro tento kurz; v testovacím prostředí jsou nainstalované (bs4 4.15, requests 2.34), na studentově počítači je nainstaluje `setup_env.py` do `.venv`.
- **m01:** HOTOVO (01–06, včetně mini-projektu Deník).
- **m02 CSV a JSON:** HOTOVO 07 CSV čtení, 08 DictReader/DictWriter, 09 JSON, 10 Zpracování tabulky (`sorted` s `key` a `lambda` už vysvětleno). 11 Kontakty v JSON je také hotová.
- **m03 Web scraping (offline):** HOTOVO 12–15 (parser nad textem) a 16 `requests` (GET, status_code, text, json), 17 chyby sítě (`raise_for_status`, timeout, opakování), 18 Projekt: ceník knih do CSV, 19 Stahování souborů a obrázků (`wb`, `urljoin`), 20 Etika a `robots.txt` (`RobotFileParser`, User-Agent, pauzy). 21 Opakování (CSV, JSON, HTML offline) a 22 Závěrečný test (sběrač cen: robots.txt, stažení s ošetřením chyb, zpracování, JSON). Podkurz je kompletní.
- **Rozhodnuto (lekce 16–20, offline):** pomocný modul `dilna_web.py` (originál `courses/soubory-web/shared/dilna_web.py`) se do každé lekce, která ho potřebuje, kopíruje jako `files/dilna_web.py` (+ stránky v `files/web/`). Díky mechanismu `files/` je u studenta vedle kódu v aplikaci, v kontrole i ve složce pro VSCodium, aniž by se měnilo `PYTHONPATH`. `spust()` vrací `http://127.0.0.1:<port>`; server umí `/_status/<kód>`, `/_pomalu/<s>`, `/_nestabilni/<jméno>` (2× 500, pak 200), `/_presmerovani`, `/_hlavicky` (JSON s hlavičkami klienta). Při úpravě originálu je nutné přegenerovat kopie (`tests/test_dilna_web.py` hlídá shodu). `check.py` si server spouští sám (`sys.path.insert(0, os.getcwd())`) a předává adresu studentovým funkcím. Dotazy na `time.sleep` se v kontrole zaznamenávají (v hlavním vlákně), server dál čeká doopravdy.
- Obrázky v lekci 19 (`files/web/img/*.png`) jsou drobné 8×8 PNG generované skriptem (binární soubory v `files/` fungují).
- Do `courses/soubory-web/data/` zatím nic nepatří (pomocné soubory jsou u lekcí v `files/`).

## 8. Další podkurzy (po dokončení soubory-web)
Pořadí podle plánu: pygame-1 (okno, kreslení, vstupy, 18; **hotovo, čeká revize;** po revizi pokračovat dalším podkurzem. Obrázky `raketa.png` a `hvezda.png` generuje skript (vlastní kresba, žádné cizí postavy), jsou v `lessons/05-obrazky/files/`; další lekce si je zkopírují do vlastní `files/`), turtle-oop (40), pandas (42, Pandas 3.0 Copy-on-Write), tkinter-api (28), pygame-2 (30), databaze (32, SQLite, parametrizované dotazy). Počty a témata viz `PLAN.md`. Ekosystém: Python 3.14 jako základ, `pygame-ce` místo `pygame`, psycopg 3, Gmail jen s heslem aplikace. U GUI lekcí je `kind: "gui"` (kontrola jen přes AST a funkce).

## 9. Neověřeno a otevřené body
- Instalace rozšíření ve VSCodium, F5 ladění, Jupyter, příkaz `codium`, URI `vscodium://file/...`, Flatpak, winget/brew příkazy.
- Chování na Windows a macOS (testováno jen na Linuxu, Python 3.13), Firefox, Safari, dotykové klávesnice, offline záložní písma.
- Lekce **nečetl žádný skutečný student**. Uživatel se o úrovni a tónu zatím nevyjádřil.
- Dříve se v adresáři `courses/zaklady/lessons/` objevily nezapsané starší lekce `37-opakovani-zaklady`, `38-opakovani-data`, `39-opakovani-chyby-moduly` (a stará verze `40-zaverecny-test`) neznámého původu. Byly přesunuty mimo projekt do scratchpadu původního chatu (`old-lekce/`), lekci 40 přepsala nová verze. V tomto předání nejsou. Pokud je chceš, zeptej se uživatele.
- Zbývá dodělat pro Základy: zpětná vazba, případně změna stavu `draft` na `ready` v `courses/catalog.json`.

## 10. Jak začít v novém chatu
1. Rozbal zip, `cd dilna-pythonu`, ověř: `python3 tools/validate_courses.py` (očekávání: 80 lekcí, 0 chyb) a `python3 -m unittest discover -s tests -q` (62 testů OK).
2. Přečti `STATUS.md` (posledních ~60 řádků) a oddíl 7 výše.
3. Napiš uživateli první větu, co budeš dělat, a pusť se do lekcí 16–20 (requests proti lokálnímu serveru, chyby sítě, projekt scraping, stahování souborů). Skripty na generování lekcí byly jednorázové ve scratchpadu a nejsou součástí projektu: piš lekce přímo do složek, nebo si vytvoř vlastní generátor.
4. Po dávce: validate, špatná řešení, testy, `STATUS.md` dopsat a zrcadlit do Projektu (`Projects` → `project_write` do `claude/STATUS-dilna-pythonu.md`), `python3 tools/make_zip.py /home/claude/dist/dilna-pythonu-v0.N.zip` a poslat uživateli. Číslo verze zvyš v `README.md` a `tools/make_zip.py`.
5. Odpověď končí: co je hotovo, co bude další krok.

**Trvalé pravidlo:** soubor `POKYNY-SPUSTENI.md` (ověření Pythonu, instalace, spuštění) je v kořeni projektu a patří do každého ZIPu (make_zip ho zahrne automaticky). Při změně příkazů nebo voleb ho aktualizovat.
