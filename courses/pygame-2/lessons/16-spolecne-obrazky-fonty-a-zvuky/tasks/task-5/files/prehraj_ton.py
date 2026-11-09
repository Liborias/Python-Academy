"""Volitelný krátký vlastní tón: python prehraj_ton.py --play."""
from pathlib import Path
import subprocess
import sys

def worker():
    import pygame
    from podklady import priprav_media
    cesta=priprav_media()/'ton.wav'
    try:
        pygame.mixer.init()
        zvuk=pygame.mixer.Sound(str(cesta))
        zvuk.set_volume(0.15)
        kanal=zvuk.play()
        if kanal is None:print('Není volný zvukový kanál.')
        else:
            print('Přehrávám krátký vlastní tón; skutečná slyšitelnost závisí na zařízení.')
            pygame.time.wait(250)
    except pygame.error as exc:
        print('Zvuk není dostupný:',exc)
    finally:
        pygame.mixer.quit()

if __name__=='__main__':
    if '--worker' in sys.argv:worker()
    elif '--play' not in sys.argv:print('Pro volitelný zvuk použijte: python prehraj_ton.py --play')
    else:
        try:subprocess.run([sys.executable,str(Path(__file__).resolve()),'--worker'],check=False,timeout=5)
        except subprocess.TimeoutExpired:print('Zvukové zařízení nereaguje; pokus skončil po 5 sekundách.')
