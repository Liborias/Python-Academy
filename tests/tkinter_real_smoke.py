"""Skutečné Tk na grafické ploše: DISPLAY=:... python tests/tkinter_real_smoke.py [--shots DIR]."""
import argparse
import os
import runpy
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LESSONS = ['01-prvni-okno-a-mainloop', '02-popisky-a-pack', '03-tlacitka-a-zpetna-volani', '04-vstupni-pole-a-grid']
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--lesson', type=int, choices=range(1, 5))
parser.add_argument('--shots', type=Path)
args = parser.parse_args()
if not os.environ.get('DISPLAY'):
    raise SystemExit('Pro tento skutečný GUI test nastavte DISPLAY na dostupnou grafickou plochu.')
if args.lesson is None:
    for index in range(1, 5):
        command = [sys.executable, __file__, '--lesson', str(index)]
        if args.shots:
            command += ['--shots', str(args.shots)]
        result = subprocess.run(command, capture_output=True, text=True, timeout=15)
        if result.returncode:
            raise SystemExit(result.stdout + result.stderr)
        print(result.stdout.strip())
    raise SystemExit(0)

import tkinter as tk
from tkinter import ttk
original = tk.Tk.mainloop
failures = []
entered = []

def mainloop(root, *a, **kw):
    entered.append(root)
    root.report_callback_exception = lambda cls, error, tb: failures.append(error)
    def inspect():
        try:
            root.update_idletasks()
            children = root.winfo_children()
            labels = [w for w in children if isinstance(w, ttk.Label)]
            buttons = {w.cget('text'): w for w in children if isinstance(w, ttk.Button)}
            if args.lesson == 1:
                assert root.title() == 'Moje první okno'
                assert (root.winfo_width(), root.winfo_height()) == (420, 240)
                assert root.minsize() == (320, 180)
            elif args.lesson == 2:
                assert [w.cget('text') for w in root.pack_slaves()] == ['Expediční přehled', 'Stav: připraveno']
                assert all(w.winfo_ismapped() for w in labels)
            elif args.lesson == 3:
                assert labels[0].cget('text') == 'Čekám na potvrzení.'
                for name, expected in [('Potvrdit', 'Akce potvrzena.'), ('Potvrdit', 'Akce potvrzena.'), ('Obnovit', 'Čekám na potvrzení.'), ('Potvrdit', 'Akce potvrzena.')]:
                    buttons[name].invoke(); root.update_idletasks()
                    assert labels[0].cget('text') == expected
                assert len(root.winfo_children()) == 3
            else:
                entry = next(w for w in children if isinstance(w, ttk.Entry))
                label = next(w for w in labels if w.cget('text') != 'Vaše jméno:')
                assert label.cget('text') == 'Zadejte jméno a klikněte.'
                for text, expected in [('', 'Zadejte jméno.'), ('  Ema  ', 'Ahoj, Ema!'), ('   ', 'Zadejte jméno.'), ('  Žofie  Nová  ', 'Ahoj, Žofie  Nová!')]:
                    before = label.cget('text')
                    entry.delete(0, tk.END); entry.insert(0, text)
                    assert label.cget('text') == before
                    buttons['Pozdravit'].invoke(); root.update_idletasks()
                    assert label.cget('text') == expected
                width = entry.winfo_width()
                root.geometry('600x260'); root.update_idletasks()
                assert entry.winfo_width() > width
                assert len(root.winfo_children()) == 4
            assert not failures, failures
            if args.shots:
                args.shots.mkdir(parents=True, exist_ok=True)
                capture = 'from PIL import ImageGrab; import os,sys; ImageGrab.grab(xdisplay=os.environ["DISPLAY"]).save(sys.argv[1])'
                subprocess.run(['python3', '-c', capture, str(args.shots/f'tk-real-{args.lesson}.png')], check=True, timeout=5)
        except BaseException as exc:
            failures.append(exc)
        finally:
            root.destroy()
    root.after(100, inspect)
    root.after(5000, root.destroy)
    return original(root, *a, **kw)

tk.Tk.mainloop = mainloop
try:
    runpy.run_path(str(ROOT/'courses/tkinter-api/lessons'/LESSONS[args.lesson-1]/'example.py'), run_name='__main__')
    assert len(entered) == 1 and not failures, failures
    print(f'OK: skutečné Tk {tk.TkVersion}, lekce {args.lesson}')
finally:
    tk.Tk.mainloop = original
