def vytvor_kontakt(jmeno, telefon):
    return {"jmeno": jmeno, "telefon": telefon}


def zmen_telefon(kontakt, novy):
    kontakt["telefon"] = novy
    return kontakt


def pridej_email(kontakt, email):
    kontakt["email"] = email
    return kontakt
