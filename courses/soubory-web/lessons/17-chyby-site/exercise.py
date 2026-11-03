import time
import requests

# Úkol:
#   stahni_bezpecne(url, timeout=2)
#       -> text stránky; při jakékoli chybě (špatný stavový kód, timeout, nepřipojení) vrátí None
#   stahni_s_opakovanim(url, pokusy=3, pauza=0.1)
#       -> text stránky; když se pokus nepovede, počká `pauza` sekund a zkusí to znovu,
#          nejvýš `pokusy` krát celkem. Když se nepovede ani jeden pokus, vrátí None.
