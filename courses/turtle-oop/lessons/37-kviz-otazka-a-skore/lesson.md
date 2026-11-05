## Druhý projekt: kvíz pravda/nepravda

Snake spojil více objektů, pravidel a zobrazení. Na závěr kurzu totéž zkusíme v jiném prostředí: vytvoříme kvíz, jehož otázky mohou přijít z přiloženého souboru nebo z API. Začneme jeho modelem bez čtení souborů a bez internetu.

Otázka je datový záznam, proto využijeme dataclass z lekce 28:

```python
@dataclass
class Otazka:
    text: str
    spravne: bool
```

`text` obsahuje tvrzení a `spravne` skutečnou hodnotu True nebo False. Anotace sama data nekontroluje. V této lekci předpokládáme platné objekty Otazka; kontrolu vnějších dat doplníme příště. Dataclass připraví konstruktor, reprezentaci a hodnotovou rovnost.

## Kvíz uchovává průběh

Třída Kviz má vlastní seznam otazky, index aktuální otázky a skore. Index začíná na nule, skóre také. Kvíz obsahuje otázky, ale sám se žádného uživatele neptá a nic nevypisuje. Stejné vyhodnocování tak později využijeme v konzolové aplikaci.

`list(otazky)` v konstruktoru vytváří vlastní seznam. Změna vstupního seznamu nemá přidávat nebo odebírat otázky rozehranému kvízu. Samotné objekty Otazka pouze čteme; nemusíme vytvářet jejich hluboké kopie.

## Která otázka je na řadě

Metoda `aktualni()` vrátí objekt na pozici index. Pokud jsme došli na konec, vrátí None. Samotné zjištění otázky nesmí posunout index nebo přidat bod — zobrazení se může na stejný stav podívat vícekrát.

Platný je i prázdný seznam. Takový kvíz má rovnou aktuální otázku None a skóre nula. Nezaměňujte chybějící otázku s otázkou, jejíž správná odpověď je False: i nepravdivé tvrzení je stále plnohodnotná otázka.

## Co provede odpovez

```python
spravne = odpoved == otazka.spravne
if spravne:
    self.skore += 1
self.index += 1
return spravne
```

Vyhodnocujeme jednu skutečnou odpověď a vracíme True při správné, False při nesprávné. Index se posune v obou případech. Bod ale přibude pouze při shodě.

Nejdřív ověříme `isinstance(odpoved, bool)`. Text `"False"` je neprázdný řetězec a při běžném převodu bool by znamenal True. Takový automatický převod zde nechceme. Čísla 0 a 1 také odmítneme, přestože se při některých porovnáních mohou chovat podobně jako False a True. Překlad uživatelského vstupu na bool bude úkolem závěrečné aplikace.

Neplatný typ nebo odpověď po dokončení kvízu vyvolá ValueError. Před odmítnutím nesmíme změnit skóre ani index. Po správné odpovědi na poslední otázku už aktualni vrací None a další odpovez se nepřičítá znovu.

## Váš úkol

Doplňte `Kviz.aktualni()` a `Kviz.odpovez(odpoved)` podle popsaných pravidel. Dataclass i konstruktor jsou připravené. Využijte aktuální hodnoty vlastního objektu, nic nevypisujte a neupravujte text nebo správnou odpověď otázek.

Spusťte ukázku: na první otázku odpoví True, na druhou False a skóre bude 2 ze 2. Změňte jednu odpověď a porovnejte skóre i počet zodpovězených otázek. Stejná pravidla musí fungovat pro jiný počet otázek a dvě současně rozehrané instance.
