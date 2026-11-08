from email.message import EmailMessage
from email.headerregistry import Address
from email.errors import HeaderParseError
from email.policy import SMTP
from email.utils import formatdate, make_msgid


def over_adresu(text):
    if not isinstance(text, str) or not text.isascii() or "\r" in text or "\n" in text:
        raise ValueError("Použijte jednu adresu ASCII bez nového řádku.")
    text = text.strip()
    try:
        adresa = Address(addr_spec=text)
    except (ValueError, HeaderParseError):
        raise ValueError("Neplatný tvar adresy.") from None
    if not adresa.username or not adresa.domain:
        raise ValueError("Adresa potřebuje uživatele i doménu.")
    return str(adresa)


# EmailMessage se postará o MIME a kódování českého předmětu i těla.
def vytvor_zpravu(odesilatel, prijemce, predmet, text):
    odesilatel = over_adresu(odesilatel)
    prijemce = over_adresu(prijemce)
    if not isinstance(predmet, str) or not predmet.strip() or "\r" in predmet or "\n" in predmet:
        raise ValueError("Předmět musí být neprázdný a jednořádkový.")
    if not isinstance(text, str):
        raise ValueError("Tělo musí být text.")
    zprava = EmailMessage(policy=SMTP)
    # Doplňte From, To a normalizovaný Subject.
    zprava["Date"] = formatdate(localtime=True)
    zprava["Message-ID"] = make_msgid(domain="example.test")
    # Nastavte tělo v UTF-8, CRLF/CR převeďte na LF.
    return zprava


def nahled_zpravy(zprava):
    telo = zprava.get_body(preferencelist=("plain",))
    text = telo.get_content().replace("\r\n", "\n").replace("\r", "\n")
    return f"Od: {zprava['From']}\nKomu: {zprava['To']}\nPředmět: {zprava['Subject']}\n\n{text}"


if __name__ == "__main__":
    # Pouhý náhled nic neodesílá a nepotřebuje SMTP server.
    zprava = vytvor_zpravu("eva@example.test", "jan@example.test", "  Česká zpráva  ", "Dobrý den,\nzkouším svoji první zprávu.")
    print(nahled_zpravy(zprava))
    print("Serializace pro SMTP:")
    print(zprava.as_string())
