from pathlib import Path
import json
import queue
from email.parser import BytesParser
from email.policy import default
from dilna import nacti_koncept
from priprava import sestav_zpravu
from prenos import predat_zpravu
from cvicna_posta import cvicna_posta


def prover_predani(cesta):
    koncept = nacti_koncept(cesta)
    zprava = sestav_zpravu(koncept)
    # Konzolová zkouška je synchronní; žádné Tk okno při ní neběží.
    with cvicna_posta() as posta:
        fronta = queue.Queue()
        predat_zpravu(zprava, posta.host, posta.port, 2, fronta)
        stav = fronta.get_nowait()
        if stav != "prijato":
            raise RuntimeError("Předání nebylo potvrzené: " + stav)
        zachycene = posta.zpravy
        if len(zachycene) != 1:
            raise RuntimeError("Záchyt musí obsahovat právě jednu zprávu.")
        zaznam = zachycene[0]
        prijata = BytesParser(policy=default).parsebytes(zaznam.data)
        telo = prijata.get_body(preferencelist=("plain",)).get_content().replace("\r\n", "\n").replace("\r", "\n")
        prilohy = [{"nazev": p.get_filename(), "velikost": len(p.get_payload(decode=True))}
                   for p in prijata.iter_attachments()]
        return {"stav": stav, "zachyceno": len(zachycene), "prijemce": zaznam.prijemci[0],
                "predmet": str(prijata["Subject"]), "text": telo, "prilohy": prilohy}


if __name__ == "__main__":
    # Jedna skutečná místní zpráva, výsledek přečteme ze záchytu, nikam dál nejde.
    cesta = Path(__file__).with_name("koncept-predani.json")
    print("Závěrečné místní ověření:")
    print(json.dumps(prover_predani(cesta), ensure_ascii=False, indent=2))
