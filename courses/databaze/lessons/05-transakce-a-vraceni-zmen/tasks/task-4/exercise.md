## Pomůcka a zpráva v jednom kroku

Vytvořte **pridej_se_zpravou(con, nazev, kusy, popis)**. Při autocommit=False vloží pomůcku a zprávu do udalosti jako jednu transakci. Vrátí id nové pomůcky z kurzoru prvního INSERT. Všechny hodnoty jsou parametry.

Pokud selže druhý zápis, například popis=None poruší NOT NULL, nová pomůcka nesmí zůstat. Chyba IntegrityError se předá, úspěšná dvojice se potvrdí. Jiný autocommit odmítněte ValueError. Spojení nezavírejte, před voláním musí být ostatní práce potvrzená nebo vrácená.
