### Sečíst a odstranit chycené bonusy

`seber_bonusy(hrac, bonusy)` vrátí součet celočíselných atributů hodnota pouze u zasažených bonusů (obdélníková kolize). Hodnota může být nulová i záporná. Zasažené odstraní ze **všech** skupin pomocí kill; ostatní a hráče zachová. Prázdný zásah vrátí 0. Přepínač True ve spritecollide spouští kill, samotné nalezení zásahů ho jinak neprovádí.
