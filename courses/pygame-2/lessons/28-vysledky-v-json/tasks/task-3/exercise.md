## Pořadí výsledků a stabilní shody

Vytvořte **serad_vysledky(data, limit=5)**. Nejdřív vyberte čisté záznamy přes připravenou vyber_vysledky. Úspěšné mise jsou první, pak vyšší body, pak jméno přes casefold vzestupně. Při úplné shodě zachovejte původní pořadí: sorted je stabilní.

Limit musí být nezáporný int, nikoli bool; jinak ValueError. Limit 0 vrátí []. Body sestupně lze v klíči vyjádřit záporným číslem. Jde o jednoduché programové pořadí Unicode, ne české slovníkové řazení. Vstupní seznam ani záznamy neměňte.
