## Přenos do schránky na vlastním počítači

SMTP je protokol pro předání e-mailu serveru. Zde přijímající server běží pouze na 127.0.0.1, ukládá zprávy do paměti a nikam je nepředává. Nemusíte zadávat osobní adresu, heslo ani povolovat přístup ke schránce. Po skončení programu se zachycená data ztratí.

Klient smtplib je ve standardní knihovně. Pro serverový záchyt přibyl balíček aiosmtpd, ověřený ve verzi 1.4.6 na Pythonu 3.14.8. Modul smtpd už v tomto Pythonu není. V projektové .venv použijte `python -m pip install "aiosmtpd>=1.4.6,<2"`; případně znovu spusťte přípravu podkurzu. Ověření importu: `python -c "import aiosmtpd; print(aiosmtpd.__version__)"`.

Vedle programu patří cvicna_posta.py a zpravy.py. První obsahuje místní serverový pomocník, druhý je přesná kopie předchozího řešení. `with cvicna_posta() as posta` server spustí na volném portu a při opuštění bloku jej ukončí. Posta.host/port jsou skutečně zvolená adresa a port; port nezapisujeme natvrdo. Posta.zpravy vrací kopii seznamu zachycených záznamů, ne skutečnou internetovou schránku.

## Co provede klient

```python
with smtplib.SMTP(host, port, timeout=timeout, local_hostname="localhost") as klient:
    odmitnuti = klient.send_message(zprava)
```

SMTP otevře spojení a přečte úvodní pozdrav serveru. Local_hostname zde jen pojmenuje klienta v protokolu a vyhne se hledání názvu počítače. Send_message předá EmailMessage: knihovna vyřeší pozdrav EHLO, obálku MAIL FROM/RCPT TO i přenos DATA. Ukončovací tečku a zdvojení tečky na začátku řádku také řeší smtplib, do textu zprávy je nevkládáme ručně.

With při úspěšném odchodu pošle QUIT a spojení zavře; úklid zajistí i při chybě. Timeout omezuje čekání na síťové operace, není to přesný celkový limit všech kroků. Bez timeoutu nechceme čekat neomezeně.

Prázdný slovník vrácený send_message znamená, že server neodmítl žádnou z adres obálky. Neznamená to přečtení zprávy ani konečné doručení do schránky. Při odmítnutí všech adres může vzniknout SMTPRecipientsRefused; při částečném odmítnutí může být vrácen neprázdný slovník, který v našem cvičném klientu také odmítáme. Náš model má jediného příjemce.

## Zkontrolujeme skutečně přenesená data

Zachycený záznam obsahuje odesilatel a prijemci z SMTP obálky a data jako bytes. BytesParser(policy=default).parsebytes(data) je rozebere zpět na zprávu. Náhled opět ukáže český předmět i tělo. Přenosové CRLF konce řádků se mohou lišit od LF v původním textu; obsah zůstává stejný.

Připravené over_spojeni povolí pouze 127.0.0.1, port 1–65535 a kladný konečný timeout do 5 sekund. Je to klient pro místní cvičení, ne obecný nástroj k připojování na libovolný SMTP server. Ověření proběhne před otevřením spojení.

## Váš úkol

Dokončete odesli_do_zachytu. Použijte předaný host, port, timeout a stejný objekt zprávy, SMTP jako kontextový správce a send_message. Neprázdné odmitnuti převeďte na SMTPRecipientsRefused. Po přijetí funkce vrátí None; chyby neskrývá, aby je mohl ošetřit volající.

Spusťte ukázku, ověřte Zachyceno: 1, obálku i text začínající tečkou. Tato tečka se nesmí ztratit ani zdvojit v rozebraném těle. Vysvětlete rozdíl mezi From/To ve zprávě, SMTP obálkou a potvrzením serveru. Nic se neposílá mimo místní záchyt.
