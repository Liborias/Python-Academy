### Cache změněných rozměrů

Vytvořte `BankaVelikosti(original, zmen)` a `obraz(rozmer)`. Při konstrukci zkopírujte původní Surface. `rozmer` je dvojice kladných celých čísel; seznam a tuple stejné velikosti mají tvořit stejný klíč. Při prvním požadavku zavolejte `zmen(vlastni_original, tuple(rozmer))`, uložte vlastní kopii výsledku a pokaždé vraťte další kopii. `zmen` má stejné rozhraní jako `pygame.transform.smoothscale` a nemění svůj vstup. Cache patří každé instanci.

Změna velikosti vždy vychází z originálu, nikoli z minulé zvětšené či zmenšené kopie. Upravování již vráceného obrázku nesmí poškodit další výsledky.
