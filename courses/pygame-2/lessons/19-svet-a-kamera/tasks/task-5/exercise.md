### Kreslení s ořezem výhledu

Napište `vykresli_svet(plocha, objekty, kamera)`. Nakreslí viditelné objekty v jejich pořadí, při převodu rohu použije na_obrazovku a výsledné x/y zaokrouhlí přes round. Viditelne i na_obrazovku jsou připravené v kamera.py. Objekty mají image a kladný rect; světové polohy ani zdrojové pixely neměňte.

Před kreslením uložte `get_clip()`, omezte kreslení na **průnik původního clip a kamera.vyhled** a původní clip obnovte v finally, i když kreslení vyvolá chybu. Tuto chybu neukrývejte. Návratovou hodnotu nepoužíváme. Výhled tak nepoškodí HUD ani jiný výřez nastavený volajícím.
