## Relační schéma klubovního skladu

Vytvořte **vytvor_relacni_schema(con)** podle popisu ve výkladu: kategorie, pomucky s volitelným kategorie_id a vypujcky s povinným pomucka_id. Použijte IF NOT EXISTS a nic nemažte ani nemigrujte. Funkce vrátí None; spojení už má zapnuté foreign_keys.

Kategorie: id INTEGER PRIMARY KEY, nazev TEXT NOT NULL UNIQUE. Pomucky: id INTEGER PRIMARY KEY, nazev TEXT NOT NULL UNIQUE, kusy INTEGER NOT NULL CHECK(typeof(kusy)='integer' AND kusy>=0), kategorie_id INTEGER REFERENCES kategorie(id) ON DELETE SET NULL.

Vypujcky: id INTEGER PRIMARY KEY, pomucka_id INTEGER NOT NULL REFERENCES pomucky(id) ON DELETE RESTRICT, clen TEXT NOT NULL, vraceno INTEGER NOT NULL DEFAULT 0 CHECK(vraceno IN(0,1)). SET NULL zachová pomůcku po zrušení kategorie. RESTRICT chrání i již vrácenou historii. Sami neukončujte spojení ani transakci.
