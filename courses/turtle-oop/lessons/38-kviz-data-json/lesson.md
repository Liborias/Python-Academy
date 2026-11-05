## Data nejsou ještě objekty našeho programu

Otázky nemusíme psát do zdrojového kódu. Přiložený soubor otazky.json obsahuje vlastní české otázky ve struktuře podobné odpovědi služby Open Trivia DB. Tato struktura nám umožní použít stejný převod pro soubor i pozdější API.

Soubor kviz_model.py obsahuje řešení předchozí lekce. Import `from kviz_model import Otazka` zpřístupní datovou třídu bez spouštění ukázky.

## Co znamená JSON

JSON je textový formát pro předávání dat. Podporuje objekty, pole, řetězce, čísla, true, false a null. Po převodu do Pythonu z nich vzniknou slovníky, seznamy, texty, čísla, True, False a None.

```json
{
  "response_code": 0,
  "results": [
    {"type": "boolean", "question": "Seznam lze měnit.", "correct_answer": "True"}
  ]
}
```

Pozor na uvozovky: tato konkrétní služba posílá correct_answer jako **text** `"True"` nebo `"False"`, nikoli jako JSON true/false. Náš model naopak potřebuje bool. Platnou odpověď převedeme porovnáním `odpoved == "True"`, ne voláním bool nad řetězcem.

## Čtení a převod jsou dva kroky

```python
text = Path(cesta).read_text(encoding="utf-8")
data = json.loads(text)
```

`Path` ze standardního pathlib představuje cestu k souboru. Read_text otevře a přečte soubor jako text a zase ho zavře; UTF-8 zachová české znaky. `json.loads` pak z textu sestaví Python data. Písmeno s v loads připomíná, že načítáme z řetězce. Chybný JSON způsobí ValueError (konkrétně jeho odvozenou JSONDecodeError).

Čtení souboru dejte do nacti_soubor. Vlastní kontrola a převod patří funkci preved_otazky(data), která už žádný soubor neotvírá. Tu později zavoláme i s údaji ze sítě.

## Zkontrolujeme dohodnutou strukturu

Před vytvářením objektů požadujeme:

1. Celá odpověď je slovník s celočíselným response_code rovným 0. Jiný kód znamená, že zdroj požadavek nesplnil.
2. Results je neprázdný seznam. Prázdná nebo chybějící data nejsou úspěšně načtený kvíz.
3. Každá položka je slovník s type rovným boolean, řetězcovým question a odpovědí přesně True nebo False zapsanou jako text.
4. Text po dekódování a odstranění vnějších mezer není prázdný.

Funkce `type(hodnota)` vrací skutečný typ. U response_code můžeme použít `type(kod) is int`, aby se nám za číslo 0 nepovažovala hodnota False. `dict.get` pomůže ověřit chybějící klíč bez předčasné KeyError. Další nevyužité klíče, například category, nevadí.

Při jakékoli vadné položce vyvolejte ValueError. Nepřeskakujte ji potichu a nevracejte jen část zdroje. Přijímaný zdroj má být jako celek použitelný; další lekce bude umět zvolit zálohu.

## Proč text obsahuje &quot;

Vnější služba může poslat HTML entity: například `&quot;Python&quot;` místo uvozovek, `&amp;` místo & nebo `&#039;` místo apostrofu. `unescape(text)` z modulu html je převede na čitelné znaky. Potom `.strip()` odstraní mezery z obou konců.

Výsledek je běžný text otázky, žádný HTML kód nevykonáváme. Seznam převedených Otazka zachová pořadí zdroje. Vstupní slovníky a seznamy neměníme.

## Váš úkol

Doplňte `preved_otazky(data)` a `nacti_soubor(cesta)` podle uvedených pravidel. První funkce vrátí neprázdný seznam objektů Otazka. Druhá přečte zadanou cestu jako UTF-8, použije json.loads a předá výsledek do stejného převodu. Chybějící nebo vadný soubor má oznámit chybu, nikoli předstírat úspěch.

Ukázka zobrazí počet pěti přiložených otázek a první tvrzení. Při práci v editoru spouštějte kód z pracovní složky lekce s otazky.json a kviz_model.py; aplikace je připraví vedle reseni.py. Zkuste ve vlastní pracovní kopii změnit jednu otázku, přidat HTML entitu nebo pokazit odpověď a sledujte výsledek.
