"""Pošle místnímu serveru požadavek s tokenem a ukáže odpověď."""
import getpass
import json
import urllib.error
import urllib.request

# getpass při psaní nezobrazuje token na obrazovce ani ho neukládá do souboru.
token = getpass.getpass("Vložte token z terminálu serveru: ")
request = urllib.request.Request(
    "http://127.0.0.1:8767/run", data=b"", method="POST",
    headers={"X-Project-Token": token},
)
try:
    with urllib.request.urlopen(request, timeout=10) as response:
        result = json.load(response)
    print("Návratový kód programu:", result["exit"])
    print(result["stdout"], end="")
except urllib.error.HTTPError as error:
    print("Server požadavek odmítl, HTTP", error.code)
    print(error.read().decode("utf-8"))
except urllib.error.URLError:
    print("Server není dostupný. Ověřte, že běží v prvním terminálu na portu 8767.")
