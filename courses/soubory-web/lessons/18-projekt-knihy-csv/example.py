import csv
from bs4 import BeautifulSoup

html = """<ul>
<li class="zvire"><span class="jmeno">Pes</span><span class="vaha">12 kg</span></li>
<li class="zvire velke"><span class="jmeno">Kůň</span><span class="vaha">450 kg</span></li>
</ul>"""

soup = BeautifulSoup(html, "html.parser")
radky = []
for li in soup.select(".zvire"):
    radky.append({
        "jmeno": li.select_one(".jmeno").get_text(strip=True),
        "vaha": int(li.select_one(".vaha").get_text(strip=True).split()[0]),   # "12 kg" -> 12
        "velke": "velke" in li.get("class", []),                               # třída je seznam
    })
print(radky[1])    # {'jmeno': 'Kůň', 'vaha': 450, 'velke': True}

with open("zvirata.csv", "w", encoding="utf-8", newline="") as soubor:         # newline="" pro csv
    zapisovac = csv.DictWriter(soubor, fieldnames=["jmeno", "vaha", "velke"])
    zapisovac.writeheader()
    zapisovac.writerows(radky)

with open("zvirata.csv", encoding="utf-8") as soubor:
    print(soubor.read().strip())
