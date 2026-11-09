### Přiletět k cíli bez přeletu

`CilovaLod(stred, rychlost, cil)` kopíruje střed/cíl do Vector2 a uloží nezápornou číselnou rychlost. V `update(dt)` letí přímo k cíli nejvýše o rychlost × dt; při dosažení se zastaví **přesně v cíli**, nesmí přeletět ani kmitat. Pokud už v cíli je, nic neposouvejte a nedělte nulou. Rect se opět řídí round. Můžete použít rozdíl vektorů a jeho délku nebo odpovídající metodu Vector2; vstupy zachovejte.
