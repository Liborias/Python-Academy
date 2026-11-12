## Zkušební inventární štítek

Před dokončením půjčovny přidáme jednoduchou kontrolu přepisu. K textovému tělu čísla doplníme jednu Luhnovu číslici. Při zadání pak poznáme některé chyby dřív, než začneme hledat v databázi. Používáme zkušební inventární čísla.

```python
# Číslo předmětu uchováváme jako text: úvodní nula je součást kódu.
telo = '0007'
print(telo, len(telo))
```

Převod na int by nuly odstranil. Samotný algoritmus přijímá ASCII 0–9, ne znaménka, mezery či jiné Unicode číslice. Pomocník telo_kodu tyto podmínky ověří, pro tělo délky 1–32, jinak ValueError.

## Pořadí zprava

Při tvorbě číslice začneme zprava v těle a zdvojnásobíme poslední, pak každou druhou číslici. Výsledek větší než 9 zmenšíme o 9. Vše sečteme a doplníme číslici tak, aby součet včetně ní byl dělitelný deseti. Pro tělo 12 je součet 1+4=5, kontrolní číslice 5 a celý kód 125.

Kontrolní číslice na konci se už nezdvojnásobuje. Právě její přidání vysvětluje paritu při tvorbě z těla. Zkuste jedno- i víceciferné tělo, nuly a maximální délku. První doplňková ukázka změní jednu číslici.

## Co kontrola nezaručí

Luhn není podpis, heslo ani potvrzení identity předmětu. Dvě různá čísla mohou být obě platná. Dokonce přeházení 09/90 někdy zůstane bez chyby: 1099 i 1909 projdou. Kontrola nenahradí vyhledání existující pomůcky a ověření její dostupnosti.

## Váš úkol

Doplňte **kontrolni_cislice(telo)** a **platny_kod(kod)**. První ověří tělo pomocníkem, provede součet a vrátí jednu ASCII číslici jako str. Druhá vrací bool; pro neplatný typ/formát, délku mimo 2–33 či ne-ASCII číslice False. Jinak ověří poslední číslici proti výpočtu z předchozí části.

Úvodní nuly jsou pro obecný Luhn dovoleny. Pozdější půjčovna má užší formát kladného databázového id bez úvodních nul; jsou to dvě různé vrstvy pravidel. Výpočet je standardní Python, bez pip balíčků, s vysvětlením a možným řešením.
