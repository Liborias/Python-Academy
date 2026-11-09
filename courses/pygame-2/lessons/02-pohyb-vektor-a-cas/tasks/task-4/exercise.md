### Nejprve rychlost, potom poloha

`ZrychlujiciLod(stred, rychlost, zrychleni)` kopíruje všechny tři dvojice do vlastních Vector2. `update(dt)` provede v tomto pořadí: rychlost += zrychleni × dt; pozice += **nová** rychlost × dt; rect podle round. Jde o předem zvolenou krokovou aproximaci, ne přesný vzorec dráhy při zrychlení. Rozdělení času na jiný počet kroků zde může změnit výsledek. Zrychlení je v pixelech za sekundu na druhou, dt nezáporné. Vstupy zachovejte.
