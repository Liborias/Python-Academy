from bs4 import BeautifulSoup

html = """<div class="zviratko" id="z1"><h3>Pes</h3><span class="vaha">12 kg</span></div>
<div class="zviratko velke" id="z2"><h3>Kůň</h3><span class="vaha">450 kg</span></div>"""
soup = BeautifulSoup(html, "html.parser")

print([h.get_text() for h in soup.select(".zviratko h3")])         # ['Pes', 'Kůň']: h3 uvnitř třídy zviratko
print(soup.select_one("#z2 .vaha").get_text())                     # 450 kg: id přes #, třída přes tečku
print(soup.select_one("#neni"))                                    # None: select_one nic nenašel

for div in soup.select("div.zviratko"):
    print("velke" in div.get("class", []))                         # class je seznam: False, True
