"""Malá náhrada Tkinteru pro úvodní lekce, nikoli vykreslovací engine Tk.

Samostatný proces: tkrun.py program.py spec.json out.json. Zaznamená okno,
rozložení a stav widgetů před akcemi i po vyplnění Entry/kliknutí na Button.
Nepodporované části Tkinteru selžou; skutečný vzhled se ověřuje zvlášť s Tk.
"""
import contextlib
import io
import json
import os
import sys
import traceback
import types

student, spec_path, out_path = sys.argv[1:4]
with open(spec_path, encoding='utf-8') as file:
    spec = json.load(file)
widgets = []
default_root = None
layout_order = 0
mainloops = 0
snapshots = []
steps = 0
focused = None
dialog_answers = list(spec.get('dialogs', []))
dialog_log = []


class TclError(Exception):
    pass


class Variable:
    def __init__(self, master=None, value='', name=None):
        self.value = value
    def get(self):
        return self.value
    def set(self, value):
        self.value = value


class StringVar(Variable):
    def get(self):
        return str(self.value)


class IntVar(Variable):
    def __init__(self, master=None, value=0, name=None):
        super().__init__(master, value, name)
    def get(self):
        return int(self.value)


def event_key(sequence):
    return '<Return>' if sequence in ('<Return>', '<Key-Return>', '<KeyPress-Return>') else sequence


class Widget:
    kind = 'widget'
    def __init__(self, master=None, cnf=None, **options):
        global default_root
        if len(widgets) >= 200:
            raise TclError('Příliš mnoho widgetů')
        if self.kind != 'root' and master is None:
            if default_root is None:
                default_root = Tk()
            master = default_root
        if master is not None and not isinstance(master, Widget):
            raise TclError('Rodič musí být widget')
        self.master = master
        self.id = f'w{len(widgets)}'
        self.options = dict(cnf or {}, **options)
        self.layout = {}
        self.manager = ''
        self.order = -1
        self.alive = True
        self.visible = True
        self.columns = {}
        self.rows = {}
        self.bindings = {}
        widgets.append(self)
    def configure(self, cnf=None, **options):
        self.options.update(cnf or {})
        self.options.update(options)
    config = configure
    def cget(self, key):
        if key == 'text' and 'textvariable' in self.options:
            return str(self.options['textvariable'].get())
        return self.options.get(key, '')
    def __getitem__(self, key):
        return self.cget(key)
    def __setitem__(self, key, value):
        self.configure(**{key: value})
    def _manage(self, manager, options):
        global layout_order
        if self.master is not None and manager in ('pack', 'grid'):
            for sibling in self.master.winfo_children():
                if sibling is not self and sibling.manager in ('pack', 'grid') and sibling.manager != manager:
                    raise TclError('V jednom rodiči nelze míchat pack a grid')
        if self.manager != manager:
            self.order = layout_order
            layout_order += 1
        self.manager = manager
        self.layout.update(options)
    def pack(self, cnf=None, **options):
        self._manage('pack', dict(cnf or {}, **options))
    def grid(self, cnf=None, **options):
        self._manage('grid', dict(cnf or {}, **options))
    def place(self, cnf=None, **options):
        self._manage('place', dict(cnf or {}, **options))
    def pack_forget(self):
        self.manager = ''
    grid_forget = pack_forget
    def pack_info(self):
        return dict(self.layout) if self.manager == 'pack' else {}
    def grid_info(self):
        return dict(self.layout) if self.manager == 'grid' else {}
    def winfo_manager(self):
        return self.manager
    def winfo_children(self):
        return [w for w in widgets if w.master is self and w.alive]
    def winfo_exists(self):
        return self.alive
    def destroy(self):
        for child in self.winfo_children():
            child.destroy()
        self.alive = False
    def columnconfigure(self, index, **options):
        self.columns[str(index)] = dict(options)
    grid_columnconfigure = columnconfigure
    def rowconfigure(self, index, **options):
        self.rows[str(index)] = dict(options)
    grid_rowconfigure = rowconfigure
    def bind(self, sequence=None, func=None, add=None):
        if sequence is None:
            return tuple(self.bindings)
        sequence = event_key(sequence)
        if func is None:
            return 'bound' if self.bindings.get(sequence) else ''
        if not callable(func):
            raise TclError('Událost potřebuje volatelnou funkci')
        if add not in (True, '+'):
            self.bindings[sequence] = []
        self.bindings.setdefault(sequence, []).append(func)
        return str(len(self.bindings[sequence]))
    def focus_set(self):
        global focused
        focused = self
    focus = focus_set
    def focus_get(self):
        return focused
    def event_generate(self, sequence, **options):
        sequence = event_key(sequence)
        event = types.SimpleNamespace(widget=self, keysym='Return' if sequence == '<Return>' else '', **options)
        # V tomto rozsahu pouze vazba na widget a jeho hlavní okno; bez třídních vazeb Tk.
        root = self
        while root.master is not None:
            root = root.master
        for target in ([self, root] if root is not self else [self]):
            for callback in target.bindings.get(sequence, []):
                if callback(event) == 'break':
                    return


class Tk(Widget):
    kind = 'root'
    def __init__(self, **options):
        global default_root
        super().__init__(**options)
        self.caption = 'tk'
        self.size = ''
        self.minimum = (1, 1)
        default_root = self
    def title(self, value=None):
        if value is not None:
            self.caption = value
        return self.caption
    def geometry(self, value=None):
        if value is not None:
            self.size = value
        return self.size
    def minsize(self, width=None, height=None):
        if width is not None and height is not None:
            self.minimum = (int(width), int(height))
        return self.minimum
    wm_title = title
    wm_geometry = geometry
    wm_minsize = minsize
    def withdraw(self):
        self.visible = False
    def deiconify(self):
        self.visible = True
    def mainloop(self, n=0):
        global mainloops
        mainloops += 1
        if mainloops != 1:
            raise TclError('Použijte jednu hlavní smyčku')
        for widget in widgets:
            if isinstance(widget, VerticalView):
                widget._notify_scroll()
        snapshots.append(snapshot())
        for action in spec.get('actions', []):
            if action.get('action') == 'fill':
                entries = [w for w in widgets if isinstance(w, Entry) and shown(w)]
                if len(entries) != 1:
                    raise TclError('Vyplnění vyžaduje právě jedno viditelné Entry')
                entries[0].delete(0, 'end')
                entries[0].insert(0, action['value'])
            elif action.get('action') == 'click':
                buttons = [w for w in widgets if isinstance(w, Button) and shown(w) and w.cget('text') == action.get('text')]
                if len(buttons) != 1:
                    raise TclError(f"Tlačítko {action.get('text')!r} není jednoznačně dostupné")
                buttons[0].invoke()
            elif action.get('action') == 'key':
                if focused is None or not shown(focused):
                    raise TclError('Klávesa potřebuje viditelný widget s fokusem')
                focused.event_generate(action.get('sequence', '<Return>'))
            elif action.get('action') in ('select', 'fill_text', 'scroll'):
                kind = action.get('kind', {'select': 'listbox', 'fill_text': 'text', 'scroll': 'scrollbar'}[action['action']])
                targets = [w for w in widgets if w.kind == kind and shown(w)]
                if len(targets) != 1:
                    raise TclError(f'Akce vyžaduje právě jeden viditelný {kind}')
                target = targets[0]
                if action['action'] == 'select':
                    target.selection_clear(0, 'end')
                    if action.get('index') is not None:
                        index = int(action['index'])
                        if not 0 <= index < target.size():
                            raise TclError('Test vybral neexistující položku')
                        target.selection_set(index)
                    target.event_generate('<<ListboxSelect>>')
                elif action['action'] == 'fill_text':
                    target.delete('1.0', 'end')
                    target.insert('1.0', action['value'])
                else:
                    args = ('moveto', action['fraction']) if 'fraction' in action else ('scroll', action.get('number', 1), action.get('what', 'units'))
                    if isinstance(target, Scrollbar):
                        command = target.cget('command')
                        if not callable(command):
                            raise TclError('Posuvník nemá připojený příkaz')
                        command(*args)
                    else:
                        target.yview(*args)
            else:
                raise TclError('Nepodporovaná testovací akce')
            snapshots.append(snapshot())


class Label(Widget):
    kind = 'label'


class Frame(Widget):
    kind = 'frame'


class Button(Widget):
    kind = 'button'
    def invoke(self):
        if str(self.cget('state')) == 'disabled':
            return ''
        command = self.cget('command')
        if command in ('', None):
            return ''
        if not callable(command):
            raise TclError('Příkaz tlačítka musí být volatelný')
        return command()


class Checkbutton(Button):
    kind = 'checkbutton'
    def __init__(self, master=None, **options):
        options.setdefault('variable', IntVar(value=0))
        options.setdefault('onvalue', 1)
        options.setdefault('offvalue', 0)
        super().__init__(master, **options)
    def selected(self):
        return str(self.options['variable'].get()) == str(self.options['onvalue'])
    def invoke(self):
        if str(self.cget('state')) == 'disabled':
            return ''
        self.options['variable'].set(self.options['offvalue'] if self.selected() else self.options['onvalue'])
        return super().invoke()


class Radiobutton(Button):
    kind = 'radiobutton'
    def __init__(self, master=None, **options):
        options.setdefault('variable', StringVar())
        options.setdefault('value', '')
        super().__init__(master, **options)
    def selected(self):
        return str(self.options['variable'].get()) == str(self.options['value'])
    def invoke(self):
        if str(self.cget('state')) == 'disabled':
            return ''
        self.options['variable'].set(self.options['value'])
        return super().invoke()


class Entry(Widget):
    kind = 'entry'
    def __init__(self, master=None, **options):
        super().__init__(master, **options)
        self.value = ''
    def get(self):
        variable = self.options.get('textvariable')
        return str(variable.get()) if variable is not None else self.value
    def _set(self, value):
        variable = self.options.get('textvariable')
        if variable is not None:
            variable.set(value)
        else:
            self.value = value
    def _index(self, index):
        return len(self.get()) if index == 'end' else max(0, min(int(index), len(self.get())))
    def delete(self, first, last=None):
        text = self.get()
        begin = self._index(first)
        end = self._index(last) if last is not None else begin + 1
        self._set(text[:begin] + text[end:])
    def insert(self, index, text):
        offset = self._index(index)
        self._set(self.get()[:offset] + str(text) + self.get()[offset:])


class VerticalView:
    """Logický svislý posun; nezahrnuje měření písma ani zalamování skutečného Tk."""
    first = 0.0
    def _visible_fraction(self):
        count = len(self.items) if isinstance(self, Listbox) else self.value.count('\n') + 1
        return min(1.0, max(1, int(self.cget('height') or 10)) / max(1, count))
    def _notify_scroll(self):
        self.first = max(0.0, min(self.first, 1.0 - self._visible_fraction()))
        callback = self.cget('yscrollcommand')
        if callable(callback):
            callback(*self.yview())
    def yview(self, *args):
        if args:
            if args[0] == 'moveto' and len(args) == 2:
                self.first = float(args[1])
            elif args[0] == 'scroll' and len(args) == 3 and args[2] in ('units', 'pages'):
                count = max(1, len(self.items) if isinstance(self, Listbox) else self.value.count('\n') + 1)
                amount = 1 / count if args[2] == 'units' else self._visible_fraction()
                self.first += int(args[1]) * amount
            else:
                raise TclError('Nepodporovaný svislý posun')
            self._notify_scroll()
        return (self.first, min(1.0, self.first + self._visible_fraction()))
    def yview_moveto(self, fraction):
        self.yview('moveto', fraction)
    def yview_scroll(self, number, what):
        self.yview('scroll', number, what)


class Listbox(VerticalView, Widget):
    kind = 'listbox'
    def __init__(self, master=None, **options):
        super().__init__(master, **options)
        self.items = []
        self.selection = set()
    def _index(self, index):
        return len(self.items) - 1 if index == 'end' else int(index)
    def size(self):
        return len(self.items)
    def get(self, first, last=None):
        start = self._index(first)
        if last is None:
            return self.items[start] if 0 <= start < len(self.items) else ''
        return tuple(self.items[max(0, start):self._index(last)+1])
    def insert(self, index, *elements):
        offset = len(self.items) if index == 'end' else max(0, min(int(index), len(self.items)))
        self.items[offset:offset] = [str(v) for v in elements]
        self.selection = {i + len(elements) if i >= offset else i for i in self.selection}
        self._notify_scroll()
    def delete(self, first, last=None):
        start = max(0, self._index(first))
        stop = min(len(self.items), self._index(last) + 1 if last is not None else start + 1)
        if stop <= start:
            return
        del self.items[start:stop]
        self.selection = {i if i < start else i - (stop-start) for i in self.selection if i < start or i >= stop}
        self._notify_scroll()
    def curselection(self):
        return tuple(sorted(self.selection))
    def selection_set(self, first, last=None):
        start, stop = self._index(first), self._index(last) if last is not None else self._index(first)
        self.selection.update(range(max(0, start), min(len(self.items)-1, stop)+1))
    select_set = selection_set
    def selection_clear(self, first, last=None):
        start, stop = self._index(first), self._index(last) if last is not None else self._index(first)
        self.selection.difference_update(range(max(0, start), min(len(self.items)-1, stop)+1))
    select_clear = selection_clear
    def see(self, index):
        index = self._index(index)
        if self.items:
            self.yview_moveto(max(0, index) / len(self.items))


class Text(VerticalView, Widget):
    kind = 'text'
    def __init__(self, master=None, **options):
        super().__init__(master, **options)
        self.value = ''
    def _index(self, index):
        index = str(index).replace(' ', '')
        if index == 'end':
            return len(self.value) + 1
        if index in ('end-1c', 'end-1chars'):
            return len(self.value)
        try:
            row, column = map(int, index.split('.'))
            if row < 1 or column < 0:
                raise ValueError
        except ValueError:
            raise TclError('Podporované indexy Text: řádek.sloupec, end a end-1c') from None
        lines = (self.value + '\n').splitlines(keepends=True)
        return min(len(self.value)+1, sum(len(line) for line in lines[:row-1]) + min(column, len(lines[row-1].rstrip('\n')) if row <= len(lines) else 0))
    def get(self, first, last=None):
        start = self._index(first)
        stop = self._index(last) if last is not None else start+1
        return (self.value + '\n')[start:stop]
    def delete(self, first, last=None):
        if self.cget('state') == 'disabled':
            return
        start = min(len(self.value), self._index(first))
        stop = min(len(self.value), self._index(last) if last is not None else start+1)
        if stop > start:
            self.value = self.value[:start] + self.value[stop:]
            self._notify_scroll()
    def insert(self, index, text, *tags):
        if self.cget('state') == 'disabled':
            return
        offset = min(len(self.value), self._index(index))
        self.value = self.value[:offset] + str(text) + self.value[offset:]
        self._notify_scroll()


class Scrollbar(Widget):
    kind = 'scrollbar'
    def __init__(self, master=None, **options):
        options.setdefault('orient', 'vertical')
        super().__init__(master, **options)
        self.range = (0.0, 1.0)
    def set(self, first, last):
        self.range = (float(first), float(last))
    def get(self):
        return self.range


def choose_file(kind, **options):
    if not dialog_answers:
        raise TclError('Pro dialog chybí připravená testovací odpověď')
    answer = dialog_answers.pop(0)
    if answer.get('kind') != kind:
        raise TclError('Program otevřel jiný typ dialogu')
    path = answer.get('path', '')
    dialog_log.append({'kind': kind, 'path': path})
    return path


def shown(widget):
    if not widget.alive or not widget.visible:
        return False
    if widget.master is None:
        return widget.kind == 'root'
    return bool(widget.manager) and shown(widget.master)


def snapshot():
    result = []
    for w in widgets:
        if not w.alive:
            continue
        item = {'id': w.id, 'kind': w.kind, 'parent': w.master.id if w.master else None,
                'manager': w.manager, 'layout': dict(w.layout), 'order': w.order,
                'visible': shown(w), 'text': str(w.cget('text')),
                'focused': w is focused, 'bindings': sorted(w.bindings),
                'columns': {k: dict(v) for k, v in w.columns.items()},
                'rows': {k: dict(v) for k, v in w.rows.items()}, 'state': str(w.cget('state'))}
        if isinstance(w, Tk):
            item.update(title=w.caption, geometry=w.size, minsize=w.minimum, columns={k: dict(v) for k, v in w.columns.items()})
        if isinstance(w, Button):
            item['has_command'] = callable(w.cget('command'))
        if isinstance(w, Entry):
            item['value'] = w.get()
        if isinstance(w, (Checkbutton, Radiobutton)):
            item['selected'] = w.selected()
            variable = w.options['variable']
            item['variable_kind'] = 'int' if isinstance(variable, IntVar) else 'string' if isinstance(variable, StringVar) else 'other'
        if isinstance(w, Listbox):
            item.update(items=list(w.items), selection=list(w.curselection()), yview=list(w.yview()))
        if isinstance(w, Text):
            item.update(value=w.value, yview=list(w.yview()))
        if isinstance(w, Scrollbar):
            item.update(range=list(w.range), orient=str(w.cget('orient')))
        result.append(item)
    return result


mod = types.ModuleType('tkinter')
mod.__path__ = []
ttk = types.ModuleType('tkinter.ttk')
filedialog = types.ModuleType('tkinter.filedialog')
filedialog.askopenfilename = lambda **options: choose_file('open', **options)
filedialog.asksaveasfilename = lambda **options: choose_file('save', **options)
for name, cls in [('Tk', Tk), ('Label', Label), ('Button', Button), ('Entry', Entry), ('Frame', Frame),
                  ('Checkbutton', Checkbutton), ('Radiobutton', Radiobutton),
                  ('Listbox', Listbox), ('Text', Text), ('Scrollbar', Scrollbar),
                  ('StringVar', StringVar), ('IntVar', IntVar), ('TclError', TclError)]:
    setattr(mod, name, cls)
for name in ('Label', 'Button', 'Entry', 'Frame', 'Checkbutton', 'Radiobutton', 'Scrollbar'):
    setattr(ttk, name, getattr(mod, name))
mod.ttk = ttk
mod.filedialog = filedialog
for name in ('END', 'W', 'E', 'N', 'S', 'EW', 'BOTH', 'X', 'Y', 'TOP', 'BOTTOM', 'LEFT', 'RIGHT', 'VERTICAL', 'HORIZONTAL', 'BROWSE', 'SINGLE', 'WORD', 'NORMAL', 'DISABLED'):
    setattr(mod, name, name.lower())
mod.mainloop = lambda: default_root.mainloop() if default_root is not None else None
sys.modules.update({'tkinter': mod, 'tkinter.ttk': ttk, 'tkinter.filedialog': filedialog})
sys.path.insert(0, os.path.dirname(os.path.abspath(student)))
out, err = io.StringIO(), io.StringIO()
error = None
calls = []


def error_info(exc):
    own = [f for f in traceback.extract_tb(exc.__traceback__) if f.filename == student]
    return {'type': type(exc).__name__, 'msg': str(exc), 'line': own[-1].lineno if own else None}


def trace(frame, event, arg):
    global steps
    if event == 'line' and frame.f_code.co_filename == student:
        steps += 1
        if steps > spec.get('max_steps', 100000):
            raise RuntimeError('Program provedl příliš mnoho kroků')
    return trace


try:
    with open(student, encoding='utf-8') as file:
        code = compile(file.read(), student, 'exec')
    sys.settrace(trace)
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        namespace = {'__name__': spec.get('run_name', '__main__'), '__file__': student}
        exec(code, namespace)
        for call in spec.get('calls', []):
            try:
                value = namespace[call['name']](*call.get('args', []))
                calls.append({'value': value, 'error': None})
            except BaseException as exc:
                calls.append({'value': None, 'error': error_info(exc)})
except BaseException as exc:
    error = error_info(exc)
finally:
    sys.settrace(None)
if not snapshots:
    snapshots.append(snapshot())
with open(out_path, 'w', encoding='utf-8') as file:
    json.dump({'snapshots': snapshots, 'mainloops': mainloops, 'error': error, 'calls': calls,
               'dialogs': dialog_log,
               'out': out.getvalue()[:20000], 'err': err.getvalue()[:20000]}, file, ensure_ascii=False)
