## Příkaz pro vlastní testy

Vytvořte **prikaz_testu(python, koren)**. Interpreter je neprázdný text a koren/testy musí být existující adresář, jinak ValueError. Vraťte [python, '-m', 'unittest', 'discover', '-s', absolutni_cesta_testy, '-p', 'test_*.py'].

Discover najde a provede testy, -s určí počáteční adresář a -p vzor názvů. Seznam pouze vracejte. Pomocný over_projekt.py navíc spustí testy se správným cwd: unittest pak najde model_hry.py i při zavolání pomocníka z jiného adresáře. Úspěšná kontrola jednoho příkazu není důkazem funkčnosti GUI na jiném systému.
