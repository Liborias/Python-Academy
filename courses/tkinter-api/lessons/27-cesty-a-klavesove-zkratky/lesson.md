## Pracovní složka a složka programu jsou různé věci

Program může být spuštěn z terminálu, editoru nebo zástupce. Jeho aktuální pracovní složka se proto může měnit. Kdyby ukázku hledal jen jako `Path("data")`, mohl by ji hledat na nesprávném místě. Přibalený zdroj má určovat soubor programu.

Funkce `cesty_projektu(soubor, domov)` vrací slovník se dvěma Path: data a koncepty. Data je složka data vedle absolutní cesty předaného souboru. Koncepty je absolutní zadaný domov; slouží jako výchozí složka dialogů pro uživatelova data. Funkce nic nevytváří a neukládá.

Path.resolve určí absolutní cestu, parent její rodičovskou složku a operátor / připojí další část. Expanduser rozvine případné ~ v domovské cestě. V hlavním programu předáme __file__ a Path.home(). __file__ je soubor tohoto modulu, Path.home získá domov současného uživatele. Sys.executable určuje interpreter či spustitelný soubor, proto z něj cestu ke zdrojům neodvozujeme.

U současného PyInstalleru je __file__ použitelné také uvnitř balíčku. Složku data do něj zahrnuje volba --add-data z lekce 26. Vlastní koncepty ukládá uživatel přes dialog například do Dokumentů; distribuční adresář se zdroji se jejich uložením nemění.

## Načtení přibalené ukázky

Tlačítko Načíst ukázku přečte data/vychozi-koncept.json přes hotové nacti_koncept z lekce 24. Stejně jako při běžném načtení nejprve ověří celý model a teprve pak přepíše formulář. Soubor s ukázkou slouží ke čtení. Změny následně uložíte jako vlastní koncept na vybranou cestu.

Chybějící nebo vadný zdroj zobrazí zprávu „Ukázkový koncept není dostupný. Zkontrolujte složku data.“ Rozpracovaná pole i náhled zůstanou zachované. Jde o konkrétní problém při čtení zdroje, takže po opravě složky nebo souboru lze akci znovu provést. Žádný prázdný náhradní koncept se automaticky nevloží.

## Klávesové zkratky bez vedlejších změn textu

Přidáme Ctrl+S pro Uložit koncept, Ctrl+O pro Načíst koncept a Ctrl+Enter pro Ověřit a zobrazit. Také na macOS tato ukázka používá klávesu Control. Předání zprávy zůstává samostatné tlačítko, aby ověření náhledu nezačalo síťovou operaci.

Bind propojí událost s funkcí. Callback dostane argument udalost, zavolá existující souborovou či ověřovací akci a vrátí text break. Ten zastaví další zpracování stejné události. Vazbu připojujeme k oknu i k oběma Entry a oběma Text. Vlastní vazba na Text proběhne před jeho třídní vazbou, takže Ctrl+O nevloží nový řádek a stejný stisk neotevře dva dialogy.

Entry dovoluje Tab pro přechod na další ovládání; v Text může být tabulátor součástí obsahu, pro přechod použijte Ctrl+Tab. Aktivní pole má fokus. Při ověřovací chybě se zaměří příslušný vstup jako v lekci 22.

Během SMTP platí stejná ochrana busy také uvnitř callbacků. Disabled tlačítko samo nestačí, protože stejnou akci nyní může vyvolat klávesnice. Uložit, načíst a měnit ukázku lze po dokončení přenosu; do polí lze mezitím dál psát a předávaný snímek se nemění.

## Váš úkol

Dokončete cesty_projektu. Z předaného souboru určete data vedle něj a ze zadaného domova výchozí umístění konceptů. Vraťte absolutní objekty Path, aktuální pracovní složku nepoužívejte jako základ pro už absolutní vstupy a nic nezapisujte. Načítání, dialogy i zkratky jsou připravené.

Spusťte reseni.py z jiného adresáře pomocí celé cesty a stiskněte Načíst ukázku. Pak vložte víceřádkový text, v jeho poli použijte Ctrl+S a po změně Ctrl+O: musí se obnovit celý uložený text bez přidaného řádku. Ctrl+Enter ověří náhled a počet v záchytu zůstane nulový. Nakonec začněte pomalé předání a vyzkoušejte stejné zkratky při čekání: neotevřou dialog a nezničí nové psaní.
