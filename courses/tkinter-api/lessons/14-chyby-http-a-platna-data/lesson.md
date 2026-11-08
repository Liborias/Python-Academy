## Tři různé příčiny neúspěchu

Server může být nedostupný, může vrátit chybový HTTP stav, nebo odpoví 200 s nepoužitelným tělem. Rozlišujeme proto přenos, rozebrání JSON a ověření jeho obsahu. Úspěšný stav 200 neznamená, že uvnitř přišel správný kurz.

Requests.Timeout znamená překročené čekání a je potomkem requests.RequestException. RequestException pokrývá také chybu spojení nebo HTTPError z raise_for_status. Poškozené JSON může vyvolat requests.exceptions.JSONDecodeError, která je současně potomkem ValueError i RequestException. Proto v ukázce kontrolujeme ValueError před obecnou RequestException, aby poškozený JSON dostal zprávu o datech. Náš over_kurz pro nesprávný obsah vyvolává ValueError. Nechytáme každou Exception, aby se programátorská chyba neskrývala jako běžný výpadek služby.

Funkce nacti_kurz chyby předává volajícímu. Konzolový hlavní blok je zobrazí a pokračuje dalším připraveným pokusem. Nevymýšlí náhradní kurz a nekonečně neopakuje neúspěšný požadavek.

## Co musí platný kurz obsahovat

Over_kurz(data, mena) dostane rozebraná data a očekávanou měnu. Ta se normalizuje přes strip().upper(). Slovník musí mít právě odpovídající mena, číselný czk_za_jednotku větší než nula a konečný, datum a neprázdný textový zdroj. Bool za kurz nepřijímáme: v Pythonu se chová také jako celé číslo, ale True není kurz 1 CZK. Proto se ověřuje dřív než isinstance(..., (int, float)). Math.isfinite znáte z převodníku vzdálenosti. Číselný kurz nejprve převedeme na float; příliš velké celé číslo může vyvolat OverflowError, kterou přeložíme na ValueError jako neplatná data. Pracujeme s konečnými hodnotami v rozsahu float.

Datum má být skutečný den v přesném tvaru RRRR-MM-DD. `from datetime import date` načte typ kalendářního data. Date.fromisoformat(datum) zkusí text rozebrat a například 2026-02-30 odmítne. Metoda isoformat() jej zapíše v běžném tvaru; porovnáním s původním textem odmítneme i jiné zkrácené zápisy, které Python jinak umí přečíst. Před rozebráním zkontrolujeme typ str.

Funkce vrátí nový slovník se čtyřmi očekávanými údaji a odstraní krajní mezery ze zdroje. Klíče navíc ignoruje, původní data nemění. Platné historické datum přijímáme; nejde automaticky o kurz platný dnes. Zdroj a datum budou proto v okně vidět.

U překladu OverflowError používáme `raise ValueError(...) from None`. Nová výjimka tím dostane naši srozumitelnou zprávu a při běžném výpisu se nezobrazuje předchozí výjimka jako navazující kontext. Ověření ani typ nové výjimky se tím nemění.

## Časový limit patří k požadavku

Nacti_kurz má nově parametr timeout=2. Předá jej requests.get, takže volající může zvolit kratší čekání pro konkrétní službu nebo test. Časový limit neřeší zamrzání hlavní smyčky: synchronní get stále čeká ve vlákně, které jej zavolalo. V další lekci jej přesuneme do pracovníka.

Pomocný server umí prefixy /chyba (503), /neplatny-json a /spatna-data (záporný kurz). /pomalu odpoví až po 0,35 s; s timeout=0.05 vyzkoušíte Timeout. Tyto režimy jsou součást místního cvičení, žádná cizí služba se nezatěžuje.

## Váš úkol

Dokončete over_kurz. Vraťte nový slovník mena, czk_za_jednotku, datum, zdroj podle popsaných pravidel; neplatný záznam odmítněte ValueError. Nacti_kurz už použije tuto funkci po ověření HTTP stavu a rozebrání JSON. Původní slovník ponechte nedotčený. Přijměte i klíče navíc, celé kladné číslo a platný historický den.

Spusťte ukázku se třemi různými chybami a následným úspěchem. Vysvětlete, ve kterém kroku se každá chyba projeví. Potom přidejte vlastní pokus s /pomalu a kratším timeoutem. Zadaný kurz se při neúspěchu nenahrazuje nulou ani hodnotou z předchozího pokusu.
