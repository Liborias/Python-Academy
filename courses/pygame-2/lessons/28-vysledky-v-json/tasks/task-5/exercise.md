## Zápis bez zničení staršího souboru

Vytvořte **uloz_vysledky(cesta, data)**. Přes vyber_vysledky vytvořte čistý seznam a uložte {'verze': 1, 'vysledky': zaznamy} v UTF-8. Vraťte počet uložených záznamů a vstup neměňte. Rodičovské adresáře vytvořte podle potřeby.

Nejdřív vytvořte jedinečný dočasný soubor ve stejném adresáři, zapište celý JSON, uzavřete ho a až pak proveďte os.replace na cíl. Na Windows se uzavření musí stát před nahrazením. Dočasný soubor uklidíte ve finally, i když nahrazení selže. Starý cíl v takovém případě zůstane beze změny a OSError předáte dál.

NamedTemporaryFile s delete=False umožní po uzavření použít jeho cestu. Ensure_ascii=False uchová čitelnou češtinu, indent=2 usnadní korektury. Jde o ochranu při selhání zápisu/nahrazení, nikoli záruku proti všem výpadkům napájení či souběžným zápisům více procesů.
