## Popisek a pozice nejsou totéž

Index může obsahovat názvy nebo čísla. Proto rozlišujeme `serie.loc[...]` pro popisky a `serie.iloc[...]` pro pořadové pozice počítané od nuly. U indexu [20, 0, 10] je loc[0] hodnota s popiskem 0, ale iloc[0] první hodnota, tedy s popiskem 20. Když zkoušíme číselné indexy, tento rozdíl je dobře vidět.

Při jedinečném indexu vrátí loc[jeden_popisek] jednu hodnotu. `loc[seznam_popisku]` vrátí Series a respektuje pořadí požadavku. Seznam může být prázdný nebo některý existující popisek zopakovat. V těchto úkolech požadované popisky vždy existují; neexistující by pandas ohlásilo přes KeyError.

## Seznam pozic a řez

`iloc[[2, 0]]` vybere třetí a první prvek v tomto pořadí. -1 znamená poslední pozici. Naopak `iloc[1:3]` vrátí souvislý úsek s pozicemi 1 a 2, konec řezu se nezahrnuje. Platí pravidla běžného Python řezu včetně záporných hranic, oříznutí příliš vzdálené hranice a prázdného výsledku.

Pozor na rozdíl při řezu podle popisků: loc u seřazeného indexu zahrnuje i koncovou hranici popisku. V dnešních úkolech loc používá seznam konkrétních názvů; pro pozicový úsek použijte iloc. Nemíchejte oba významy do neurčitého `serie[...]`.

Copy vytvoří samostatnou kopii vybraného výsledku. Pandas 3 používá Copy-on-Write, takže změny výsledku se nemají provádět řetězeným přiřazením do původních dat. Zatím jen vybíráme a vracíme výsledek; změny přes loc budeme probírat zvlášť. Vstupní Series v žádném z těchto úkolů neměňte.

## Změna popisku a řazení

`serie.rename(index={"A": "Brno"})` vrátí Series s přejmenovaným vybraným indexem. Ostatní popisky zůstanou a hodnoty se nepřesouvají. To je jiná operace než rename("nazev"), kterou jsme měnili název celé Series v lekci 1.

Sort_index vrací vzestupně seřazené popisky i s jejich původními hodnotami. Pro cvičení používáme jednoduché textové kódy nebo čísla. Technické řazení textu není plnohodnotné české abecední řazení; u znaků s diakritikou s ním nelze bez dalšího zacházet jako s českým slovníkem.

## Váš úkol

Dokončete `vyber_podle_popisku(serie, popisky)`. Vraťte Series s požadovanými existujícími popisky v přesně požadovaném pořadí, včetně opakování. Zachovejte name a dtype. Seznam popisků může být prázdný a vstupní index je jedinečný.

Potom vyzkoušejte úkoly s úsekem, jednotlivými pozicemi, novými názvy a řazením. Při každém výběru si nahlas určete, zda právě používáte popisek, nebo pozici.
