### Animace podle stavu

Vytvořte `StavoveAnimace(animace, pocatecni)`. Zkopíruje mapu jméno → objekt animace do vlastního slovníku `animace`, ponechá stejné hodnoty a uloží `stav`. Neznámé počáteční jméno odmítne KeyError. `update(dt)` a `obraz()` delegují jen na aktuální objekt.

`prepni(jmeno)` nejdříve ověří, že jméno existuje. Při stejném stavu vrací False a nic nerestartuje. Při jiném nastaví stav, zavolá restart vybrané animace a vrátí True. Neznámé jméno vyvolá KeyError bez změny dosavadního stavu. Neaktivní animace se neposouvají. Animace z animator.py už rozhraní update/obraz/restart poskytuje.
