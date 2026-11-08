import sys
from unittest.mock import patch
import tkinter
from dilna_check import check

c = check()
sys.path.insert(0, str(c.student.parent))
with patch.object(tkinter, "Tk", side_effect=RuntimeError("Import nesmí otevřít okno.")):
    ns = c.load()
work = c.student.parent


def named(r, name, index=-1):
    return next((w for w in r.widgets(index=index) if w.get("name") == name), {})


def fill(name, value):
    return {"action": "fill_text" if name == "telo" else "fill", "name": name, "value": value}


def click(text):
    return {"action": "click", "text": text}

if ns:
    for args in [("", "", ""), ("  jan@example.test ", "  Žofie  ", "A\nB\n", " soubor.txt"), ("nedopsaná@", "", "  ")]:
        expected = dict(zip(("prijemce", "predmet", "text", "priloha"), (*args, "") if len(args)==3 else args))
        c.returns(ns, "vytvor_koncept", args, expected)
    for args in [(None,"",""),("",3,""),("","",[]),("","","",False)]:
        c.raises(ns,"vytvor_koncept",args,ValueError,"Všechny čtyři hodnoty musí být texty.")
    ok, first = c.call(ns,"vytvor_koncept",("a","b","c"))
    ok2, second = c.call(ns,"vytvor_koncept",("a","b","c"))
    c.add("Každý koncept je nový slovník",ok and ok2 and isinstance(first,dict) and first is not second,"Neuchovávejte jeden sdílený slovník pro všechny koncepty.")

actions=[fill("prijemce","  jan@example.test "),fill("predmet","  Žofie  "),fill("telo","A\nB\n"),click("Obnovit náhled"),
         fill("prijemce","nedopsaná@"),fill("predmet",""),fill("telo","  "),click("Obnovit náhled"),
         {"action":"fill_text","name":"nahled","value":"Nesmí se přepsat"}]
r=c.tk_run(actions)
if c.tk_no_error(r):
    for index,values,preview in [(4,("  jan@example.test ","  Žofie  ","A\nB\n"),"Komu:   jan@example.test \nPředmět:   Žofie  \n\nA\nB\n"),
                                  (8,("nedopsaná@","","  "),"Komu: nedopsaná@\nPředmět: \n\n  ")]:
        c.add("Čerstvá data bez změny vstupu "+str(index),tuple(named(r,k,index).get('value') for k in ('prijemce','predmet','telo'))==values
              and named(r,'nahled',index).get('value')==preview and named(r,'nahled',index).get('state')=='disabled',
              "Koncept uchovává i neúplný text a mezery. Tělo čtěte do end-1c, ne do end.")
    c.add("Náhled nelze přepsat",named(r,'nahled',8).get('value')==named(r,'nahled',9).get('value'),"Náhled je pouze pro čtení.")
c.done()
