# Praktické zkoušky projektu

Provádějte na vlastní pracovní kopii a s cvičnými soubory. Spusťte python aplikace.py. Tato část ověřuje skutečné okno; test_projekt.py ji nenahrazuje.

- [ ] Načíst ukázku funguje i při spuštění z jiného pracovního adresáře. Po ověření je náhled pouze ke čtení.
- [ ] Prázdný příjemce, předmět a tělo postupně ohlásí konkrétní chybu s fokusem. Pole se neztratí.
- [ ] Výběr přílohy, nový výběr, zrušení a chybějící či příliš velký soubor zachovají odpovídající stav. Limit je 1 000 000 B.
- [ ] Ctrl+S z těla otevře právě jeden dialog. Ctrl+O obnoví přesné řádky bez vloženého znaku. Ctrl+Enter jen ověří náhled, záchyt zůstane prázdný.
- [ ] Neúplný koncept lze uložit a načíst včetně mezer a cesty přílohy. Zrušení a vadný JSON zachovají text, přílohu i náhled.
- [ ] V režimu Odmítnutí příjemce se zpráva nezachytí. V režimu Přijetí lze provést nový ruční pokus.
- [ ] Během Opožděného potvrzení zůstane okno použitelné. Druhý klik, souborové zkratky a Načíst ukázku nespustí další operaci. Nové psaní po dokončení zůstane zachované.
- [ ] Změna souboru přílohy během čekání nezmění již připravený snímek. Další ruční pokus načte nové bajty.

## Krátký timeout

Ukončete aplikaci a přímo v terminálu spusťte:

```powershell
$env:DILNA_SMTP_TIMEOUT = "0.05"
python aplikace.py
Remove-Item Env:DILNA_SMTP_TIMEOUT
```

Na macOS/Linux lze použít DILNA_SMTP_TIMEOUT=0.05 python aplikace.py. Nepřepisujte automatický port a odstraňte dříve nastavené DILNA_SMTP_HOST/PORT, pokud už neplatí. Vlastní SMTP proměnné nezkoušejte v běžném webovém běhu výukové aplikace; ten je nepředává.

- [ ] Opožděné potvrzení může skončit nejistým výsledkem, ačkoli záchyt obsahuje jednu zprávu. Žádný automatický druhý pokus nenastane.
- [ ] Další předání vyžaduje Zkontrolovat záchyt. Načtení jiného konceptu tuto potřebu nesmaže. Další vědomý pokus může vytvořit kopii.
- [ ] Po novém spuštění je záchyt prázdný, uložený koncept se přesto obnoví ze souboru.

## Pokud sestavujete

- [ ] Ověřte celou distribuční složku na cílovém systému. Přesuňte kopii výsledku a spusťte ji z jiného pracovního adresáře, načtěte přibalenou ukázku a uložte vlastní koncept mimo balíček.
- [ ] Doplňte do README skutečně použité verze a výsledky. Neověřený systém označte jako neověřený.
