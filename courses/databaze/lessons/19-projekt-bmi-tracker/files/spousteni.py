from contextlib import closing
import tkinter as tk

def spust(Aplikace, Tracker, cesta, ukazka=False):
    with closing(Tracker(cesta)) as model:
        if ukazka:
            model.pridej('2026-04-01', 80, 180, 'Ukázka')
            model.pridej('2026-04-05', 81, 180, 'Další ukázka')
        try:
            okno = tk.Tk()
        except tk.TclError:
            raise ValueError('Není dostupná grafická plocha pro Tkinter.') from None
        okno.title('BMI tracker: měření v čase')
        okno.geometry('840x700')
        okno.minsize(650, 600)
        try:
            Aplikace(okno, model)
            okno.mainloop()
        finally:
            try:
                okno.destroy()
            except tk.TclError:
                pass
