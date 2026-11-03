## Cíl
Poznat, co po serverovém pokusu ještě chybí pro dlouhodobý provoz. Toto je koncept navazujícího nasazovacího bloku, nikoli hotový návod k produkčnímu provozu libovolné aplikace.

## Praktický krok
Sepište pro svůj projekt krátký provozní plán. Rozlišujte skript, statický web a webovou aplikaci s backendem; nespouštějí se stejným způsobem.

1. Zapište požadovanou verzi Pythonu, závislosti a přesný startovací příkaz i pracovní složku.
2. Rozhodněte, kdo má projekt používat. Pro osobní pokus stačí SSH tunel. Veřejný statický web lze svěřit statickému hostingu; Python backend vyžaduje server vhodný pro zvolený framework.
3. Pro trvalý Linuxový provoz navrhněte samostatného uživatele a službu spravovanou například systemd: start, stop, restart po pádu, logy. Konkrétní konfiguraci je třeba doplnit pro konkrétní aplikaci, ne ji hádat pro všechny projekty.
4. Při veřejném přístupu naplánujte doménu, HTTPS, správu přístupů a síťová pravidla. Výukový `http.server` ani `start.py` Dílny nezpřístupňujte jako veřejnou službu.
5. Oddělte tajné konfigurace a data od zdrojového repozitáře. Určete zálohu, obnovení a způsob ověření, že služba po restartu opravdu odpovídá.
6. Aktualizaci nejprve vyzkoušejte na kopii. Poznamenejte si nasazený commit, test po aktualizaci a cestu zpět, která zachová data.

Výstupem celého úvodního podkurzu má být vlastní projekt, reprodukovatelné prostředí, srozumitelný README, základní Git historie a schopnost projekt znovu spustit. Serverový modul může zůstat odložený.

## Co příkazy dělají a co se děje
Provozní plán má obsahovat ověřitelný startovací příkaz, například úplnou cestu k interpreteru a skriptu, ne jen poznámku „spustit Python“. systemd je správce služeb Linuxu: místo otevřeného ručního terminálu může startovat, hlídat a zastavovat konkrétní proces. Samotný koncept zde žádnou službu nevytváří.

HTTPS chrání síťový přenos, ověřovací token povoluje konkrétní požadavky a virtuální prostředí vybírá závislosti. Každá součást má jinou úlohu. Konečné ověření nasazení musí provést skutečný požadavek a zkontrolovat odpověď po restartu; samotný existující proces nebo otevřený port není důkaz správné funkce.

## Vlastní ověření
- [ ] Umím z nového terminálu spustit projekt podle README.
- [ ] Vím, co je hotový místní pokus a co teprve návrh nasazení.
- [ ] Mám seznam chybějících provozních kroků pro svůj konkrétní projekt.
