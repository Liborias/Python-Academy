## Z konceptu vznikne připravená zpráva

Navážeme na formulář z lekce 21. Pomocný koncept.py obsahuje její hotový model, zpravy.py řešení lekce 17 a prilohy.py řešení lekce 19. Při otevření lekce v editoru se zkopírují vedle reseni.py. Import jejich funkcí neotevře pomocná okna: blok `if __name__ == "__main__"` se při importu neprovede.

Funkce `sestav_zpravu(koncept)` vytvoří novou EmailMessage. Koncept ponechá beze změny. Pořadí ověření je struktura konceptu, příjemce, předmět, tělo a příloha. Zobrazíme první chybu, kterou může uživatel opravit, a po dalším kliknutí zkontrolujeme aktuální údaje znovu.

## Chyba ví, ke kterému poli patří

Přidáme malý vlastní typ chyby `ChybaPole(ValueError)`. Zápis v závorkách znamená dědění: ChybaPole se dá zachytit i jako ValueError. V __init__ zavoláme `super().__init__(zprava)`, čímž předáme popis běžné výjimce; `self.pole = pole` navíc uloží označení problematického pole. Callback pak použije `str(chyba)` pro zprávu a chyba.pole pro fokus. Zápis `raise ... from None` skryje řetězec původní chyby, kterou už jsme přeložili do srozumitelného vysvětlení.

Struktura má být slovník se čtyřmi textovými poli. Chybějící klíč nebo jiný typ hodnoty ohlásíme s pole="koncept". V podmínce `any(k not in koncept for k in (...))` stačí jediný chybějící klíč, aby any vrátilo True. Připravený vytvor_koncept vytvoří ověřenou kopii hodnot; pomocné klíče můžeme ignorovat.

Over_adresu ověří jednu ASCII adresu a odstraní její krajní mezery. Neplatnou adresu přeložíme na ChybaPole s pole="prijemce". Předmět musí po strip obsahovat text a nesmí mít CR/LF; chyba má pole="predmet". Tělo musí po strip obsahovat text; chyba má pole="text". Strip tu slouží jen ke kontrole prázdnosti. Původní tělo včetně mezer předáme vytvor_zpravu, která sjednotí konce řádků a zajistí UTF-8. Předmět pro přenos očistí od krajních mezer, koncept si původní mezery ponechá.

## Přílohu načteme před změnou stavu

Prázdná cesta znamená žádnou přílohu. Jinak zavoláme pridej_prilohu nad novou zprávou: načte nejvýše 1 000 001 bajtů a povolí nejvýše 1 000 000. Chybu souboru nebo limitu přeložíme na ChybaPole s pole="priloha". Výsledná zpráva již obsahuje skutečné bytes, jméno souboru a MIME typ. Pozdější změna konceptu nebo souboru tuto hotovou zprávu nezmění.

Tlačítko Vybrat přílohu umožňuje volbu i před vyplněním formuláře. Nejprve ověří soubor na pomocné zprávě a teprve potom uloží absolutní cestu přes `str(Path(cesta).resolve())`. Resolve určí celou cestu nezávislou na pozdější pracovní složce. Zrušení vrátí prázdný text, takže nic nenahrazujeme. Chybějící nebo příliš velký soubor zachová předchozí výběr i náhled. Úspěšný výběr nahradí přílohu; Odebrat přílohu vymaže jen její cestu. Po obou změnách se má náhled znovu ověřit.

Ověřit a zobrazit čte všechna současná pole. Při chybě zachová jejich obsah, zaměří problematické pole přes focus_set a odstraní starý ověřený náhled. Při úspěchu ukáže dekódované hlavičky, tělo a informace o příloze. Náhled odpovídá poslednímu ověření. Sestavení ani výběr souboru neprovádí SMTP přenos.

## Váš úkol

Dokončete sestav_zpravu podle uvedeného pořadí. Použijte připravené funkce, odesílatel je eva@example.test. Vraťte EmailMessage, při chybě použijte ChybaPole s odpovídajícím polem; koncept neměňte. Připravený typ chyby i ovládání okna ponechte.

Nejdřív stiskněte Ověřit a zobrazit s prázdným formulářem. Postupně opravte příjemce na jan@example.test, předmět a tělo. Sledujte fokus a zprávy u každé chyby. Vyberte poznamka.txt z pracovních souborů lekce, ověřte znovu a potom zrušte další dialog: vybraná příloha se musí zachovat. Vyzkoušejte také chybnou adresu po předchozím úspěchu; starý náhled se nesmí vydávat za nově ověřený.
