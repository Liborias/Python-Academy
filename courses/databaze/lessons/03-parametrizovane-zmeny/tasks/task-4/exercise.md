## Smazání podle identifikátoru

Vytvořte **smaz_pomucku(con, id_pomucky)**. Parametrizovaný DELETE odstraní jen odpovídající id a vrátí rowcount. Podruhé už stejné id nenajde, vrátí tedy 0.

Text '22 OR 1=1' je při správném předání parametru prostě hodnota, ne další část příkazu; nesmí smazat všechny řádky. Nevracejte lastrowid, ten popisuje vložení. Transakci a spojení vlastní volající.
