from bs4 import BeautifulSoup

html = "<ul><li>pes</li><li class='x'>kocka</li><li>kun</li></ul>"
soup = BeautifulSoup(html, "html.parser")

print([li.get_text() for li in soup.find_all("li")])               # ['pes', 'kocka', 'kun']
print(len(soup.find_all("li", class_="x")))                        # 1: jen položky s touto třídou
print(soup.find_all("table"))                                      # []: nic nenalezeno, seznam je prázdný

ul = soup.find("ul")                                               # najdeme jednu značku
print(len(ul.find_all("li")))                                      # a hledáme jen uvnitř ní: 3
