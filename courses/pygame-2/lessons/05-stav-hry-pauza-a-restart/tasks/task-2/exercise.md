### Jednorázový signál vypršení

`Casovac(limit)` dostane kladný počet sekund; uloží limit i zbyva=limit. `update(dt)` odečte nezáporné dt, zbyva nesmí pod nulu. Vrátí bool True **jen v kroku přechodu z kladného času na nulu**, další kroky False. `restart()` obnoví zbyva na původní limit. Neopakujte událost v každém snímku po vypršení. Desetinný čas je float; nepožadujeme obecně přesnou rovnost součtu deseti desetin s jedničkou.
