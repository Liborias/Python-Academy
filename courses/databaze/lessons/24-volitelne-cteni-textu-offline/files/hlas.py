"""Pevné argumenty, text jde přes stdin: žádný shell ani síťová služba."""
import platform
import shutil

POWERSHELL = "[Console]::InputEncoding=[System.Text.UTF8Encoding]::new($false); $text=[Console]::In.ReadToEnd(); Add-Type -AssemblyName System.Speech; $hlas=[System.Speech.Synthesis.SpeechSynthesizer]::new(); try { $hlas.Speak($text) } finally { $hlas.Dispose() }"

def vyber_prikaz(system=None, najdi=None):
    system = platform.system() if system is None else system
    najdi = shutil.which if najdi is None else najdi
    if system=='Windows':
        program = najdi('powershell.exe')
        return [program,'-NoProfile','-NonInteractive','-Command',POWERSHELL] if program else None
    if system=='Darwin':
        program = najdi('say')
        return [program,'-f','-'] if program else None
    if system=='Linux':
        program = najdi('espeak-ng') or najdi('espeak')
        return [program,'--stdin','-v','cs'] if program else None
    return None

def over_text(text):
    if not isinstance(text,str) or not text.strip() or len(text)>2000:
        raise ValueError('Pro řeč zadejte 1 až 2000 znaků textu.')
    try:
        text.encode('utf-8')
    except UnicodeError:
        raise ValueError('Text musí být platný UTF-8.') from None
    return text
