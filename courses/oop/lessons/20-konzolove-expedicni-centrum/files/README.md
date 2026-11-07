# Chytré expediční centrum

V pracovní složce spusťte `python reseni.py`. Ukončení: `konec` nebo konec vstupu.
Změny jsou jen v paměti a po dalším spuštění začínáme znovu s pěti knihami a dvěma obaly.
Kniha stojí 250 Kč, obal 30 Kč; doprava je nabídka, nikoli provedená platba nebo odeslání.
Pro vlastní rozšíření změňte katalog ve vytvor_demo a odpovídající obsluhu nova.

Příklad:

```
stav
nova A 2 1 1200
doprava A kolo
poznamka A Nezvonit prosím
prehled A
nova B 4 0 800
storno A
storno A
nova B 4 0 800
stav
konec
```

B je nejprve odmítnuta bez částečné rezervace. Po stornu A ji lze přijmout.
Druhé storno A nic neuvolní. Číslo jednou úspěšně přijaté objednávky se znovu nepoužívá.
Adresa je v ukázce předvyplněná: Javorová 1, 60200 Brno. Způsoby dopravy: odber, kuryr, kolo.

Příkazy mají malá písmena; nova přijímá číslo objednávky, počty knih/obalů a hmotnost v gramech.
Nula vynechá dané zboží, alespoň jeden kus je nutný. Mezery mezi slovy poznámky se sjednotí.
Chybný příkaz se odmítne a ovladač pokračuje. Samotný proved_prikaz chybu předává přes ValueError.

Testy modelu: `python -m unittest -v test_centrum`. Čtyři příklady testů jsou čitelné v test_centrum.py.
Přidejte vlastní test na hranici 2000/2001 g cyklodopravy a na dvě nezávislá centra.

Rozdělení práce:

- NakupniObjednavka skládá starší Objednavka/Polozka, sčítá skladové kódy a uzavírá úpravy.
- RezervacniSklad rozšiřuje Sklad, používá SkladovaKarta a eviduje kusy podle objednávky.
- ExpedicniCentrum propojuje objednávku, Expedice a ExpedicniStitek s adresou a poznámkami.
- Cyklodoprava má společné veřejné cena(balik), žádné větvení podle tříd v centru nepotřebuje.
- reseni.py pouze čte příkazy, převádí vstupy, volá model a formátuje odpovědi.

Vlastními slovy vysvětlete: proč se doprava ověřuje před skladem, proč objednávku uzavíráme,
proč storno vrací jen její kusy a jak přidat další dopravu bez změny centra.
Projekt používá standardní knihovnu a vymyšlené údaje; nic nemusíte registrovat na internetu.
