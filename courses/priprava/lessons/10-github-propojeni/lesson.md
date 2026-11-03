## Cíl
Propojit existující místní repozitář s vlastním vzdáleným repozitářem. Žádný repozitář aplikace nevytváří automaticky.

## Praktický krok
1. Přihlaste se na [GitHub](https://github.com/) a přes New repository vytvořte vlastní repozitář. Rozmyslete viditelnost; pro první pokus zvolte Private. Název například `moje-akademie`.
2. Protože už máte místní commit, na GitHubu nepřidávejte další README, licenci ani .gitignore. Vznikne prázdný repozitář.
3. Zkopírujte HTTPS adresu svého repozitáře. V příkazech níže nahraďte `VAS-UCET` a případně název projektu skutečnými údaji:
```bash
git remote -v
git remote add origin https://github.com/VAS-UCET/moje-akademie.git
git push -u origin main
```
Pokud už origin existuje, nejdřív zjistěte, na co ukazuje; nepřidávejte a nepřepisujte ho slepě. Přihlášení řešte podporovaným správcem přihlašovacích údajů Gitu nebo přihlášením editoru přes prohlížeč. GitHub pro HTTPS nepřijímá běžné heslo k účtu. Tokeny nevkládejte do adresy remote, zdrojového kódu, screenshotu ani chatu.

Alternativa je SSH klíč nastavený podle [dokumentace GitHubu](https://docs.github.com/en/authentication/connecting-to-github-with-ssh). Vyberte jeden způsob; pro začátek stačí HTTPS. Po push otevřete GitHub a porovnejte poslední commit i obsah. Změna na webu není automaticky změnou na disku.

## Co příkazy dělají a co se děje
`git remote -v` vypíše pojmenované vzdálené adresy pro čtení a odesílání. `git remote add origin ADRESA` uloží do místní konfigurace adresu pod přezdívkou origin; teprve tím ještě nic neodesílá ani nevytváří na GitHubu. Webové vytvoření repozitáře a místní přiřazení adresy jsou dva samostatné kroky.

`git push -u origin main` naváže spojení, ověří vaše oprávnění a odešle místní větev main na origin. Volba `-u` nastaví její sledovanou vzdálenou větev pro další push/pull. Při úspěchu uvidíte commit na webu. Odmítnutí přístupu není ztráta místního commitu; ověřte adresu, účet a oprávnění. Přihlášení správcem údajů či SSH klíčem potvrzuje vaši identitu službě GitHub, zatímco token z předchozí lekce patřil jen místnímu učebnímu serveru.

## Vlastní ověření
- [ ] Viditelnost a vlastník repozitáře odpovídají mému záměru.
- [ ] `git remote -v` ukazuje můj repozitář bez tajných údajů.
- [ ] Commit z počítače se zobrazil i na GitHubu.
