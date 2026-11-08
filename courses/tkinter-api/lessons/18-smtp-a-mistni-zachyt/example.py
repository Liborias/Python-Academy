import math
import smtplib
from cvicna_posta import cvicna_posta
from zpravy import vytvor_zpravu, nahled_zpravy
from email.parser import BytesParser
from email.policy import default


def over_spojeni(host, port, timeout):
    if host != "127.0.0.1":
        raise ValueError("Cvičení používá pouze místní záchyt 127.0.0.1.")
    if isinstance(port, bool) or not isinstance(port, int) or not 1 <= port <= 65535:
        raise ValueError("Port musí být celé číslo 1 až 65535.")
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)):
        raise ValueError("Timeout musí být číslo.")
    if not 0 < timeout <= 5 or not math.isfinite(timeout):
        raise ValueError("Timeout musí být konečný, větší než 0 a nejvýše 5 sekund.")
    return host, port, float(timeout)


# Tento klient se smí připojit pouze k místnímu cvičnému serveru.
def odesli_do_zachytu(zprava, host, port, timeout=2):
    host, port, timeout = over_spojeni(host, port, timeout)
    with smtplib.SMTP(host, port, timeout=timeout, local_hostname="localhost") as klient:
        odmitnuti = klient.send_message(zprava)
        if odmitnuti:
            raise smtplib.SMTPRecipientsRefused(odmitnuti)
    return None


if __name__ == "__main__":
    zprava = vytvor_zpravu("eva@example.test", "jan@example.test", "Zkouška SMTP", "Dobrý den.\n.Řádek začínající tečkou.")
    # Záchyt zprávu uloží jen v paměti a nikam dál ji nedoručuje.
    with cvicna_posta() as posta:
        odesli_do_zachytu(zprava, posta.host, posta.port)
        prijata = posta.zpravy[0]
        rozebrana = BytesParser(policy=default).parsebytes(prijata.data)
        print("Zachyceno:", len(posta.zpravy))
        print("Obálka:", prijata.odesilatel, "->", ", ".join(prijata.prijemci))
        print(nahled_zpravy(rozebrana))
