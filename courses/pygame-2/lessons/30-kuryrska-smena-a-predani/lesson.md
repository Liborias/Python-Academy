## Kurýrská směna: vlastní profil a paměť výsledků

Závěrečný projekt spojí skutečnou hru z25 s uloženými výsledky z28 a cestami z29. Dědičnost použijeme pro malé rozšíření životního cyklu. Zásobník režimů i Kolo zůstávají hotové součásti; nepíšeme druhou paralelní herní smyčku.

Vlastní varianta má pojmenovaného kurýra a nastavitelnou rychlost. Výchozích 260 px/s je o něco více než původních 240. Můžete si vyzkoušet například 220 nebo 280 a porovnat ovladatelnost. Vyšší rychlost automaticky neznamená snazší hru. Vítězství stále vyžaduje alespoň šest dat a přežití tří vln; pauza, štít a životy mají stejná pravidla.

```python
class Pokus:
    pass
prvni, druhy = Pokus(), Pokus()
ulozeny = prvni
print('Stejný pokus:', ulozeny is prvni)
print('Nový pokus:', ulozeny is druhy)
```

Identita umožní zapsat dokončený pokus právě jednou. Obrazovka výsledku může běžet mnoho snímků, ale nepřidá při každém další řádek ani znovu nezkusí neúspěšný zápis. Nový restart vytvoří novou identitu.

## Životní cyklus a chyby

Konstruktor jen načte tabulku. Novy_let nejprve vytvoří nový svět přes rodiče a upraví rychlost hráče. Update po rodiči pozná přechod do výsledku, zkusí uložit pořadí a zapamatuje si identitu. Kresli deleguje původnímu vykreslení a přidá přehled z pamet.py. Souborový zápis tedy není součást každého kreslení.

Při chybě čtení či zápisu se objeví zpráva v okně. OSError zachytíme právě na hranici aplikace, kde ho umíme vysvětlit. Nižší funkce ho nezaměňují za úspěch. Do tabulky patří i neúspěšný let, úspěšné lety mají přednost. Uchováváme nejlepších pět záznamů, nejde o oddělený žebříček pro různé rychlosti.

## Uložení projektu a zkouška předání

V aplikaci použijte uložení do pracovní složky a otevřete reseni.py v editoru. Teprve z této stálé složky budou výsledky v data/vysledky.json dostupné i po dalších spuštěních. Běžné tlačítko Spustit v prohlížeči vytváří dočasnou kopii běhu, proto jeho soubory nepovažujte za trvalou paměť. PNG droni.png lze po normálním zavření prohlédnout a stáhnout.

```powershell
python over_projekt.py
python reseni.py
```

První příkaz provede připravené testy původního modelu; vlastní testy rozšíření přidejte do testy podle předchozí lekce. Druhý otevře vaši skutečnou hru. Mezerník start/nabídka, šipky/WASD pohyb, P pauza, R nový let, Esc/křížek konec. Okno potřebuje místní grafickou plochu hostitele Pythonu a nepřenáší se z virtuálního serveru do webové stránky. Běžné zavření ukládá PNG, Stop ho nezaručuje.

Dokončete alespoň jeden let, vraťte se do nabídky a program zavřete. Spusťte jej znovu a ověřte tabulku. Zkuste také neplatný JSON, nedostupnou cestu a restart v pauze; své důležité výsledky pro pokusy nejdřív zkopírujte. Volitelný sestavit.py zde sestavuje přímo reseni.py. Předávací NAVOD.md popisuje obsah složky, instalaci, ovládání, cestu výsledků a známá omezení.

## Váš úkol

Doplňte **HraSPoradim(Hra)** podle výkladu. Zachovejte skutečnou Hra z25, její režimy, herní pravidla, ovládání, pauzu a nový svět. Vlastní profil mění pouze rychlost hráče, ne pravidla vítězství. Jméno má po strip 1–24 znaků, rychlost je kladná konečná; jinak ValueError.

Konstruktor (cesta, jmeno='Kurýr', rychlost=260, seed=23) volá rodiče, uloží Path(cesta), čisté jméno, rychlost, zapsane_kolo=None, zprava='Výsledky připravené.' a načte serad_vysledky(nacti_vysledky(cesta),5). Při OSError má vysledky=[] a zprava='Výsledky nejsou dostupné.'. Nic nezapisuje.

Novy_let zavolá rodiče a nastaví kolo.hrac.rychlost z profilu. Update nejprve zavolá rodiče; při bezi=True a stav='vysledek' jednou na identitu kola připraví záznam jmeno/body=kolo.skore/uspech=(duvod=='uspech'). Smrt a nedostatek dat jsou také platné neúspěšné pokusy. Zapsane_kolo nastavte před pokusem, aby chyba nevyvolala další zápis každý snímek.

Zkuste uložit serad_vysledky([*vysledky, novy],5). Při úspěchu nahraďte paměť pořadím a zprava='Výsledek uložen.'. Při OSError zachovejte starou tabulku a zprava='Výsledek se nepodařilo uložit.'. Menu, pauza, rozehraná hra a ukončený program se nezapisují. Další restart má novou identitu a lze ho zaznamenat znovu.

Kresli nejdřív deleguje rodiči a pak zavolá připravenou vykresli_pamet(plocha,self), která přidá profil/stav a tabulku nejlepších výsledků v nabídce. Režimy, vykreslování a zápis mají oddělené odpovědnosti.

Před další stavbou zkopírujte vlastní výsledky z distribuční složky mimo dist: sestavení s --noconfirm nahrazuje předchozí výstup.
