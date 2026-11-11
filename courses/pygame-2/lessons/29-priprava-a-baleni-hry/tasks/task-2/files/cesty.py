from pathlib import Path

def koren_aplikace(soubor, spustitelny, zmrazeno=False):
    zdroj = spustitelny if zmrazeno else soubor
    return Path(zdroj).resolve().parent

def chybejici_soubory(koren, povinne):
    koren = Path(koren)
    return sorted(jmeno for jmeno in povinne if not (koren / jmeno).is_file())

def prikaz_spusteni(python, skript):
    skript = Path(skript).resolve()
    if not isinstance(python, str) or not python.strip() or not skript.is_file() or skript.suffix.lower() != '.py':
        raise ValueError('Zadejte interpreter a existující Python soubor.')
    return [python, '-X', 'utf8', str(skript)]

def prikaz_baleni(python, skript, vystup, jmeno='KuryrskaSmena'):
    skript, vystup = Path(skript).resolve(), Path(vystup).resolve()
    platne_jmeno = (isinstance(jmeno, str) and 1 <= len(jmeno) <= 40 and jmeno.isascii()
                    and jmeno[0].isalpha() and all(c.isalnum() or c in '_-' for c in jmeno))
    if not isinstance(python, str) or not python.strip() or not platne_jmeno or not skript.is_file() or skript.suffix.lower() != '.py':
        raise ValueError('Neplatný interpreter, skript nebo název aplikace.')
    return [python, '-m', 'PyInstaller', '--onedir', '--console', '--clean', '--noconfirm',
            '--name', jmeno, '--distpath', str(vystup / 'dist'),
            '--workpath', str(vystup / 'build'), '--specpath', str(vystup / 'spec'), str(skript)]

def prikaz_testu(python, koren):
    testy = (Path(koren).resolve() / 'testy')
    if not isinstance(python, str) or not python.strip() or not testy.is_dir():
        raise ValueError('Zadejte interpreter a složku s adresářem testy.')
    return [python, '-m', 'unittest', 'discover', '-s', str(testy), '-p', 'test_*.py']
