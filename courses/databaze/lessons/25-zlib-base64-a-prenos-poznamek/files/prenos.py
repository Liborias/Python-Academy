import json
from pathlib import Path
from format_dat import MAX_BALICEK
from soubory import bezpecny_cil

def prenos(akce, sezeni, cesta, zabal, rozbal):
    if akce=='export':
        texty = [text for _,text in sezeni.seznam()]
        obsah = json.dumps({'verze':1,'poznamky':texty},ensure_ascii=False)
        balicek = zabal(obsah)
        with bezpecny_cil(cesta,sezeni.ucty.cesta) as (docasny,cil):
            docasny.write_text(balicek,encoding='ascii')
        return len(texty)
    with Path(cesta).open('rb') as file:
        data = file.read(MAX_BALICEK+1)
    if len(data)>MAX_BALICEK:
        raise ValueError('Soubor balíčku je příliš velký.')
    try:
        obsah = json.loads(rozbal(data.decode('ascii')))
    except (UnicodeError,ValueError):
        raise ValueError('Neplatný soubor poznámek.') from None
    if (not isinstance(obsah,dict) or set(obsah)!={'verze','poznamky'}
            or type(obsah['verze']) is not int or obsah['verze']!=1):
        raise ValueError('Neznámá verze poznámek.')
    return sezeni.importuj(obsah['poznamky'])
