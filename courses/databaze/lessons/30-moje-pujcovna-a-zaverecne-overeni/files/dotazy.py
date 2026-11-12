def pomucky_s_kategorii(con):
    return con.execute('''
        SELECT p.id, p.nazev, p.kusy, k.nazev
        FROM pomucky AS p JOIN kategorie AS k ON p.kategorie_id = k.id
        ORDER BY p.id
    ''').fetchall()

def vsechny_pomucky(con):
    return con.execute('''
        SELECT p.id, p.nazev, p.kusy, k.nazev
        FROM pomucky AS p LEFT JOIN kategorie AS k ON p.kategorie_id = k.id
        ORDER BY p.id
    ''').fetchall()

def prehled_kategorii(con):
    return con.execute('''
        SELECT k.id, k.nazev, COUNT(p.id), COALESCE(SUM(p.kusy), 0)
        FROM kategorie AS k LEFT JOIN pomucky AS p ON p.kategorie_id = k.id
        GROUP BY k.id, k.nazev ORDER BY k.id
    ''').fetchall()

def bez_aktivni_vypujcky(con):
    return con.execute('''
        SELECT p.id, p.nazev, p.kusy FROM pomucky AS p
        WHERE NOT EXISTS (
            SELECT 1 FROM vypujcky AS v WHERE v.pomucka_id = p.id AND v.vraceno = 0
        ) ORDER BY p.id
    ''').fetchall()

def vypujcky_clena(con, clen):
    return con.execute('''
        SELECT v.id, p.nazev FROM vypujcky AS v
        JOIN pomucky AS p ON v.pomucka_id = p.id
        WHERE v.clen = ? AND v.vraceno = 0 ORDER BY v.id
    ''', (clen,)).fetchall()
