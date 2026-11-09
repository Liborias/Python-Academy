### Kill odstraní členství všude

`vyrad_mimo(skupina, hranice)` vyřadí přes kill všechny členy, jejichž rect **nemá kladný plošný průnik** s hranice. Pouhé přiložení hran bez plochy je také mimo. Vraťte počet vyřazených. `kill()` odstraní sprite ze všech jeho skupin, nikoli jen této; Python objekt může dál existovat v proměnné. Zbylé objekty a hranice neměňte. `skupina.sprites()` je seznam členů, přes který lze bezpečně procházet při odstraňování.
