def zapis_pomucku(con, nazev, kusy, kategorie_id=None):
    return con.execute('INSERT INTO pomucky (nazev, kusy, kategorie_id) VALUES (?, ?, ?)',
                       (nazev, kusy, kategorie_id)).lastrowid

def presun_do_kategorie(con, pomucka_id, kategorie_id):
    return con.execute('UPDATE pomucky SET kategorie_id = ? WHERE id = ?',
                       (kategorie_id, pomucka_id)).rowcount

def smaz_kategorii(con, kategorie_id):
    return con.execute('DELETE FROM kategorie WHERE id = ?', (kategorie_id,)).rowcount
