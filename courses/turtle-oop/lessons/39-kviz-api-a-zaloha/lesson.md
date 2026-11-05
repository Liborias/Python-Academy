## Stejná data mohou přijít přes internet

API je rozhraní, přes které program žádá službu o data. Použijeme veřejnou [Open Trivia Database](https://opentdb.com/api_config.php). Adresa `https://opentdb.com/api.php?amount=5&type=boolean` žádá o pět otázek typu pravda/nepravda. Amount určuje počet, type druh otázky. Přihlášení ani API klíč zde nejsou potřeba.

Otázky této služby jsou v angličtině. České otázky v přiloženém souboru jsou vlastní offline obsah; program je automaticky nepřekládá. Uživatel si v příští lekci zdroj vybere. Výchozí nastavení použije místní soubor.

## Co stáhne stahni_json

Použijeme standardní urllib.request, json a předchozí převod, takže se neinstaluje další pip balíček:

```python
with urlopen(url, timeout=5) as odpoved:
    obsah = odpoved.read(MAX_BAJTU + 1)
```

`urlopen` otevře HTTP(S) požadavek. Parametr timeout nastaví čekání síťové operace na 5 sekund; není to celkový časový limit celé aplikace. `with` zajistí zavření odpovědi i při chybě. Chybný HTTP stav, například 503, urllib obvykle oznámí výjimkou.

Read vrací **bajty**, ne Python slovník. Povolíme nejvýš 65 536 bajtů, tedy 64 KiB. Načteme o jeden více, abychom poznali překročení hranice. Při větší odpovědi vyvoláme ValueError. `.decode("utf-8")` převede bajty na text a json.loads z něj sestaví data.

Stahni_json pouze stáhne a dekóduje. Funkce preved_otazky z minulé lekce zvlášť ověří, zda obsah skutečně odpovídá kvízu.

## Dva různé druhy neúspěchu

HTTP chyba popisuje přenos. Naproti tomu response_code uvnitř JSON patří službě Open Trivia DB: i při úspěšném přenosu může oznámit nedostatek otázek nebo omezení požadavků. Proto nestačí pouze přijmout HTTP odpověď. Chybný JSON, chybějící otázky nebo jiný response_code odmítne náš převod.

Funkce `ziskej_otazky(online=False, cesta="otazky.json", stahni=stahni_json)` vrátí tři hodnoty: seznam Otazka, název zdroje a případnou vysvětlující zprávu.

- Při online=False přečte zadaný místní soubor a vrátí zdroj offline a prázdnou zprávu. Funkci stahni vůbec nevolá.
- Při online=True zavolá stahni s API_URL a převede data. Úspěch vrátí zdroj API a prázdnou zprávu.
- Při OSError nebo ValueError přečte místní soubor, vrátí zdroj záloha a neprázdnou zprávu o příčině. Skutečný zdroj tak uživatel pozná.

Síťové chyby urllib i vypršení čekání patří pod OSError; vadný JSON, dekódování a naše validace patří pod ValueError. Nezachytáváme libovolnou chybu programu. Je-li vadná i místní záloha, chyba se předá volajícímu, který ji uživateli srozumitelně oznámí.

## Jak si API vyzkoušet bez náhodných výpadků

Parametr stahni je funkce, kterou můžeme vyměnit, podobně jako výběr potravy ve Snake. Předáme jí URL a ona vrátí dekódovaná data nebo vyvolá chybu. Logika výběru zdroje nemusí vědět, jak je funkce získala.

Ukázka postupně vyzkouší offline režim, úspěšné API simulované přiloženým api_ukazka.json a ukázkový výpadek. Všechny tři scénáře jsou opakovatelné. Soubor představuje vlastní testovací data ve stejném formátu, nikoli aktuální výsledek stažený ze služby.

Pro skutečné volání lze v místním projektu použít `ziskej_otazky(online=True)`. Připojení potřebuje přístup k doméně opentdb.com a služba může uplatnit omezení četnosti. Není třeba opakovaně klikat nebo měnit bezpečnostní nastavení aplikace: při běžném výpadku se použije záloha. V závěrečné aplikaci bude online režim výslovná volba api.

## Váš úkol

Doplňte stahni_json a ziskej_otazky podle popsaného rozhraní. Zachovejte API_URL a MAX_BAJTU. Funkce stahni_json přijímá URL jako argument, používá timeout, omezené čtení a uzavření odpovědi. Druhá funkce vybírá zdroj a přiznává použití zálohy; při offline volbě nepřistupuje k síti.

Kontroly používají připravené odpovědi a místní testovací zdroj. Jejich úspěch nezávisí na internetu, dostupnosti veřejné služby ani náhodném znění otázek. Ponechte kviz_model.py, kviz_data.py a otazky.json ve stejné pracovní složce jako svůj program.
