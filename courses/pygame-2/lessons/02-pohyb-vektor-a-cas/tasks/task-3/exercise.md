### Desetinný pohyb uvnitř hranic

`OmezenaLod(stred, rychlost, hranice)` má stejný pohyb a kopie vektorů jako Úkol 1, navíc vlastní kopii Rect hranice. Loď 32 × 24 začíná uvnitř hranic (šířka alespoň 32, výška alespoň 24). Po každém kroku omezte **desetinný střed** na x od left+16 do right−16 a y od top+12 do bottom−12. `max(minimum, min(maximum, hodnota))` ořízne hodnotu do intervalu. Pak aktualizujte rect přes round. Zpětné kopírování zaokrouhleného rect do pozice v každém kroku by ztratilo malé pohyby. Rychlost neměňte.
