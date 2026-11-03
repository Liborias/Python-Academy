## Síť nikdy není jistota

Při stahování může selhat spousta věcí: stránka neexistuje, server má chybu, spojení je pomalé nebo se vůbec nepřipojíte. Slušný program s tím počítá.

## Stavový kód a raise_for_status

`requests.get` **nehlásí chybu**, když server odpoví `404` nebo `500`; vrátí odpověď, jako by vše bylo v pořádku. Chybu musíte vyvolat sami metodou `raise_for_status()`: pro úspěšné kódy nedělá nic, pro chybové vyvolá výjimku `requests.HTTPError`.

```python
odpoved = requests.get(url, timeout=3)
odpoved.raise_for_status()      # při 404 nebo 500 vznikne výjimka
```

## Timeout

Bez `timeout` může program čekat na pomalý server donekonečna. Parametr `timeout=3` říká „čekej nejvýš 3 sekundy“, potom vznikne výjimka `requests.Timeout`. **Piště `timeout` vždy.**

## Zachycení výjimek

Všechny výjimky balíčku `requests` mají společného předka `requests.RequestException`, takže jedním `except` zachytíte špatný stavový kód, timeout i nepřipojení:

```python
try:
    odpoved = requests.get(url, timeout=3)
    odpoved.raise_for_status()
except requests.RequestException:
    return None
return odpoved.text
```

## Zkusit znovu

Některé chyby jsou jen chvilkové, a tak stačí chvíli počkat a požadavek zopakovat. Počet pokusů ale musí být omezený (cyklus `for` s `range`), jinak byste server zahltili. Mezi pokusy se čeká pomocí `time.sleep(sekundy)`.

Místní server pro to má adresu `/_nestabilni/jmeno`: první dva dotazy na dané jméno selžou (kód 500), třetí uspěje. A adresa `/_pomalu/3` odpoví až za 3 sekundy.