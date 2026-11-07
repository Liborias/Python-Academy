## Dva štítky mohou nést stejnou adresu

Zákazník napsal stejnou doručovací adresu do dvou formulářů. V programu vznikly dva objekty. Mají stejné údaje, ale každý můžeme samostatně upravit. To je rozdíl mezi identitou a hodnotovou rovností.

Použijeme nový jednoduchý model Adresa(ulice, mesto, psc). V této lekci předpokládáme všechny tři vstupy jako text. PSČ necháme textové, aby zůstala zachovaná i případná počáteční nula. Konstruktor nic neořezává ani nepřevádí na číslo. Ulice, město a PSČ jsou běžné veřejné atributy; repr je připravený podle minulé lekce.

## is: označují odkazy tentýž objekt?

```python
prvni = Adresa("Javorová 1", "Brno", "60200")
druha = Adresa("Javorová 1", "Brno", "60200")
odkaz = prvni
```

Volání konstruktoru vytvořila dva různé objekty, proto `prvni is druha` vrátí False. Přiřazení odkaz = prvni nový objekt nevytváří; `prvni is odkaz` je True. Změna odkaz.psc tedy změní i objekt dostupný pod jménem prvni.

Operátor is slouží k totožnosti, například když chceme ověřit, že expedice uchovala původní balík. Nehodí se k porovnávání obsahu textů nebo čísel. Ke zjištění shody údajů použijeme ==.

## ==: co v našem modelu znamená shoda?

U obyčejné vlastní třídy bez vlastního porovnání dva samostatné objekty se stejnými atributy obvykle rovné nejsou. Python naše pravidlo shody nezná. Definujeme proto __eq__(self, other), kterou využije operátor ==.

Pro adresy stanovíme přesné pravidlo: porovnáváme objekty stejného konkrétního typu a všechny tři textové údaje musejí být shodné. Žádné sjednocování velikosti písmen ani mezer neprobíhá. Stejná ulice v jiném městě nebo jiné PSČ znamená jinou hodnotu.

Metoda vrací True nebo False podle aktuálních atributů. Neuchovává starou kopii výsledku a nic nepřepisuje. Když druhé adrese opravíme PSČ, další porovnání změnu hned uvidí.

## NotImplemented nabídne šanci druhé straně

```python
if type(other) is not type(self):
    return NotImplemented
```

type(objekt) vrací jeho konkrétní třídu. Tímto pravidlem neporovnáváme různé druhy objektů, ani předka s potomkem. Pro cizí typ vracíme zvláštní hodnotu NotImplemented. Říká Pythonu „toto porovnání neumím“, takže může zkusit porovnání z druhé strany. Pokud ani druhý objekt porovnání neposkytne, == nakonec pro různé objekty vrátí False.

NotImplemented je návratová hodnota. Není to výjimka NotImplementedError, kterou jsme použili u nehotové základní dopravy. Nevyvoláváme ji přes raise. Přímé volání adresa.__eq__("text") zde vrátí NotImplemented, zatímco výraz adresa == "text" projde celým postupem Pythonu a vyjde False.

## Váš úkol

Doplňte __eq__ v Adresa. Ponechte konstruktor a repr. U stejného typu porovnejte ulici, město i PSČ a vraťte bool. Pro jiný typ vraťte NotImplemented. Porovnání nic nevypisuje a nemění žádný objekt.

Spusťte ukázku: dvě instance nejsou totožné, ale před opravou PSČ mají stejnou hodnotu. Pak zkuste změnit postupně ulici, město a PSČ. Porovnejte adresy v obou pořadích. Nakonec vytvořte odkaz na původní adresu a vysvětlete, proč změna přes něj zasáhne tentýž objekt, zatímco změna druhé instance původní adresu neovlivní.
