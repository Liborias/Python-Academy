## Sestavit zprávu není totéž co ji odeslat

EmailMessage je objekt standardní knihovny pro hlavičky, tělo a později přílohy. V této lekci zprávu pouze vytvoříme a zobrazíme; žádné spojení se schránkou ani serverem nevzniká. Adresy eva@example.test a jan@example.test jsou cvičné. Doména .test je vyhrazená pro testování, není to adresa skutečného příjemce.

Hlavičky nastavujeme podobně jako položky slovníku: From je odesilatel, To příjemce a Subject předmět. Nejde o přihlášení k účtu a From sám nijak nedokazuje vlastnictví adresy. SMTP později použije také samostatnou obálku přenosu; hlavičky jsou součástí samotné zprávy.

## Jedna adresa a jedna řádka předmětu

Připravená funkce over_adresu přijme jednu textovou adresu, odstraní krajní mezery a nechá její tvar rozebrat přes Address(addr_spec=...). Address má username a domain, oba vyžadujeme. Neověřuje však existenci schránky ani doručitelnost. Pro tuto výuku používáme adresy ASCII; isascii() kontroluje, že neobsahují znaky mimo tuto základní sadu. České jméno do adresy nepíšeme, čeština bude v předmětu a těle. Mezinárodní adresy by potřebovaly další pravidla SMTPUTF8.

Do hlaviček nepřijímáme \r ani \n. Nový řádek by mohl změnit jejich význam či přidat jinou hlavičku. Předmět je navíc po odstranění krajních mezer neprázdný. Tělo smí mít více řádků a může být i prázdné. HeaderParseError a ValueError při rozebrání adresy překládáme na srozumitelnou ValueError; from None už znáte z ověřování API.

## Kódování necháme knihovně

```python
zprava = EmailMessage(policy=SMTP)
zprava["Subject"] = predmet.strip()
zprava.set_content(text, charset="utf-8")
```

Policy SMTP nastavuje podobu zprávy pro běžný SMTP přenos, včetně konců řádků CRLF. Set_content nastaví textové tělo a jeho kódování. Není potřeba ručně sestavovat MIME ani kódovat český předmět do speciálních hlaviček. As_string zprávu serializuje do přenosové podoby; náhled pro člověka naopak ukazuje rozkódované hodnoty.

Před set_content sjednotíme CRLF/CR vstupního textu na LF. Knihovna doplní koncový nový řádek těla, pokud chybí; ani prázdné tělo tak při get_content není úplně prázdný řetězec. V síťové podobě se konce řádků opět zapíší podle SMTP politiky. Po přenosu může parser vrátit CRLF, proto při porovnávání obsahu rozlišujeme text od způsobu zápisu konců řádků.

Připravené Date a Message-ID přidávají datum s časovým pásmem a jedinečný identifikátor. Formatdate(localtime=True) používá místní čas. Make_msgid vytvoří ID s cvičnou doménou; ID není potvrzení o doručení. Nahled_zpravy přes get_body(preferencelist=("plain",)) najde prosté textové tělo a get_content jej přečte. N-tice s jedním prvkem má opět čárku.

## Váš úkol

Ve vytvor_zpravu doplňte From, To, Subject a set_content. Ověření vstupů, datum, identifikátor i náhled jsou připravené. Funkce vrací EmailMessage, nikoli jeho vytištěný text. Zachovejte diakritiku a vnitřní mezery, předmět ořízněte jen na krajích, v těle sjednoťte konce řádků a použijte UTF-8.

Spusťte ukázku a porovnejte čitelný náhled se serializací. Jiný zápis předmětu v přenosu není ztráta češtiny: příjemce jej zase dekóduje. Zkuste prázdné tělo, nový řádek uprostřed těla a odmítnutý nový řádek v předmětu. Nic se zatím neodesílá.
