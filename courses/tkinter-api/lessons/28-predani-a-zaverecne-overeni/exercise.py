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
    # TODO: proveďte jedno předání a vraťte údaje skutečně zachycené zprávy.
    return {"stav": "neovereno", "zachyceno": 0}


if __name__ == "__main__":
    # Jedna skutečná místní zpráva, výsledek přečteme ze záchytu, nikam dál nejde.
    cesta = Path(__file__).with_name("koncept-predani.json")
    print("Závěrečné místní ověření:")
    print(json.dumps(prover_predani(cesta), ensure_ascii=False, indent=2))
