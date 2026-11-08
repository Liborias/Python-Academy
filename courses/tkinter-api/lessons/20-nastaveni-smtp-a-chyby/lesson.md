## Nastavení oddělíme od programu

Host, port a čas čekání nemusí být rozeseté v kódu. Os.environ je mapování proměnných prostředí procesu. Hodnoty jsou texty, takže port převádíme pomocí int a timeout pomocí float. Get dovolí výchozí hodnotu, když proměnná chybí. Nacti_nastaveni(prostredi, vychozi_port) dostává mapování jako argument, díky čemuž se dá ověřit i bez skutečné změny systému.

Používáme DILNA_SMTP_HOST, DILNA_SMTP_PORT a DILNA_SMTP_TIMEOUT. Výchozí host je 127.0.0.1, port vybere právě spuštěný záchyt a timeout je 2 sekundy. Připravené over_spojeni z lekce 18 vynutí místní adresu, port 1–65535 a konečný kladný timeout nejvýše 5 sekund. Konfigurace tak nemůže z tohoto cvičení udělat odesílání do cizí schránky.

Zápis `all(isinstance(v, str) for v in (...))` ověří postupně všechny tři hodnoty. All vrátí True, jen když každá podmínka vyjde pravdivě. Tím ještě před převody odmítneme jiný typ než text. V popisku nastavení formát :g zobrazí například 2 místo 2.0; jde o obecný číselný formát, nikoli změnu uložené hodnoty timeoutu.

Toto není úplný klient veřejné poštovní služby. U skutečného poskytovatele by bylo nutné ověřit jeho server a port, použít ověřené TLS (například STARTTLS s výchozím ověřováním certifikátu nebo SMTP_SSL) a podporovaný způsob přihlášení. Heslo či token nepatří do zdrojového kódu ani Git repozitáře. Tady se nepřihlašujeme a osobní údaje ke schránce nepotřebujeme; změna na veřejnou službu není součástí spustitelné ukázky.

## Jak nastavení vyzkoušet

Spouštěný program dědí prostředí terminálu. Pro kratší čekání v PowerShellu:

```powershell
$env:DILNA_SMTP_TIMEOUT = "0.05"
python reseni.py
Remove-Item Env:DILNA_SMTP_TIMEOUT
```

Na macOS/Linux lze použít `DILNA_SMTP_TIMEOUT=0.05 python reseni.py`, což hodnotu nastaví jen pro tento proces. Python musí být ze správné .venv. Při práci přes prohlížeč zdědí ukázka jen proměnné, které výukový server dovolí: tuto konfiguraci proto zkoušejte přímo v terminálu nad souborem reseni.py nebo v prostředí editoru. Změna v jiném terminálu už běžícímu programu prostředí nezmění; spusťte jej znovu. Před koncem cvičení odstraňte i další vlastní DILNA_SMTP_* proměnné.

Port při tomto pokusu nenastavujte, výchozí hodnota přijde z aktivního místního serveru. Neplatný text, nula nebo cizí host se odmítne před spojením. Když zadáte jiný neobsazený místní port, nastavení může být syntakticky platné, ale spojení selže. To jsou dvě různé chyby.

## Přijetí a odmítnutí

Při Přijetí server vrátí úspěšné potvrzení, počet v záchytu vzroste a náhled ukáže zachycenou zprávu. V režimu Odmítnutí příjemce server odmítne krok RCPT ještě před DATA. S jediným příjemcem se tělo nepředá a SMTPRecipientsRefused zobrazíme jako odmítnutí. Nejde o chybu Python syntaxe.

Stejně jako u API běží přenos v pracovním vlákně, fronta předá jen stav a after zpracuje výsledek v hlavní smyčce. Po dobu přenosu je tlačítko i změna scénáře disabled. Po skončení se ovládání povolí. Tlačítko Zkontrolovat záchyt zůstává použitelné i během čekání.

## Timeout nemusí znamenat, že zpráva nebyla převzata

Opožděné potvrzení je záměrná ukázka této hranice: místní server už zprávu uloží, ale s odpovědí 250 počká 0,35 s. S výchozím timeoutem obvykle uspěje. S timeoutem 0.05 může klient ztratit spojení dřív než potvrzení přijde. Smtplib takové čekání při čtení odpovědi může ohlásit také jako SMTPServerDisconnected, ne jen TimeoutError.

Program proto řekne Přenos není potvrzený. Před novým pokusem zkontrolujte záchyt. Nepíše, že se určitě nic nestalo, a automaticky neopakuje odeslání. Zkontrolujte počet a náhled: zpráva už může být uvnitř. Opakování by mohlo vytvořit další kopii. Ani Message-ID samo nezaručuje, že server duplicitu odmítne.

Zachycené zprávy zůstávají jen v paměti tohoto cvičného serveru, ne v doručené poště. Konec programu je smaže.

## Váš úkol

Dokončete nacti_nastaveni: přečtěte uvedené proměnné s výchozími hodnotami, povolte krajní mezery, převeďte port a timeout na čísla a zavolejte over_spojeni. Vraťte slovník host, port, timeout. Zadané hodnoty mapování neměňte. Neplatné hodnoty odmítněte ValueError. Zbytek GUI, pracovního vlákna a zpráv je připravený.

Vyzkoušejte normální přijetí, odmítnutí a nový úspěšný pokus. Potom v terminálu spusťte program s krátkým timeoutem a vyberte Opožděné potvrzení. Vysvětlete, proč přírůstek v záchytu a chybějící potvrzení mohou nastat současně a proč program sám nevytváří další pokus. Při každé změně konfigurace zkontrolujte také zobrazený host, port a timeout.
