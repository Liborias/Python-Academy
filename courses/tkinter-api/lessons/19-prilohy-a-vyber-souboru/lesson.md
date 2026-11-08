## Příloha je součást zprávy

EmailMessage umí uchovat více částí MIME: textové tělo a přílohy. Add_attachment potřebuje obsah, typ a název. V této lekci se nic neodesílá, soubor jen přidáme a zobrazíme jeho název, typ a velikost. Při kopírování mimo Akademii patří vedle programu zpravy.py z files. Pro zkoušku je v files i vlastní česká poznámka poznamka.txt.

## Čteme bytes a hlídáme velikost

```python
cesta = Path(cesta)
with cesta.open("rb") as soubor:
    data = soubor.read(MAX_PRILOHA + 1)
```

Path z pathlib představuje cestu a její name vrací pouze název souboru bez adresářů. Rb znamená čtení binárních dat, takže nic nepřekódujeme a nepotřebujeme encoding. Do přílohy se mají dostat původní bajty. Read s omezením nenačte libovolně velký soubor; jeden bajt navíc dovolí poznat překročení limitu. Prázdná příloha je platná. Pro toto cvičení je MAX_PRILOHA 1 000 000 bajtů, nikoli obecný limit e-mailových služeb.

Při neexistující cestě nebo složce místo souboru vznikne OSError. Překročení limitu odmítneme ValueError. V obou případech zůstane předaná zpráva beze změny: měníme ji teprve po úspěšném přečtení a ověření.

## MIME typ a název

Mimetypes.guess_type(cesta.name) odhadne typ podle přípony, například text/plain nebo image/png. Jde o odhad, nikoli ověření obsahu či jeho bezpečnosti. Druhá hodnota označuje případné kódování typu gzip. U neznámého typu nebo takového kódování použijeme obecné application/octet-stream.

`hlavni_typ, podtyp = typ.split("/", 1)` rozdělí typ na dvě části. Pak add_attachment dostane původní data, maintype, subtype a filename=cesta.name. Úplná místní cesta se do názvu přílohy neposílá. Knihovna připraví MIME obálku, přenosové kódování a český název; binární obsah zůstane při dekódování stejný.

Iter_attachments poskytne části, které jsou přílohami. Get_filename vrátí jejich název, get_content_type typ a get_payload(decode=True) původní bytes po dekódování. Len počítá bajty, ne počet písmen; český text v UTF-8 může mít bajtů víc než znaků.

List(kandidat.iter_attachments()) převede přílohy na seznam pro snadné indexování. Popisek velikosti používá jednotku B, tedy bajty. Funkci pridej_prilohu lze importovat bez vytvoření okna, protože samotné hlavni se volá až v hlavním bloku.

## Zrušení ani chyba nesmažou poslední přílohu

Dialog askopenfilename už znáte. Zrušení vrátí prázdnou cestu a skončí před čtením. Pro nový výběr vytvoříme kandidátní zprávu, teprve po úspěchu jí nahradíme aktuální model. Tím výběr dalšího souboru přílohu nahradí; nezačne hromadit všechny dříve zvolené soubory. Chyba ponechá předchozí náhled i přílohu.

Čitelný náhled ukazuje hlavičky a tělo. Přílohu shrnuje samostatný popisek, takže nemusíme číst zakódovaný obsah MIME. Vytvoření kandidáta a přiřazení přes celý řez seznamu znáte z úkolníčku.

## Váš úkol

Dokončete pridej_prilohu(zprava, cesta). Přečtěte omezený počet bajtů, před změnou zprávy ověřte velikost, určete typ a připojte přesný obsah s názvem souboru bez cesty. Vraťte tentýž objekt zprávy. Na chybě jej neměňte, tělo i hlavičky zachovejte. Ostatní části GUI jsou připravené.

Vyberte poznamka.txt, zkuste jiný soubor, potom dialog zrušte a zvolte neexistující či příliš velký soubor. Při úspěchu má být právě jedna nová příloha, při zrušení a chybě zůstane poslední platný výběr. Tento náhled ještě nic neodesílá.
