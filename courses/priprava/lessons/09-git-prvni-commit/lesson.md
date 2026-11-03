## Cíl
Uložit první místní verzi vlastního projektu. Git je nástroj pro historii; GitHub je služba pro sdílení repozitářů. Commit ještě nic nikam neodesílá.

## Praktický krok
Nainstalujte Git z [git-scm.com](https://git-scm.com/downloads) (Linux také správce balíčků distribuce) a ověřte `git --version`. Ve vlastní složce `moje-akademie` nejprve zkontrolujte, zda už není v repozitáři: `git status`. Jestli je, použijte pro tento pokus nový prázdný projekt; nepřepisujte jeho nastavení.

V novém projektu vytvořte `.gitignore`:
```text
.venv/
__pycache__/
*.pyc
.env
```
Následující údaje nahraďte svým jménem a e-mailem, který chcete mít v historii. Na GitHubu lze použít adresu noreply z nastavení účtu:
```bash
git init -b main
git config user.name "Vase jmeno"
git config user.email "vas-email@example.com"
git status
git add main.py README.md .gitignore
git diff --staged
git commit -m "Vytvoreni prvniho projektu"
git log --oneline
```
Konfigurace bez `--global` platí jen pro tento repozitář. Uvidíte pracovní kopii, připravené změny a commit. `.gitignore` nezneviditelní již sledovaný soubor ani nesmaže tajemství z historie. Do commitu nepřidávejte `.venv`, soukromé klíče nebo hesla.

## Co příkazy dělají a co se děje
`git --version` ověří dostupnost Gitu, ne přihlášení do GitHubu. `git init -b main` vytvoří místní historii v adresáři `.git` a hlavní větev pojmenuje main. `git config user.name` a `user.email` nastaví údaje autora pro tento repozitář; nejde o heslo ani síťové přihlášení.

`git status` vypíše stav pracovní kopie. `git add main.py README.md .gitignore` připraví aktuální podobu přesně těchto souborů pro příští commit. Změníte-li je po add, novou úpravu je nutné přidat znovu. `git diff --staged` ukáže připravené rozdíly. `git commit -m "..."` uloží místní snímek s popisnou zprávou. `git log --oneline` vypíše zkrácené identifikátory a zprávy historie. Úspěchem je nový commit a žádné nechtěné soubory v připravených změnách; samotný commit nic na síť neodesílá.

Řádky `.gitignore` jsou vzory pro dosud nesledované soubory: `.venv/` ignoruje prostředí, `__pycache__/` cache, `*.pyc` zkompilované moduly a `.env` soubor případné soukromé konfigurace. Git tím nemaže již uloženou historii.

## Vlastní ověření
- [ ] `git status` neukazuje `.venv` mezi soubory k přidání.
- [ ] Před commitem jsem prohlédl/a připravené změny.
- [ ] `git log --oneline` obsahuje můj první commit.
