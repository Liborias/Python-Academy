"""Tkinter 9–12: výběr mezi duplicitami, text, JSON a zachování práce při chybě."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from server.checker import run_check

BASE=ROOT/'courses/tkinter-api/lessons'
IDS=['09-seznam-a-vyber','10-text-a-posuvnik','11-json-a-dialogy','12-projekt-ukolnicek']


class TkinterFilesTest(unittest.TestCase):
    def source(self,index):
        return (BASE/IDS[index]/'solution.py').read_text('utf-8')
    def variants(self,index,wrong,correct):
        for expected,variants in [(False,wrong),(True,correct)]:
            for code in variants:
                self.assertNotEqual(code,self.source(index))
                with self.subTest(expected=expected,code=code),tempfile.TemporaryDirectory() as temp:
                    result=run_check(BASE/IDS[index],code,ROOT/'lib',Path(temp))
                    self.assertNotIn('error',result,result)
                    self.assertEqual(result.get('ok'),expected,result)

    def test_listbox_model_and_selected_duplicate(self):
        s=self.source(0)
        wrong=[s.replace('ukoly.pop(vyber[0])','ukoly.pop(0)'),
               s.replace('if not vyber:','if False:'),s.replace('if not text:','if False:'),
               s.replace('ukoly.append(text)','seznam.insert(tk.END, text)'),
               s.replace('text = ukoly.pop(vyber[0])','text = ukoly[vyber[0]]'),
               s.replace('vstup.delete(0, tk.END)',''),
               s.replace('text = ukoly.pop(vyber[0])','text = ukoly[vyber[0]]\n    ukoly.remove(text)')]
        correct=[s.replace('ukoly.append(text)','ukoly.insert(len(ukoly), text)'),
                 s.replace('text = ukoly.pop(vyber[0])','text = ukoly[vyber[0]]\n    del ukoly[vyber[0]]'),
                 s.replace('zprava','stavovy_text').replace('vstup','pole')]
        self.variants(0,wrong,correct)

    def test_text_counts_and_two_way_scroll(self):
        s=self.source(1)
        wrong=[s.replace('command=text.yview','command=None'),s.replace('text.configure(yscrollcommand=posuvnik.set)',''),
               s.replace('"end-1c"','"end"'),s.replace('obsah = text.get("1.0", "end-1c")','obsah = text.get("1.0", "end-1c").strip()'),
               s.replace('obsah.count("\\n") + 1','len(obsah.splitlines())'),s.replace('pocet_radku = 0','pocet_radku = 1'),
               s.replace('def spocitej():\n    obsah = text.get("1.0", "end-1c")','obsah = text.get("1.0", "end-1c")\n\ndef spocitej():'),
               s.replace('    zprava.configure(text=f"Znaků:', '    text.delete("1.0", "end")\n    zprava.configure(text=f"Znaků:')]
        correct=[s.replace('obsah.count("\\n") + 1','len(obsah.split("\\n"))'),s.replace('posuvnik.set','lambda a, b: posuvnik.set(a, b)'),
                 s.replace(', orient="vertical"',''),
                 s.replace('command=text.yview','command=None').replace('text.configure(yscrollcommand=posuvnik.set)','posuvnik.configure(command=text.yview)\ntext.configure(yscrollcommand=posuvnik.set)')]
        self.variants(1,wrong,correct)

    def test_note_json_utf8_validation_cancel_and_recovery(self):
        s=self.source(2)
        wrong=[s.replace('ensure_ascii=False','ensure_ascii=True'),s.replace('encoding="utf-8"','encoding="ascii"'),
               s.replace('return data["text"]','return data'),s.replace('if not isinstance(data, dict) or not isinstance(data.get("text"), str):','if False:'),
               s.replace('{"text": text}','{"text": "Pevná poznámka"}'),s.replace('"end-1c"','"end"'),
               s.replace('            novy_text = nacti_poznamku(cesta)','            text.delete("1.0", "end")\n            novy_text = nacti_poznamku(cesta)'),
               s.replace('if not cesta:','if False:')]
        correct=[s.replace('indent=2','indent=4'),
                 s.replace('json.dump({"text": text}, soubor, ensure_ascii=False, indent=2)','soubor.write(json.dumps({"text": text}, ensure_ascii=False, indent=2))'),
                 s.replace('not isinstance(data.get("text"), str)','("text" not in data or not isinstance(data["text"], str))')]
        self.variants(2,wrong,correct)

    def test_task_project_model_validation_and_file_roundtrip(self):
        s=self.source(3)
        wrong=[s.replace('ukoly.append({"nazev": nazev, "hotovo": False})','pass'),
               s.replace('ukoly[index]["hotovo"] = True','ukoly[index]["hotovo"] = not ukoly[index]["hotovo"]'),
               s.replace('ukoly[index]["hotovo"] = True','ukoly[0]["hotovo"] = True'),
               s.replace('ukoly.pop(vyber[0])','ukoly.pop(0)'),s.replace('ukoly[:] = nactene','ukoly.extend(nactene)'),
               s.replace('ukoly[:] = nactene','ukoly = nactene'),
               s.replace('            nactene = nacti_ukoly(cesta)','            ukoly.clear()\n            nactene = nacti_ukoly(cesta)'),
               s.replace('isinstance(zaznam.get("hotovo"), bool)','isinstance(zaznam.get("hotovo"), int)'),
               s.replace('json.dump(ukoly,','json.dump([u["nazev"] for u in ukoly],'),
               s.replace('detail.configure(state="disabled")','detail.configure(state="normal")')]
        correct=[s.replace('ukoly[:] = nactene','ukoly.clear()\n        ukoly.extend(nactene)'),
                 s.replace('ukoly[index]["hotovo"] = True','ukoly[index].update(hotovo=True)'),
                 s.replace('hlavni','spust_ukolnicek')]
        self.variants(3,wrong,correct)

    def test_metadata_third_module_and_quizzes(self):
        course=json.loads((BASE.parent/'course.json').read_text('utf-8'))
        self.assertEqual(course['modules'][2]['lessons'],IDS)
        self.assertGreaterEqual(sum(len(m['lessons']) for m in course['modules']),12)
        for lid in IDS:
            d=BASE/lid
            self.assertEqual(json.loads((d/'lesson.json').read_text('utf-8'))['kind'],'gui')
            self.assertEqual(len(json.loads((d/'quiz.json').read_text('utf-8'))),3)


if __name__=='__main__':
    unittest.main()
