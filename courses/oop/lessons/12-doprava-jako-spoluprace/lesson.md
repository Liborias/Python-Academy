## Expedice má balík a zvolenou dopravu

Při objednávání měníme způsob doručení. Kdybychom kvůli každé kombinaci tvořili novou třídu, potřebovali bychom postupně ExpediceKuryr, ExpediceExpres, ExpediceOsobniOdber a další. Expedice ale sama kurýrem není. Uchová odkaz na balík a na objekt, který umí jeho dopravu ocenit.

Tomuto skládání spolupracujících objektů říkáme kompozice. Už ji známe z objednávky obsahující položky. Dědění vyjadřuje „expresní kurýr je kurýr“, kompozice zde vyjadřuje „expedice má zvolenou dopravu“. Oba postupy mohou v programu spolupracovat.

## Odkazy místo kopií

Konstruktor Expedice(balik, doprava) přijme existující objekty. Nejdřív ověří, že doprava umí převézt tento balík, voláním doprava.cena(balik). Pokud to vyvolá ValueError, nová expedice se nevytvoří úspěšně. Při úspěchu si uloží přesně původní objekty, nikoli jejich kopie.

Property balik a doprava jsou pouze pro čtení. Volající může ověřit `expedice.balik is balik`: operátor is zjišťuje, zda oba odkazy označují stejný objekt. Přiřazení expedice.doprava = nova vyvolá AttributeError; k ověřené změně slouží metoda.

Připravené soubory balik.py, doprava.py a expres.py obsahují předchozí řešení a objeví se i ve staženém pracovním prostoru. Žádné balíčky se neinstalují. Stávající sklad ani objednávku v této lekci neměníme: stavíme jen volbu nabídky dopravy pro jeden balík. Celý průchod propojí závěrečný projekt.

## Nabídku určuje aktuální spolupracovník

```python
def nabidka(self):
    return self.doprava.cena(self.balik)
```

Expedice přepošle otázku aktuální dopravě. Tomu se říká delegování. Cenu nekopíruje do vlastního ceníku a nerozhoduje podle názvu třídy. Každé volání se zeptá znovu, takže zachytí i změnu nabídky u spolupracujícího objektu.

## Nejdřív ověřit, potom změnit

```python
cena = nova.cena(self.balik)
self._doprava = nova
return cena
```

zmen_dopravu(nova) nejprve požádá novou dopravu o cenu. Až když dotaz úspěšně skončí, uloží novou volbu a vrátí její cenu. Pokud nový kurýr odmítne balík kvůli limitu, přiřazení se vůbec neprovede a původní doprava zůstane zachovaná. Stejné pořadí „ověřit, potom měnit“ jsme používali při rezervaci skladu.

Balík se při přepnutí nemění. Dotazy a výběr nic nevypisují, nerezervují ani skutečně neodesílají. Dvě expedice mají vlastní volbu dopravy.

## Nová doprava bez změny Expedice

Ukázka přidává Cyklodoprava s metodou cena(balik): do 2000 g vrací 59 Kč, těžší balík odmítne. Nemusí dědit z Doprava. Expedici stačí společné potřebné rozhraní, metoda cena. Neměla by proto vybírat dopravy přes isinstance nebo seznam povolených názvů tříd.

Kdyby nová možnost slibovala totéž rozhraní, ale v cena měnila balík nebo rezervovala zboží, neodpovídala by naší dohodě o nezměněném stavu. Společné jméno metody je začátek; důležité je také její očekávané chování.

## Váš úkol

Doplňte konstruktor, nabidka a zmen_dopravu. Zachovejte odkazy na původní objekty, připravené property a kontrolu před změnou. Výjimku z odmítnuté nabídky nechte projít k volajícímu. Neuchovávejte zastaralou kopii ceny.

Spusťte ukázku: osobní odběr stojí 0, kurýr 99 a expres 149 Kč. Následuje neúspěšný pokus zvolit kurýra s limitem 1000 g; balík váží 1200 g, proto zůstává expres za 149 Kč. Nakonec ukázka přepne na cyklodopravu za 59 Kč bez zásahu do Expedice. Vyzkoušejte dvě expedice a ověřte, že změna jedné neovlivní druhou.
