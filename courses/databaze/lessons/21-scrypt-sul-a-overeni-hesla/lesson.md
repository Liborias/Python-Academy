## Heslo nepotřebujeme zpětně přečíst

Ověříme, zda člověk zadal správnou frázi, aniž bychom uložili její čitelný text. `scrypt` z hesla, soli a parametrů odvodí bajty. Při ověření spočítáme stejné odvození a porovnáme je. Nejde o šifrování s pozdějším dešifrováním.

```python
# Běžný text se nejprve převede na bajty UTF-8.
text = 'Žofie'
print('Znaků:', len(text), 'bajtů:', len(text.encode('utf-8')))
```

Výsledek 5 znaků a 6 bajtů připomíná, proč počítáme také s češtinou. Heslo neořezáváme ani nepřevádíme na malá písmena; mezery i rozdílné Unicode zápisy jsou jeho součást.

## Sůl, náklady a záznam

Sůl je 16 náhodných bajtů ze secrets.token_bytes, pro každé nové vytvoření jiná. Není tajná: uložíme ji s otiskem. Stejné heslo tak obvykle dostane jiný otisk. Přepínatelná ukázka porovná dvě vytvoření.

Používáme pevný profil: n=131072, r=8, p=1, dklen=32. Scrypt spotřebuje přibližně 128 MiB pracovní paměti; maxmem=256 MiB je povolená horní mez. Záměrná náročnost ztěžuje rychlé hádání. Není to počet znaků hesla ani velikost uloženého souboru. Konkrétní provoz by parametry volil podle svých nároků a měření.

`pravidla.py` má verzi 1, profil a validaci. Záznam má přesně verze, algoritmus, n, r, p, dklen, sul a otisk. Sul je 32 hex znaků (16 bajtů), otisk 64 hex znaků (32 bajtů). Pevná kontrola odmítne poškozené či neznámé parametry **před** výpočtem, aby soubor nemohl nařídit neomezené nároky.

## Porovnávání a prostředí

Hmac.compare_digest porovnává odvozené bajty vhodným standardním postupem. Prosté SHA-256 je pro tento účel příliš rychlé, Base64 zase jen převádí zápis. Heslo ani celý záznam nevypisujeme do konzole. Příklady používají záměrně fiktivní frázi.

Python 3.12+, ověřeno 3.14.8; bez pip a bez sítě. Podpora scrypt závisí na sestavení Pythonu. Výpočet může na slabším stroji chvíli trvat. Ve VS Code/VSCodium/PyCharm zvolte stejnou .venv jako v terminálu. Podrobnosti v Přípravě a NAVOD.md.

## Váš úkol

Doplňte **vytvor_zaznam(heslo)** a **over_heslo(heslo, zaznam)**. Validace over_heslo_text přijímá 12–256 znaků, nejvýše 1024 bajtů UTF-8, bez ořezání. Neplatný vstup při vytváření vyvolá ValueError.

Vytvor_zaznam vezme novou sůl ze secrets, zavolá hashlib.scrypt s pevným profilem a MAXMEM, vrátí slovník profilu se sul/otisk jako hex. Over_heslo vrací bool: neplatné heslo či záznam False, jinak znovu odvodí otisk ze stejné soli a použije hmac.compare_digest. Neznámou verzi/parametry nepočítá. Funkce importem nic neprovádějí. Více správných zápisů je v pořádku, zachovejte pravidla algoritmu a formátu.
