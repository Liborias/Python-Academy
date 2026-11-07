"""Tkinter 5–8: rodiče, události, skupiny voleb a oprava chybných vstupů."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.checker import run_check

BASE = ROOT/'courses/tkinter-api/lessons'
IDS = ['05-ramecky-a-zmena-velikosti','06-enter-a-fokus','07-promenne-a-volby','08-projekt-prevodnik-vzdalenosti']


class TkinterFormsTest(unittest.TestCase):
    def source(self, index):
        return (BASE/IDS[index]/'solution.py').read_text('utf-8')

    def variants(self, index, wrong, correct):
        for expected, variants in [(False,wrong),(True,correct)]:
            for source in variants:
                self.assertNotEqual(source,self.source(index))
                with self.subTest(expected=expected,source=source), tempfile.TemporaryDirectory() as temp:
                    result=run_check(BASE/IDS[index],source,ROOT/'lib',Path(temp))
                    self.assertNotIn('error',result,result)
                    self.assertEqual(result.get('ok'),expected,result)

    def test_frames_parent_layout_and_growth(self):
        s=self.source(0)
        wrong=[s.replace('ttk.Entry(formular)','ttk.Entry(okno)'),
               s.replace('weight=1','weight=0'),s.replace('sticky="ew"','sticky="w"'),
               s.replace('fill="x"','fill="none"'),s.replace('informace.pack(fill="x", padx=16, pady=8)',''),
               s.replace('ttk.Label(informace','ttk.Label(formular'),
               s.replace('formular.pack(fill="x", padx=16, pady=12)','').replace('informace.pack(fill="x", padx=16, pady=8)','informace.pack(fill="x", padx=16, pady=8)\nformular.pack(fill="x", padx=16, pady=12)')]
        correct=[s.replace('fill="x"','fill="both"'),s.replace('formular','horni').replace('informace','dolni'),
                 s.replace('padding=12','padding=8').replace('weight=1','weight=3').replace('sticky="ew"','sticky="we"')]
        self.variants(0,wrong,correct)

    def test_enter_and_button_both_read_fresh_input(self):
        s=self.source(1)
        wrong=[s.replace('jmeno.bind("<Return>", pozdrav)',''),s.replace('jmeno.focus_set()',''),
               s.replace('def pozdrav(udalost=None):','def pozdrav():'),
               s.replace('command=pozdrav)','command=pozdrav())'),
               s.replace('jmeno.get().strip()','jmeno.get()'),
               s.replace('jmeno.get().strip()','"Ema"'),
               s.replace('vysledek.configure(text=f"Ahoj, {text}!")','return f"Ahoj, {text}!"')]
        correct=[s.replace('<Return>','<KeyPress-Return>'),
                 s.replace('jmeno.bind("<Return>", pozdrav)','jmeno.bind("<Return>", lambda event: pozdrav())'),
                 s.replace('vysledek.configure(text=f"Ahoj, {text}!")','vysledek["text"] = f"Ahoj, {text}!"')]
        self.variants(1,wrong,correct)

    def test_check_and_radio_group_all_combinations(self):
        s=self.source(2)
        wrong=[s.replace('text="Kurýr", variable=doprava','text="Kurýr", variable=tk.StringVar(okno, value="kuryr")'),
               s.replace('tk.IntVar(okno, value=0)','tk.IntVar(okno, value=1)'),
               s.replace('tk.StringVar(okno, value="odber")','tk.StringVar(okno, value="kuryr")'),
               s.replace('onvalue=1, offvalue=0','onvalue=1, offvalue=1'),
               s.replace('if krehke.get() == 1:','if False:'),
               s.replace('if doprava.get() == "odber":','if True:'),
               s.replace('command=zobraz)','command=zobraz())'),
               s.replace('vysledek.configure(text=f"Doprava: {nazev}; křehké: {krehkost}.")','ttk.Label(okno,text=f"Doprava: {nazev}; křehké: {krehkost}.").pack()')]
        correct=[s.replace('doprava','volba').replace('krehke','opatrne'),
                 s.replace('"odber"','"osobne"').replace('"kuryr"','"doruceni"'),
                 s.replace('.configure(','.config(')]
        self.variants(2,wrong,correct)

    def test_converter_pure_function_errors_and_gui_recovery(self):
        s=self.source(3)
        wrong=[s.replace('hodnota * 1000','hodnota / 1000'),s.replace('hodnota / 1000','hodnota * 1000'),
               s.replace('or hodnota < 0','or hodnota < -10'),
               s.replace('not math.isfinite(hodnota) or ','').replace('if not math.isfinite(vysledek):','if False:'),
               s.replace('raise ValueError("Neznámý směr převodu.")','return 0'),
               s.replace('return vysledek','return str(vysledek)'),
               s.replace('.replace(",", ".")',''),s.replace('except ValueError:','except TypeError:'),
               s.replace('{cislo:.3f}','{cislo:.2f}'),s.replace('smer.get()','"km-m"'),
               s.replace('if __name__ == "__main__":','if True:'),
               s.replace('vstup.bind("<Return>", preved)','')]
        correct=[s.replace('hlavni','spust_okno'),s.replace('hodnota * 1000','1000 * hodnota'),
                 s.replace('f"{cislo:.3f} {jednotka}"','"{:.3f} {}".format(cislo, jednotka)')]
        self.variants(3,wrong,correct)

    def test_course_has_second_module_and_complete_lesson_files(self):
        course=json.loads((BASE.parent/'course.json').read_text('utf-8'))
        self.assertEqual(course['modules'][1]['lessons'],IDS)
        self.assertEqual(sum(len(m['lessons']) for m in course['modules']),8)
        for lid in IDS:
            d=BASE/lid
            self.assertEqual(json.loads((d/'lesson.json').read_text('utf-8'))['kind'],'gui')
            self.assertEqual(len(json.loads((d/'quiz.json').read_text('utf-8'))),3)


if __name__ == '__main__':
    unittest.main()
