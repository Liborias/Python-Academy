## Proč přidáváme vlastní testy

V projektu už máme formulář, zprávu a ukládání. Teď si ověříme, že změna jedné části nepoškodí jinou. Testy v této lekci běží v konzoli, neotevírají okno a nepoužívají osobní schránku. Pomocné dilna.py obsahuje hotové uložení z lekce 24, prenos.py pracovníka z 23 a priprava.py sestavení zprávy z 22. Import jejich funkcí nespouští hlavní blok s oknem.

Budeme používat unittest ze standardní knihovny. Třída TestDilna dědí z unittest.TestCase, metody s názvem začínajícím test_ vyhledá testovací běh automaticky. Každá má vytvořit vlastní vstupy, provést operaci a ověřit pozorovatelný výsledek. Pořadí testů nemá být podmínkou úspěchu.

## Výsledek, výjimka a zachovaný stav

AssertEqual porovná hodnoty, assertTrue ověří pravdivou podmínku a `with self.assertRaises(ValueError)` vyžaduje uvedenou výjimku. Pouhé zavolání funkce bez ověření může projít i se špatným výsledkem. U neúspěšného uložení chceme ověřit jak vznik chyby, tak původní obsah souboru po ní.

TemporaryDirectory vytvoří vlastní dočasnou složku a po with ji odstraní. Path pomůže vytvořit cestu uvnitř, read_text/write_text s encoding="utf-8" určují kódování a read_bytes/write_bytes uchovávají přesné bajty přílohy. Díky vlastní složce testy nepoškodí vaše koncepty. SubTest pojmenuje průchod uvnitř cyklu, aby bylo z výsledku jasné, který vstup selhal.

První test uloží neúplnou adresu, mezery, více řádků a absolutní cestu zatím neexistující přílohy. To vše je platný koncept. Načtený model se má rovnat původnímu a vstup se nesmí změnit. Druhý test odmítne verzi True, verzi 2 a text s hodnotou 3. Připomeňte si, že True == 1, ale bool není platná verze tohoto formátu.

## Řízená chyba místo čekání na náhodu

Patch z unittest.mock dočasně nahradí konkrétní jméno a po with vrátí původní funkci. `patch("dilna.os.replace", side_effect=OSError("Cvičná chyba"))` vyvolá chybu v okamžiku nahrazení uloženého souboru. Potom skutečně přečteme disk a porovnáme starší obsah; ověříme také úklid dočasného souboru. Side_effect může být výjimka nebo funkce pro řízené chování.

Ve workeru nahrazujeme `prenos.odesli_do_zachytu`: místo skutečného spojení připravíme úspěch, odmítnutí příjemce a ztracené potvrzení. Nahrazuje se jméno v modulu, kde ho pracovník používá. `assert_called_once_with(...)` ověří jedno volání se správnou zprávou, hostem, portem a timeoutem. Get_nowait přečte stav z Queue a empty ověří, že pracovník nepřidal další výsledek.

Takový test ověřuje spolupráci kódu s rozhraním přenosu. Skutečné SMTP, vykreslení okna a chování kláves tím ještě ověřené nejsou. Tyto části mají samostatné běhové zkoušky a praktické scénáře v dalších lekcích.

## Snímek zprávy

Poslední test sestaví zprávu z textu a přílohy. Potom změní původní předmět i bajty souboru. Zpráva si má podržet původní Subject, tělo včetně mezer a původní přílohu. Ověřujeme veřejně přístupné části EmailMessage, ne názvy soukromých proměnných formuláře.

## Váš úkol

Napište alespoň pět metod v TestDilna pro popsané scénáře: přesný roundtrip neúplného konceptu s cestou přílohy, neplatné verze/typ, zachování staršího souboru při chybě, stavy a argumenty pracovníka a samostatný snímek. Použijte vlastní dočasná data a testy nepřeskakujte. Název pomocných lokálních proměnných ani rozdělení dalších metod nejsou předepsané.

Při přímém spuštění proveďte `unittest.main(verbosity=2)`. Unittest píše svůj běžný přehled na stderr, takže text OK v chybovém výstupním proudu sám neznamená chybu. Rozhoduje výsledek testů a návratový kód procesu.

Kontrola nejprve spustí vaše testy nad správnými moduly. Potom dočasně vloží osm známých chyb a ověří, že je testy skutečně odhalí. Prázdné testy proto nestačí. Zelený výsledek je důkazem ověřených scénářů, nikoli zárukou všech možných chování aplikace.
