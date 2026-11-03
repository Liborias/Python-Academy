## Cíl
Porozumět klientovi, serveru, portu a pracovní složce na bezpečném malém statickém webu. Tento pokus není nasazení veřejné aplikace.

## Praktický krok
Ve vlastním projektu vytvořte složku `public` a soubor `public/index.html` s textem:
```html
<!doctype html>
<html lang="cs"><meta charset="utf-8"><title>Můj projekt</title>
<h1>Server funguje</h1></html>
```
Z kořene vlastního projektu spusťte Windows:
```powershell
.\.venv\Scripts\python.exe -m http.server 8000 --bind 127.0.0.1 --directory public
```
Na macOS/Linux nahraďte první část cestou `./.venv/bin/python`. V prohlížeči otevřete `http://127.0.0.1:8000`. Očekávejte nadpis Server funguje. Změňte HTML, uložte a obnovte stránku. Server zastavte Ctrl+C a ověřte, že už neodpovídá.

`127.0.0.1` označuje tento počítač. Port 8000 rozlišuje programy, které na něm poslouchají. Při obsazeném portu použijte 8001 v příkazu i adrese. Server zpřístupňuje jen adresář `public`; nedávejte do něj `.env`, klíče ani osobní data.

Dílna používá vlastní `start.py`, jiný port a API pro spouštění Pythonu. Statický http.server neumí její kontrolu úkolů ani API a nenahrazuje ji. Ani jeden z těchto výukových serverů není určený k veřejnému provozu.

## Co příkazy dělají a co se děje
`-m http.server` spustí modul jednoduchého webového serveru. Číslo `8000` je port, na kterém čeká na požadavky. `--bind 127.0.0.1` omezí naslouchání na tento počítač a `--directory public` určí složku zveřejněných souborů. Server čte HTML, neprovádí ho jako Python. Prohlížeč vyšle požadavek, server odešle obsah `index.html` a prohlížeč jej vykreslí.

HTML značka `<h1>` vytváří hlavní nadpis, `<title>` text záložky a `charset="utf-8"` správné zobrazení diakritiky. Změna souboru se projeví až při dalším načtení stránky. Po Ctrl+C už tento proces neobsluhuje požadavky; prohlížeč může stále ukazovat dříve načtenou stránku, proto spojení ověřte obnovením.

## Vlastní ověření
- [ ] Místní adresa ukáže právě můj `public/index.html`.
- [ ] Vím, který terminál drží server, a umím ho zastavit.
- [ ] Změna portu vyžaduje změnu adresy v prohlížeči.
