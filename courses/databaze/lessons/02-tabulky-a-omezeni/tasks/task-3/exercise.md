## Výpůjčka s výchozím stavem

Vytvořte **vytvor_vypujcky(con)**. Tabulka vypujcky má id INTEGER PRIMARY KEY, pomucka TEXT NOT NULL, clen TEXT NOT NULL a vraceno INTEGER NOT NULL DEFAULT 0 CHECK (vraceno IN (0, 1)).

Nula znamená probíhající výpůjčku, jednička vrácenou. Tento zjednodušený záznam zatím drží názvy jako text, není ještě propojen cizím klíčem. Při vložení bez vraceno se doplní nula; jiná hodnota ani NULL neplatí. Použijte IF NOT EXISTS, nevracejte data a neukončujte předané spojení či transakci.
