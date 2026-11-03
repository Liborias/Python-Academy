# Koncept podkurzu: Začínáme – prostředí, projekt a Git

Podkurz patří na první místo Python Akademie / Dílny Pythonu. Je samostatný a nic neblokuje. Určen je začátečníkovi, který ještě neví, jaký nástroj co dělá. Výsledkem má být malý vlastní projekt, který student umí vytvořit, spustit, verzovat a obnovit na jiném stroji.

Aktuální dodávka je **koncept**, ne kompletní výukový kurz s automatickými úlohami. Obsahuje 15 čitelných návrhů lekcí s cíli, praktickými kroky a vlastním ověřením. Správnost instalace editoru, přihlášení do GitHubu nebo přístupu na VPS nelze prokázat zaškrtnutím v aplikaci. Neprovádíme automatické instalace ani založení účtů.

| Modul | Lekce | Výstup |
|---|---|---|
| Orientace a nástroje | 01 Co je Python, editor, projekt a server; 02 Instalace a ověření Pythonu; 03 VS Code, VSCodium nebo PyCharm | Student zná svůj interpreter a vybere jeden editor. |
| Vlastní projekt a podkurzy | 04 Nový projekt; 05 venv, pip a závislosti; 06 Příprava podkurzu; 07 Spuštění a ladění | Malý projekt s README, vlastní .venv, reprodukovatelný start. |
| Místní server a token | 08 localhost, port a statický web; 09 spuštění main.py přes ověřený požadavek | Stránka dostupná jen místně; student umí server zastavit. |
| Git, GitHub a obnova | 10 status, add, diff, commit; 11 GitHub a remote; 12 větve, pull, merge; 13 clone a obnova prostředí | Historie, vlastní remote a funkční nová kopie projektu. |
| Virtuální server (volitelné) | 14 Linux VM/VPS, SSH a tunel; 15 od pokusu k nasazení | Skript na jiném stroji, statický web přes tunel a konkrétní plán chybějících provozních kroků. |

## Didaktická návaznost

Nejprve použitelné minimum: Python, editor, soubor a jeho spuštění. Teprve potom balíčky a izolace, ještě později Git a síťové pojmy. Praktickým vláknem je vlastní složka `moje-akademie` s `main.py`, README a později statickým webem `public/index.html`. Není to nový obsah Základů ani přepis existujících navazujících projektů.

Windows používá PowerShell a launcher `py -3.14`; macOS/Linux `python3`. Vlastní prostředí se vždy ověřuje přes přesnou cestu k jeho Pythonu. Editor se dá volit a měnit bez změny projektu. Volba OS je nezávislá na volbě editoru. Návody se soustředí na místní vývoj; GUI hry, Turtle a Tkinter se nepřesouvají na server bez grafické plochy.

## Příprava u každého podkurzu

Před seznamem lekcí je rozbalitelná příprava. Balíčky se berou ze stejného zdroje jako `tools/setup_env.py`, aby se návod nerozcházel s instalací. Každý profil obsahuje účel balíčků, požadavky mimo pip, importní ověření, výběr interpreteru a spuštění Dílny. Funguje i u podkurzů, jejichž lekce jsou teprve plánované; jejich stav se nemění.

Výběr editoru a OS se pamatuje v prohlížeči. Vlastní potvrzení připravenosti je oddělené podle podkurzu a zvoleného prostředí; nezamyká lekce. Virtuální server se nenabízí jako předpoklad běžného kurzu.

## Rozsah dalšího dopracování

Příští samostatná práce může doplnit vyzkoušené snímky a kroky pro konkrétní verze editorů, samostatné cvičení Git konfliktu, obnovu ze zálohy a konkrétní nasazení vybraného backendového frameworku včetně služby, HTTPS a testu po restartu. Než se koncept označí jako hotový kurz, má ho projít začátečník na Windows/macOS/Linux.

Veřejné nasazení není přejmenovaný `http.server`. V konceptu slouží server jen k názornému pochopení klienta, portu a SSH tunelu. Dílna sama vykonává studentský kód a nemá být veřejně dostupným výukovým serverem. Konfiguraci skutečného nasazení je nutné připravit pro konkrétní aplikaci.

## Doplnění v0.36: porozumění příkazům a token

Každý dosavadní průvodce nyní obsahuje samostatné vysvětlení příkazů, jejich argumentů,
změn na disku nebo v procesu a očekávaného výsledku. Vysvětlení zahrnuje rozdíl
mezi systémovým Pythonem, interpreterem .venv, instalací balíčků, pracovním
adresářem, serverem, tokenem a přihlášením ke GitHubu.

Nová devátá lekce je za místním serverem a před Gitem. Obsahuje tři přiložené
soubory v `courses/priprava/lessons/09-server-a-token/files`: pevný main.py,
místní token_server.py a token_client.py. Student nejprve ověří přímý běh z .venv,
potom server a klienta ve dvou terminálech, správný/chybný token i restart.
Tlačítko prohlížeče je vysvětleno jako jiný klient stejného principu; ukázka
zatím používá Python klienta a nevyžaduje znalost JavaScriptu.

Původní id lekcí se zachovala kvůli odkazům a uloženému postupu. Zobrazované číslo
určuje pořadí v course.json, takže Git začíná číslem 10 a volitelný VPS číslem 14.
