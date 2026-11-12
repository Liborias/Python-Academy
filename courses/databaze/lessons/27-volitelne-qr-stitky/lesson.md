## QR je obrázek nesoucí text

QR štítek může obsahovat inventární kód. Telefon či čtečka z něj získá text, samo vytvoření nikam nic neodesílá. V naší půjčovně používáme tvar PY-AKADEMIE:PUJ:18; není to odkaz, který by aplikace automaticky otevírala.

```python
# Text budeme do QR předávat jako přesné bajty UTF-8.
text = 'Štítek; ukázka'
print(text.encode('utf-8').decode('utf-8') == text)
```

Tato lekce je volitelná. Bez QR knihovny příklad pouze vypíše postup, ostatní databázové části fungují dál. Do stejné .venv pro VS Code, VSCodium či PyCharm a terminál nainstalujte:

```powershell
python -m pip install "qrcode[pil]>=8.2,<9"
python -c "import qrcode, PIL; print('QR připraveno')"
```

První příkaz potřebuje internet jen pro instalaci. Samotné vytváření funguje lokálně a offline. Pillow zapisuje PNG, qrcode sestaví symbol. Nejde o povinnou závislost celého kurzu.

## Čitelnost a zápis

Použijeme černé moduly na bílém podkladu, box_size=6 a border=4. Bílý okraj pomáhá čtečce odlišit symbol od okolí, proto jej neodřezáváme. Oprava chyb M a fit=True dovolí knihovně zvolit velikost podle obsahu. Text se nesmí oříznout či změnit.

Píšeme přes bezpecny_cil z dřívější lekce. Zvolený PNG se nahradí až po dokončení, chyba zachová starý soubor. Dočasný název nemá příponu png, proto save dostane výslovně format='PNG'. Parametr zdroj může chránit právě otevřenou DB.

## Váš úkol

Doplňte **qr_png(text, cesta, zdroj=None)** s pojmenovaným zdroj. Over_qr_text vrací platné neprázdné UTF-8 do 512 bajtů, cil_png absolutní Path s příponou .png. Ziskej_qrcode vrátí knihovnu nebo None. Pokud chybí, vraťte None a nic nevytvářejte.

Jinak v bezpecny_cil(cil, zdroj) vytvořte QRCode s ERROR_CORRECT_M, box_size=6, border=4; přidejte bajty, make(fit=True), make_image s černou/bílou a save jako PNG do dočasného souboru. Vrátíte absolutní cílový Path. Chyby nepohlcujte. Jiný správný zápis knihovny je v pořádku, nastavení a obsah zachovejte.

Tlačítko Spustit v Akademii při dostupné knihovně ukáže PNG ke stažení. Pro vlastní trvalý soubor uložte pracovní složku a spusťte ji v editoru. QR není šifrovaný: kdo jej přečte, získá celý vložený text. Do ukázky patří fiktivní inventární kód.
