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

    def test_keyboard_focus_event_argument_and_break(self):
        r = self.run_prog('''import tkinter as tk
w=tk.Tk()
e=tk.Entry(w); e.pack(); e.focus_set()
l=tk.Label(w,text="Čekám"); l.pack()
def enter(event):
    assert event.widget is e and event.keysym == "Return"
    l.config(text=e.get())
    return "break"
e.bind("<KeyPress-Return>",enter)
w.bind("<Return>",lambda event: l.config(text="Chybná druhá reakce"))
w.mainloop()
''', actions=[{'action':'fill','value':'Žofie'}, {'action':'key'}])
        self.assertIsNone(r.error)
        self.assertTrue(r.widgets('entry')[0]['focused'])
        self.assertEqual(r.widgets('label',-1)[0]['text'],'Žofie')
        self.assertEqual(r.widgets('entry')[0]['bindings'],['<Return>'])
        missing=self.run_prog('import tkinter as tk\nw=tk.Tk()\ntk.Entry(w).pack()\nw.mainloop()',actions=[{'action':'key'}])
        self.assertEqual(missing.error['type'],'TclError')
        bad=self.run_prog('import tkinter as tk\nw=tk.Tk()\ne=tk.Entry(w);e.pack();e.focus_set()\ne.bind("<Return>",lambda: None)\nw.mainloop()',actions=[{'action':'key'}])
        self.assertEqual(bad.error['type'],'TypeError')

    def test_binding_replace_and_add_and_parent_dispatch(self):
        r=self.run_prog('''import tkinter as tk
w=tk.Tk();e=tk.Entry(w);e.pack();e.focus_set()
events=[]
e.bind("<Return>",lambda event: events.append("old"))
e.bind("<Return>",lambda event: events.append("new"))
e.bind("<Return>",lambda event: events.append("extra"),add="+")
w.bind("<Return>",lambda event: events.append("root"))
w.mainloop()
print(events)
''',actions=[{'action':'key'}])
        self.assertIsNone(r.error)
        self.assertEqual(r.out.strip(),"['new', 'extra', 'root']")

    def test_choices_update_variables_before_callback_and_share_radio_group(self):
        r=self.run_prog('''import tkinter as tk
from tkinter import ttk
w=tk.Tk();c=tk.IntVar(w,value=0);s=tk.StringVar(w,value="a")
l=ttk.Label(w,text="Čekám");l.pack()
ttk.Checkbutton(w,text="C",variable=c,command=lambda: l.config(text=str(c.get()))).pack()
ttk.Radiobutton(w,text="A",variable=s,value="a").pack()
ttk.Radiobutton(w,text="B",variable=s,value="b").pack()
ttk.Button(w,text="Číst",command=lambda: l.config(text=s.get())).pack()
w.mainloop()
''',actions=[{'action':'click','text':t} for t in ['C','B','B','Číst','C','A']])
        self.assertIsNone(r.error)
        self.assertFalse(r.widgets('checkbutton')[0]['selected'])
        self.assertEqual(r.widgets('label',1)[0]['text'],'1')
        self.assertEqual([w['selected'] for w in r.widgets('radiobutton',2)],[False,True])
        self.assertEqual([w['selected'] for w in r.widgets('radiobutton',3)],[False,True])
        self.assertEqual(r.widgets('label',4)[0]['text'],'b')
        self.assertEqual(r.widgets('label',5)[0]['text'],'0')
        self.assertEqual([w['selected'] for w in r.widgets('radiobutton',6)],[True,False])

    def test_calls_without_starting_window_and_per_call_exceptions(self):
        r=self.run_prog('''import tkinter as tk
def double(x): return x*2
def fail(): raise ValueError("neplatné")
if __name__ == "__main__":
    w=tk.Tk();w.mainloop()
''',run_name='student',calls=[{'name':'double','args':[1.25]},{'name':'fail'},{'name':'double','args':[3]}])
        self.assertIsNone(r.error)
        self.assertEqual(r.widgets(),[])
        self.assertEqual(r.mainloops,0)
        self.assertEqual(r.calls[0],{'value':2.5,'error':None})
        self.assertEqual(r.calls[1]['error']['type'],'ValueError')
        self.assertEqual(r.calls[2],{'value':6,'error':None})

    def test_listbox_endpoints_selection_and_snapshot_independence(self):
        r=self.run_prog('''import tkinter as tk
w=tk.Tk();l=tk.Listbox(w);l.pack()
l.insert(tk.END,"A","B","A")
assert l.get(0,tk.END)==("A","B","A")
l.selection_set(2)
assert l.curselection()==(2,)
count=[]
l.bind("<<ListboxSelect>>",lambda event: count.append(l.curselection()))
assert not count
tk.Button(w,text="Smazat",command=lambda: l.delete(2)).pack()
w.mainloop()
print(count)
''',actions=[{'action':'select','index':2},{'action':'click','text':'Smazat'},{'action':'select','index':None}])
        self.assertIsNone(r.error)
        self.assertEqual(r.widgets('listbox')[0]['items'],['A','B','A'])
        self.assertEqual(r.widgets('listbox',2)[0]['items'],['A','B'])
        self.assertEqual(r.widgets('listbox',2)[0]['selection'],[])
        self.assertEqual(r.out.strip(),'[(2,), ()]')

    def test_text_indices_and_implicit_final_newline(self):
        r=self.run_prog('''import tkinter as tk
w=tk.Tk();t=tk.Text(w);t.pack()
assert t.get("1.0","end")=="\\n"
assert t.get("1.0","end-1c")==""
t.insert("1.0","A\\nB\\n")
assert t.get("1.0","end")=="A\\nB\\n\\n"
assert t.get("2.0","2.1")=="B"
t.delete("2.0","2.1")
assert t.get("1.0","end-1c")=="A\\n\\n"
w.mainloop()
''',actions=[{'action':'fill_text','value':'Žofie\nNová\n'}])
        self.assertIsNone(r.error)
        self.assertEqual(r.widgets('text')[0]['value'],'A\n\n')
        self.assertEqual(r.widgets('text',1)[0]['value'],'Žofie\nNová\n')

    def test_readonly_text_ignores_edits_until_enabled(self):
        r=self.run_prog('''import tkinter as tk
w=tk.Tk();t=tk.Text(w);t.pack();t.insert("1.0","Původní")
t.config(state="disabled")
def enable():
    t.config(state="normal")
tk.Button(w,text="Povolit",command=enable).pack()
w.mainloop()
''',actions=[{'action':'fill_text','value':'Zakázaná změna'},{'action':'click','text':'Povolit'},{'action':'fill_text','value':'Nová'}])
        self.assertIsNone(r.error)
        self.assertEqual(r.widgets('text',1)[0]['value'],'Původní')
        self.assertEqual(r.widgets('text',3)[0]['value'],'Nová')

    def test_scrollbar_and_text_report_both_directions(self):
        r=self.run_prog('''import tkinter as tk
from tkinter import ttk
w=tk.Tk();t=tk.Text(w,height=5);t.grid(row=0,column=0)
b=ttk.Scrollbar(w,orient="vertical",command=t.yview);b.grid(row=0,column=1)
t.config(yscrollcommand=b.set)
t.insert("1.0","\\n".join(str(i) for i in range(30)))
w.rowconfigure(0,weight=1)
w.mainloop()
''',actions=[{'action':'scroll','fraction':.5},{'action':'scroll','kind':'text','number':-1,'what':'pages'}])
        self.assertIsNone(r.error)
        self.assertGreater(r.widgets('text',1)[0]['yview'][0],r.widgets('text',2)[0]['yview'][0])
        for i in range(3):
            self.assertEqual(r.widgets('text',i)[0]['yview'],r.widgets('scrollbar',i)[0]['range'])
        self.assertEqual(r.widgets('root')[0]['rows'],{'0':{'weight':1}})

    def test_listbox_scroll_updates_range_after_rows_are_removed(self):
        r=self.run_prog('''import tkinter as tk
w=tk.Tk();l=tk.Listbox(w,height=5);l.pack()
b=tk.Scrollbar(w,command=l.yview);b.pack();l.config(yscrollcommand=b.set)
l.insert("end",*range(30))
tk.Button(w,text="Vyprázdnit",command=lambda:l.delete(0,"end")).pack()
w.mainloop()
''',actions=[{'action':'scroll','fraction':.5},{'action':'click','text':'Vyprázdnit'}])
        self.assertIsNone(r.error)
        self.assertGreater(r.widgets('listbox',1)[0]['yview'][0],0)
        self.assertEqual(r.widgets('listbox',2)[0]['items'],[])
        self.assertEqual(r.widgets('scrollbar',2)[0]['range'],[0,1])
        self.assertEqual(r.widgets('scrollbar')[0]['orient'],'vertical')

    def test_file_dialog_answers_cancel_and_mismatched_dialog(self):
        source='''import tkinter as tk
from tkinter import filedialog
w=tk.Tk()
tk.Button(w,text="Otevřít",command=lambda:print(repr(filedialog.askopenfilename(parent=w)))).pack()
tk.Button(w,text="Uložit",command=lambda:print(repr(filedialog.asksaveasfilename(parent=w)))).pack()
w.mainloop()
'''
        r=self.run_prog(source,actions=[{'action':'click','text':'Otevřít'},{'action':'click','text':'Uložit'}],
                        dialogs=[{'kind':'open','path':''},{'kind':'save','path':'česká cesta.json'}])
        self.assertIsNone(r.error)
        self.assertEqual(r.out.splitlines(),["''","'česká cesta.json'"])
        self.assertEqual(r.dialogs,[{'kind':'open','path':''},{'kind':'save','path':'česká cesta.json'}])
        bad=self.run_prog(source,actions=[{'action':'click','text':'Otevřít'}],dialogs=[{'kind':'save','path':''}])
        self.assertEqual(bad.error['type'],'TclError')

    def test_after_arguments_order_and_cancel_run_in_main_thread(self):
        r=self.run_prog('''import threading
import tkinter as tk
w=tk.Tk();owner=threading.get_ident();events=[]
def add(value):
    assert threading.get_ident()==owner
    events.append(value)
w.after(5,add,"první")
token=w.after(5,add,"zrušené");w.after_cancel(token)
w.after(10,add,"druhé")
w.mainloop()
print(events)
''',actions=[{'action':'wait','ms':30}])
        self.assertIsNone(r.error)
        self.assertEqual(r.out.strip(),"['první', 'druhé']")
        self.assertEqual(len(r.callbacks),2)

    def test_real_worker_queue_and_wait_until_callback(self):
        r=self.run_prog('''import queue,threading,time
import tkinter as tk
w=tk.Tk();q=queue.Queue();b=tk.Button(w,text="Hotovo",state="disabled");b.pack()
def worker():
    time.sleep(.03);q.put("výsledek")
def poll():
    try:value=q.get_nowait()
    except queue.Empty:w.after(5,poll);return
    assert value=="výsledek"
    b.config(state="normal")
threading.Thread(target=worker,daemon=True).start();w.after(5,poll)
w.mainloop()
''',actions=[{'action':'wait','until':{'text':'Hotovo'},'timeout':1}])
        self.assertIsNone(r.error)
        self.assertEqual(r.widgets('button',-1)[0]['state'],'normal')

    def test_worker_cannot_access_widget_or_tk_variable_even_if_caught(self):
        for operation in ['label.config(text="Špatně")','value.get()','w.after(1,lambda:None)']:
            source='''import threading
import tkinter as tk
w=tk.Tk();label=tk.Label(w,text="Původní");label.pack();value=tk.StringVar(w,value="A")
def worker():
    try:
        OPERATION
    except RuntimeError:
        pass
t=threading.Thread(target=worker);t.start();t.join()
w.mainloop()
'''.replace('OPERATION',operation)
            with self.subTest(operation=operation):
                r=self.run_prog(source)
                self.assertEqual(r.error['type'],'RuntimeError')
                self.assertIn('hlavní vlákno',r.error['msg'])

    def test_scripted_http_uses_real_response_exceptions_and_worker_log(self):
        r=self.run_prog('''import queue,threading
import requests
import tkinter as tk
w=tk.Tk();q=queue.Queue();b=tk.Button(w,text="Hotovo",state="disabled");b.pack()
def worker():
    with requests.Session() as s:
        response=s.get("http://test.invalid/kurz",params={"mena":"EUR"},timeout=2)
        response.raise_for_status()
        assert response.json()=={"mena":"EUR"}
        try:s.get("http://test.invalid/kurz",timeout=.1)
        except requests.Timeout:pass
        else:raise AssertionError("Chybí timeout")
    q.put(True)
def poll():
    try:q.get_nowait()
    except queue.Empty:w.after(5,poll);return
    b.config(state="normal")
threading.Thread(target=worker,daemon=True).start();w.after(5,poll);w.mainloop()
''',actions=[{'action':'wait','until':{'text':'Hotovo'},'timeout':1}],http=[{'json':{'mena':'EUR'},'delay_ms':20},{'error':'Timeout'}])
        self.assertIsNone(r.error)
        self.assertEqual(len(r.http),2)
        self.assertTrue(all(not row['main_thread'] for row in r.http))
        self.assertEqual(r.http[0]['params'],{'mena':'EUR'})

    def test_disabled_entry_ignores_fill_but_normal_entry_accepts_it(self):
        r=self.run_prog('''import tkinter as tk
w=tk.Tk();e=tk.Entry(w);e.pack();e.insert(0,"Původní");e.config(state="disabled")
tk.Button(w,text="Povolit",command=lambda:e.config(state="normal")).pack()
w.mainloop()
''',actions=[{'action':'fill','value':'Zakázáno'},{'action':'click','text':'Povolit'},{'action':'fill','value':'Nové'}])
        self.assertIsNone(r.error)
        self.assertEqual(r.widgets('entry',1)[0]['value'],'Původní')
        self.assertEqual(r.widgets('entry',3)[0]['value'],'Nové')

    def test_extra_environment_applies_only_to_student_process(self):
        before=os.environ.get('DILNA_SMTP_TIMEOUT')
        r=self.run_prog('''import os
import tkinter as tk
w=tk.Tk();tk.Label(w,text=os.environ["DILNA_SMTP_TIMEOUT"]).pack();w.mainloop()
''',extra_env={'DILNA_SMTP_TIMEOUT':'0.05'})
        self.assertIsNone(r.error)
        self.assertEqual(r.widgets('label')[0]['text'],'0.05')
        self.assertEqual(os.environ.get('DILNA_SMTP_TIMEOUT'),before)


if __name__ == '__main__':
    unittest.main()
