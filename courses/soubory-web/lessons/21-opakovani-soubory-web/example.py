import csv
import json

radky = [{"jmeno": "Eva", "body": "42"}, {"jmeno": "Jan", "body": "35"}]

with open("zaci.csv", "w", encoding="utf-8", newline="") as soubor:      # CSV se píše s newline=""
    zapisovac = csv.DictWriter(soubor, fieldnames=["jmeno", "body"])
    zapisovac.writeheader()
    zapisovac.writerows(radky)

with open("zaci.csv", encoding="utf-8", newline="") as soubor:
    nactene = list(csv.DictReader(soubor))
print(sum(int(r["body"]) for r in nactene))                           # 77: hodnoty z CSV jsou text, převádíme

with open("zaci.json", "w", encoding="utf-8") as soubor:
    json.dump(nactene, soubor, ensure_ascii=False, indent=2)           # čeština zůstane čitelná
print(json.load(open("zaci.json", encoding="utf-8"))[0]["jmeno"])
