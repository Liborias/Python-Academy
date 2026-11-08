## Kterou zprávu právě předáváme

Máme rozpracovaný koncept a umíme sestavit EmailMessage. Nyní propojíme formulář s místním SMTP záchytem z lekcí 18–20. Potřebujeme Tk, requests pro dřívější část kurzu a aiosmtpd pro záchyt. Příprava kurzu obsahuje instalační postup; ověřená kombinace je Python 3.14.8 a aiosmtpd 1.4.6. Záchyt se spouští jen na 127.0.0.1, zvolený port je volný a zprávy nikam nepřeposílá.

Po kliknutí Předat místnímu záchytu čteme pole i nastavení v hlavním vlákně. Sestav_zpravu z lekce 22 vytvoří samostatnou EmailMessage s právě načtenými bajty přílohy. Tento snímek pak předáme pracovníkovi. EmailMessage je měnitelný objekt; po předání jej už neměníme. Není to trvale propojený odkaz na obsah formuláře.

Uživatel může během čekání dál psát do příjemce, předmětu a těla. Odesílaný snímek i jeho náhled zůstávají původní. Po dokončení přenosu pole nevymažeme ani nepřepíšeme starými hodnotami. Další ruční pokus sestaví novou zprávu z aktuálního formuláře.

## Pracovník předává pouze výsledek

Funkce `predat_zpravu(zprava, host, port, timeout, fronta)` zavolá odesli_do_zachytu s přesně předanými argumenty. Přijme už připravený objekt, nepotřebuje Entry, Text, StringVar ani cestu přílohy. Při úspěchu vloží `fronta.put("prijato")`. Známe tyto další výsledky:

- SMTPRecipientsRefused → odmitnuto. Příjemce byl odmítnut před přijetím těla.
- SMTPServerDisconnected nebo TimeoutError → nejiste. Chybí potvrzení; zpráva už může být uvnitř.
- Ostatní SMTPException nebo OSError → chyba. GUI vysvětlí selhání služby nebo spojení.

Pořadí except je podstatné: konkrétnější SMTP chyby musí přijít před společnou SMTPException. Na každý průchod patří právě jeden výsledek do fronty. Funkce vrací None a původní zprávu nemění. Odesli_do_zachytu nadále vynucuje 127.0.0.1, platný port a konečný timeout do pěti sekund.

Thread dostane funkci v target, hotové argumenty v args a start spustí práci. Queue bezpečně předá krátký stav mezi vlákny. Callback vyzvedni přes get_nowait přečte výsledek; Empty znamená, že ještě není hotovo, a after naplánuje další kontrolu. Veškeré configure a práce s widgety zůstávají v hlavním vlákně.

## Ochrana před dvojím pokusem

Model má busy pro právě probíhající přenos a nutna_kontrola pro výsledek bez potvrzení. Busy kontrolujeme přímo v callbacku a současně zablokujeme tlačítka přílohy, ověření, přenosu a volby režimu. Formulář a Zkontrolovat záchyt zůstávají použitelné. Výsledek ovládání znovu povolí; žádný retry se sám nespustí.

Záchyt umí Přijetí, Odmítnutí příjemce a Opožděné potvrzení. V posledním režimu uloží zprávu a s odpovědí 250 počká 0,35 s. S běžným timeoutem 2 s přenos uspěje. Pro krátký pokus spusťte reseni.py přímo ze složky lekce v terminálu s Pythonem ze stejné .venv:

```powershell
$env:DILNA_SMTP_TIMEOUT = "0.05"
python reseni.py
Remove-Item Env:DILNA_SMTP_TIMEOUT
```

Na macOS/Linux použijte `DILNA_SMTP_TIMEOUT=0.05 python reseni.py`. Běžný běh přes web tyto vlastní SMTP proměnné nepředává. Prostředí se dědí při spuštění procesu, po změně program znovu spusťte. Port ponechte automatický. Před pokusem odstraňte dříve zadané vlastní DILNA_SMTP_HOST/PORT, pokud už neplatí.

Po nejistém výsledku další klik na přenos pouze vyzve ke kontrole. Zkontrolovat záchyt ukáže počet i předmět poslední zprávy a dovolí další vědomý pokus. Uživateli výslovně připomene možnost další kopie. Tato kontrola duplicity automaticky neodstraňuje a nezaručuje doručení do schránky. Zachycené zprávy žijí jen v paměti do ukončení programu.

## Váš úkol

Dokončete predat_zpravu. Použijte předaný objekt a nastavení, ošetřete uvedené výjimky a vložte právě jeden správný stav do fronty. GUI, sestavení zprávy i přenosový helper jsou připravené.

Vyplňte jan@example.test, předmět Původní snímek a krátký text. Zvolte Opožděné potvrzení, spusťte přenos a hned upravte předmět i tělo. Záchyt musí převzít původní snímek, zatímco nová práce v polích zůstane zachovaná. Vyzkoušejte odmítnutí a ruční úspěšný pokus. Potom spusťte program s krátkým timeoutem a vysvětlete, proč počet 1 může být současně s nejistým výsledkem.
