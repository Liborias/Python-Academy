"""Úvodní Tkinter bez okna: stav, akce, omezený rozsah a chyby."""
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT/'lib'))
from dilna_check import check


class TkRunTest(unittest.TestCase):
    def run_prog(self, source, **options):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            program = root/'main.py'
            program.write_text(source, encoding='utf-8')
            with patch.dict(os.environ, DILNA_STUDENT=str(program), DILNA_RESULT=str(root/'result.json'), DILNA_DATA=str(root)):
                return check().tk_run(**options)

    def test_window_properties_and_no_mainloop(self):
        r = self.run_prog('import tkinter as tk\nw=tk.Tk()\nw.wm_title("Žluté okno")\nw.geometry("420x240")\nw.minsize(320,180)\nw.mainloop()')
        self.assertIsNone(r.error)
        self.assertEqual(r.mainloops, 1)
        root = r.widgets('root')[0]
        self.assertEqual((root['title'], root['geometry'], root['minsize'], root['visible']), ('Žluté okno', '420x240', [320,180], True))
        self.assertEqual(self.run_prog('import tkinter as tk\nw=tk.Tk()').mainloops, 0)
        self.assertEqual(r.widgets(index=99), [])

    def test_commands_are_delayed_and_snapshots_are_independent(self):
        r = self.run_prog('''import tkinter as tk
from tkinter import ttk
w=tk.Tk()
s=tk.StringVar(w, value="Čekám")
l=ttk.Label(w,textvariable=s)
l.pack()
ttk.Button(w,text="Změnit",command=lambda: s.set("Hotovo")).pack()
w.mainloop()
''', actions=[{'action':'click','text':'Změnit'}])
        self.assertIsNone(r.error)
        self.assertEqual(r.widgets('label')[0]['text'], 'Čekám')
        self.assertEqual(r.widgets('label',1)[0]['text'], 'Hotovo')
        self.assertEqual(r.widgets('label')[0]['id'], r.widgets('label',1)[0]['id'])

    def test_entry_editing_and_fresh_fill(self):
        r = self.run_prog('''from tkinter import Tk, END
from tkinter.ttk import Entry, Label, Button
w=Tk()
e=Entry(w);e.grid(row=0,column=0)
e.insert(0,"abc");e.delete(1,2);e.insert(1,"Ž")
print(e.get())
l=Label(w,text="Prázdné");l.grid(row=1,column=0)
Button(w,text="Číst",command=lambda: l.config(text=e.get())).grid(row=2,column=0)
w.mainloop()
''', actions=[{'action':'fill','value':'  Ema  '},{'action':'click','text':'Číst'},{'action':'fill','value':'Jan'},{'action':'click','text':'Číst'}])
        self.assertIsNone(r.error)
        self.assertEqual(r.out.strip(),'aŽc')
        self.assertEqual(r.widgets('label',2)[0]['text'],'  Ema  ')
        self.assertEqual(r.widgets('label',4)[0]['text'],'Jan')

    def test_parent_layout_and_unsupported_widgets(self):
        good = self.run_prog('''import tkinter as tk
w=tk.Tk()
f=tk.Frame(w);f.pack()
tk.Label(f,text="Uvnitř").grid()
w.mainloop()''')
        self.assertIsNone(good.error)
        self.assertTrue(good.widgets('label')[0]['visible'])
        bad = self.run_prog('import tkinter as tk\nw=tk.Tk()\ntk.Label(w).pack()\ntk.Entry(w).grid()\nw.mainloop()')
        self.assertEqual(bad.error['type'],'TclError')
        missing = self.run_prog('from tkinter import ttk\nttk.Treeview()')
        self.assertEqual(missing.error['type'],'AttributeError')

    def test_errors_limits_and_callback_line(self):
        broken = self.run_prog('import tkinter as tk\nw=tk.Tk()\ndef f():\n    return 1/0\ntk.Button(w,text="Chyba",command=f).pack()\nw.mainloop()',actions=[{'action':'click','text':'Chyba'}])
        self.assertEqual((broken.error['type'],broken.error['line']),('ZeroDivisionError',4))
        infinite = self.run_prog('while True:\n    pass',max_steps=50)
        self.assertEqual(infinite.error['type'],'RuntimeError')
        self.assertTrue(self.run_prog('import time\ntime.sleep(2)',timeout=.1).timed_out)
        self.assertEqual(self.run_prog('def :').error['type'],'SyntaxError')

    def test_validator_executes_tk_instead_of_only_compiling(self):
        sys.path.insert(0,str(ROOT))
        from tools import validate_courses as validator
        with tempfile.TemporaryDirectory() as temp:
            d=Path(temp)
            for code, expected in [('import tkinter as tk\nw=tk.Tk()\nw.mainloop()',False),('import tkinter as tk\nw=tk.Tk()',True),('import tkinter as tk\nraise ValueError("Chyba")',True)]:
                (d/'example.py').write_text(code,encoding='utf-8')
                before=len(validator.errors)
                validator.run_gui_example(d,d/'example.py')
                errors=validator.errors[before:];del validator.errors[before:]
                self.assertEqual(bool(errors),expected,errors)


if __name__ == '__main__':
    unittest.main()
