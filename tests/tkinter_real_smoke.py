"""Skutečné Tk na grafické ploše: DISPLAY=:... python tests/tkinter_real_smoke.py [--shots DIR]."""
import argparse
import os
import runpy
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LESSONS = ['01-prvni-okno-a-mainloop', '02-popisky-a-pack', '03-tlacitka-a-zpetna-volani', '04-vstupni-pole-a-grid',
           '05-ramecky-a-zmena-velikosti', '06-enter-a-fokus', '07-promenne-a-volby', '08-projekt-prevodnik-vzdalenosti']
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--lesson', type=int, choices=range(1, len(LESSONS)+1))
parser.add_argument('--shots', type=Path)
args = parser.parse_args()
if not os.environ.get('DISPLAY'):
    raise SystemExit('Pro tento skutečný GUI test nastavte DISPLAY na dostupnou grafickou plochu.')
if args.lesson is None:
    for index in range(1, len(LESSONS)+1):
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

def descendants(widget):
    return [child for w in widget.winfo_children() for child in [w] + descendants(w)]

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
            elif args.lesson == 4:
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
            elif args.lesson == 5:
                frames = root.pack_slaves()
                assert len(frames) == 2 and all(isinstance(f,ttk.Frame) for f in frames)
                entry = next(w for w in frames[0].winfo_children() if isinstance(w,ttk.Entry))
                assert entry.winfo_manager() == 'grid' and entry.winfo_ismapped()
                assert frames[1].pack_slaves()[0].cget('text') == 'Formulář je připravený.'
                width = entry.winfo_width()
                root.geometry('700x300'); root.update_idletasks()
                assert entry.winfo_width() > width + 100
            elif args.lesson == 6:
                entry = next(w for w in children if isinstance(w,ttk.Entry))
                label = next(w for w in labels if w.cget('text') != 'Jméno:')
                # Bez správce oken nemá nové okno aktivaci systému. Vynutíme aktivaci,
                # nikoli cílový widget; Entry musí být vybrané studentským focus_set.
                root.tk.call('focus','-force',root.tk.call('focus','-lastfor',root))
                root.update()
                assert root.focus_get() is entry
                for text, use_key, expected in [('  Ema  ',True,'Ahoj, Ema!'),('   ',False,'Zadejte jméno.'),('  Žofie  Nová  ',True,'Ahoj, Žofie  Nová!')]:
                    before=label.cget('text')
                    entry.delete(0,tk.END);entry.insert(0,text)
                    assert label.cget('text') == before
                    if use_key:
                        entry.event_generate('<Return>');root.update()
                    else:
                        buttons['Pozdravit'].invoke()
                    assert label.cget('text') == expected
            elif args.lesson == 7:
                check=next(w for w in children if isinstance(w,ttk.Checkbutton))
                radios={w.cget('text'):w for w in children if isinstance(w,ttk.Radiobutton)}
                label=labels[0]
                assert not check.instate(['selected']) and radios['Osobní odběr'].instate(['selected'])
                for choice, fragile in [('Osobní odběr',False),('Kurýr',False),('Kurýr',True),('Osobní odběr',True),('Osobní odběr',False),('Kurýr',True)]:
                    before=label.cget('text')
                    radios[choice].invoke()
                    if check.instate(['selected']) != fragile:
                        check.invoke()
                    assert label.cget('text') == before
                    assert sum(w.instate(['selected']) for w in radios.values()) == 1
                    buttons['Zobrazit volby'].invoke()
                    name='odběr' if choice == 'Osobní odběr' else 'kurýr'
                    value='ano' if fragile else 'ne'
                    assert label.cget('text') == f'Doprava: {name}; křehké: {value}.'
            elif args.lesson == 8:
                all_widgets=descendants(root)
                entry=next(w for w in all_widgets if isinstance(w,ttk.Entry))
                label=next(w for w in all_widgets if isinstance(w,ttk.Label) and w.cget('text') != 'Vzdálenost:')
                button=next(w for w in all_widgets if isinstance(w,ttk.Button))
                radios={w.cget('text'):w for w in all_widgets if isinstance(w,ttk.Radiobutton)}
                root.tk.call('focus','-force',root.tk.call('focus','-lastfor',root));root.update()
                assert root.focus_get() is entry
                cases=[('Kilometry na metry','  1,25  ','1250.000 m'),('Metry na kilometry','1250','1.250 km'),
                       ('Metry na kilometry','-1','Zadejte platné nezáporné číslo.'),('Kilometry na metry','nan','Zadejte platné nezáporné číslo.'),
                       ('Kilometry na metry','inf','Zadejte platné nezáporné číslo.'),('Kilometry na metry','1e308','Zadejte platné nezáporné číslo.'),
                       ('Kilometry na metry','','Zadejte platné nezáporné číslo.'),('Kilometry na metry','0','0.000 m'),
                       ('Metry na kilometry','1250','1.250 km')]
                for index,(direction,text,expected) in enumerate(cases):
                    before=label.cget('text')
                    radios[direction].invoke();entry.delete(0,tk.END);entry.insert(0,text)
                    assert label.cget('text') == before
                    if index % 2:
                        button.invoke()
                    else:
                        entry.event_generate('<Return>');root.update()
                    assert label.cget('text') == expected,(text,label.cget('text'))
                    assert entry.get() == text
                assert len(descendants(root)) == len(all_widgets)
            root.update_idletasks()
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
    if args.lesson == 8:
        namespace=runpy.run_path(str(ROOT/'courses/tkinter-api/lessons'/LESSONS[7]/'example.py'),run_name='student')
        assert tk._default_root is None
        assert namespace['preved_vzdalenost'](1.25,'km-m') == 1250
    runpy.run_path(str(ROOT/'courses/tkinter-api/lessons'/LESSONS[args.lesson-1]/'example.py'), run_name='__main__')
    assert len(entered) == 1 and not failures, failures
    print(f'OK: skutečné Tk {tk.TkVersion}, lekce {args.lesson}')
finally:
    tk.Tk.mainloop = original
