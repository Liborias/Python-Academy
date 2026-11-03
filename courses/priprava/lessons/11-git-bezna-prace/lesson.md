## Cíl
Dělat malé srozumitelné změny, prohlížet rozdíly a oddělit pokus do větve.

## Praktický krok
V čistém vlastním repozitáři změňte pozdrav v `main.py`:
```bash
git status
git diff
git switch -c uprava-pozdravu
git add main.py
git diff --staged
git commit -m "Uprava pozdravu"
git switch main
git merge uprava-pozdravu
git log --oneline --graph --all
git push
```
Větev je pojmenovaný ukazatel do historie, ne kopie `.venv`. Před přepnutím zkontrolujte neuloženou práci pomocí `git status`. Nechcete-li změny odeslat, skončete před push.

Pro stažení změn na čisté hlavní větvi použijte `git pull --ff-only`. Pokud historie nejde posunout přímo, příkaz se zastaví; nejprve prozkoumejte obě historie pomocí `git log --oneline --graph --all`. Neřešte to force push nebo mazáním své práce.

Koncept dalšího procvičení: na dvou větvích změnit stejný řádek a vyřešit konflikt. Při konfliktu upravíte označená místa do výsledného textu, spustíte program, dáte `git add` a dokončíte merge commitem. Pokud si nejste jisti a máte uchovanou práci, `git merge --abort` vrátí nedokončené slučování. Samostatné cvičení konfliktu se doplní později.

## Co příkazy dělají a co se děje
`git diff` porovná nepřipravené změny s připravenou podobou; `git diff --staged` porovná připravenou podobu s posledním commitem. `git switch -c uprava-pozdravu` vytvoří novou větev a přepne do ní. Po add a commit je úprava uložená na této větvi. `git switch main` přepne zpět a pracovní soubory se podle historie změní. Proto přepínejte se zkontrolovaným stavem.

`git merge uprava-pozdravu` začlení tuto větev do právě otevřené main. Při jednoduchém postupu jen posune její ukazatel; při odlišných změnách může vytvořit slučovací commit nebo požádat o řešení konfliktu. `git log --oneline --graph --all` ukáže souvislosti všech větví. `git push` odešle změny na dříve nastavený upstream.

`git pull --ff-only` stáhne vzdálenou historii a přijme ji jen tehdy, když stačí přímý posun místní větve. Odmítnutí znamená potřebu rozhodnout o rozdílných změnách, nikoli pokyn k mazání. `git merge --abort` ukončí rozpracované slučování; nepoužívejte ho jako obecné „zpět“ pro hotové commity.

## Vlastní ověření
- [ ] Umím vysvětlit rozdíl mezi add, commit, push a pull.
- [ ] Prohlédl/a jsem diff před commitem.
- [ ] Větev s úpravou je sloučená a program stále funguje.
