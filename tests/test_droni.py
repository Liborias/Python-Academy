"""Hon na dronech: chyby, správné alternativy, návaznost a skutečná smyčka."""
import ast,json,os,re,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from server.checker import run_check
from server.content import lesson_view,solution_view
BASE=ROOT/'courses/pygame-2/lessons'
IDS=['21-droni-hrac-a-svet','22-droni-pronasledovani-a-rozestupy','23-droni-rizene-vlny','24-droni-zakladna-a-zivoty','25-droni-hra-pauza-a-vysledek']
WRONG=[
[('self.pozice += vektor * self.rychlost * dt','self.pozice += vektor * self.rychlost'),
 ('vektor = vektor.normalize()','vektor = vektor'),
 ('self.hranice = pygame.Rect(hranice)','self.hranice = hranice'),
 ('self.hranice.right - 16','self.hranice.right'),
 ('return pygame.Vector2(hrac.pozice)','return hrac.pozice'),
 ('self.data.kill()','pass'),
 ('self.skore += 1','self.skore += 2')],
[('self.kotva = pygame.Vector2(stred)','self.kotva = stred'),
 ('pygame.Vector2(hrac.pozice) - self.kotva','pygame.Vector2(hrac.pozice) - self.pozice'),
 ('smer += odpor * 1.6','smer += odpor * 0'),
 ('krok = min(krok, vzdalenost)','krok = krok'),
 ('dron.rychlost * dt','dron.rychlost'),
 [('puvodni = {d: d.pozice.copy() for d in objekty}','puvodni = {d: d.pozice for d in objekty}'),('nove.append((dron, bod))','dron.pozice.update(bod)\n        nove.append((dron, bod))')],
 ('hranice.right - 14','hranice.right')],
[('random.Random(seed)','random.Random(23)'),
 ('dron.kill()','self.drony.remove(dron)'),
 ('while self.cekaji and self.cas >= self.interval:','if self.cekaji and self.cas >= self.interval:'),
 ('self.cas -= self.interval','self.cas = 0.0'),
 ('>= 150 ** 2','>= 0'),
 ('self.vytvoreno += 1','self.vytvoreno += 2'),
 ('min(90 + 10 * (self.cislo - 1), 140)','90 + 10 * (self.cislo - 1)')],
[('self.energie = max(0, self.energie - dt)','self.energie = self.energie - dt'),
 ('self.energie > 0 and self.energie >= dt','self.energie > 0'),
 ('self.zona.contains(self.hrac.rect)','self.zona.collidepoint(self.hrac.rect.center)'),
 ('self.nezranitelnost = max(0, self.nezranitelnost - dt)','self.nezranitelnost = self.nezranitelnost'),
 ('zasah = any(','zasah = all('),
 ('self.zivoty -= 1','self.zivoty -= 2'),
 ("'uspech' if self.skore >= 6","'uspech' if self.skore >= 5"),
 ('if self.konec:','if False:')],
[('Kolo(self.seed)','Kolo(23)'),
 ('self.zasobnik.vloz(PauzaLetu())','self.zasobnik = ZasobnikRezimu(PauzaLetu())'),
 ('self.zasobnik.aktualni.smer = pygame.Vector2(smer)','self.zasobnik.aktualni.smer = smer'),
 ('if not self.bezi:','if False:'),
 ('self.zasobnik.update(dt)','self.kolo.update(smer, dt) if self.kolo is not None else None'),
 ('self.kolo = novy','self.kolo.drony.empty() if self.kolo is not None else None\n        self.kolo = novy'),
 ("self.zasobnik = ZasobnikRezimu(Vysledek(self.kolo))","self.zasobnik = ZasobnikRezimu(Menu())")]
]
CORRECT=[
[('vektor = vektor.normalize()','vektor.normalize_ip()'),('self.hranice = pygame.Rect(hranice)','self.hranice = pygame.Rect(tuple(hranice))'),('return pygame.Vector2(hrac.pozice)','return hrac.pozice.copy()')],
[('bod += smer.normalize() * krok','smer.normalize_ip()\n            bod += smer * krok'),('objekty = list(drony)','objekty = [*drony]'),('return self.kotva.copy()','return pygame.Vector2(self.kotva)')],
[('self.drony.add(dron)','self.drony.add([dron])'),('self.cislo += 1','self.cislo = self.cislo + 1'),('self.cas -= self.interval','self.cas = self.cas - self.interval')],
[('self.energie = min(self.kapacita, self.energie + dt * self.obnova)','self.energie = min(self.energie + self.obnova * dt, self.kapacita)'),('self.zona = ZONA.copy()','self.zona = pygame.Rect(ZONA)'),('zasah = any(','zasah = any(')],
[('Kolo(self.seed)','Kolo(seed=self.seed)'),('self.zasobnik.odeber()','self.zasobnik.odeber()  # pokračujeme v podkladu'),('self.zasobnik.aktualni.smer = pygame.Vector2(smer)','self.zasobnik.aktualni.smer = pygame.Vector2(*smer)')]
]
# Třetí správná varianta kola mění zápis stejně platné podmínky.
CORRECT[3][2]=('if zasah and not self.chraneno and self.nezranitelnost == 0:','if self.nezranitelnost == 0 and zasah and not self.chraneno:')

class DroniTest(unittest.TestCase):
    def variants(self,index):
        d=BASE/IDS[index];source=(d/'solution.py').read_text()
        for expected,cases in [(False,WRONG[index]),(True,CORRECT[index])]:
            for case in cases:
                changes=[case] if isinstance(case[0],str) else case
                code=source
                for before,after in changes:self.assertIn(before,code);code=code.replace(before,after)
                self.assertNotEqual(code,source)
                with self.subTest(lesson=index+21,expected=expected,changes=changes),tempfile.TemporaryDirectory() as temp:
                    result=run_check(d,code,ROOT/'lib',Path(temp))
                    self.assertNotIn('error',result,result);self.assertEqual(result['ok'],expected,result)

    def test_actors_sources_bounds_time_and_cyclic_data(self):self.variants(0)
    def test_snapshot_steering_zero_distance_guards_and_separation(self):self.variants(1)
    def test_waves_rng_safe_entries_catchup_cleanup_and_fallback(self):self.variants(2)
    def test_round_energy_damage_priority_transitions_and_win(self):self.variants(3)
    def test_game_layers_pause_restart_and_closed_states(self):self.variants(4)

    def test_exact_helpers_scope_and_possible_solutions(self):
        course=json.loads((BASE.parent/'course.json').read_text())
        self.assertEqual(next(m for m in course['modules'] if m['id']=='m05')['lessons'],IDS)
        previous={}
        for i,lid in enumerate(IDS):
            d=BASE/lid;view=lesson_view(ROOT/'courses','pygame-2',lid)
            self.assertEqual((view['kind'],view['run_timeout'],len(view['examples']),len(view['tasks']),len(view['quiz'])),('gui',600,0,0,3))
            self.assertTrue(view['preview_images'])
            self.assertEqual(solution_view(ROOT/'courses','pygame-2',lid)['code'],(d/'solution.py').read_text())
            self.assertEqual((d/'example.py').read_bytes(),(d/'solution.py').read_bytes())
            if i:
                actual={n.name:ast.dump(n) for n in ast.parse((d/'files/predchozi.py').read_text()).body if isinstance(n,(ast.ClassDef,ast.FunctionDef))}
                self.assertEqual(actual,previous)
            previous.update({n.name:ast.dump(n) for n in ast.parse((d/'solution.py').read_text()).body if isinstance(n,(ast.ClassDef,ast.FunctionDef))})
            for name in ['podklady.py','zdroje.py','zasobnik.py','sceny.py','sestava.py','herni_okno.py']:
                self.assertEqual((d/'files'/name).read_bytes(),(BASE/IDS[0]/'files'/name).read_bytes())
        for filename,paths in [('zdroje.py',['16-spolecne-obrazky-fonty-a-zvuky/solution.py','16-spolecne-obrazky-fonty-a-zvuky/tasks/task-2/solution.py']),('zasobnik.py',['20-skladani-hernich-rezimu/solution.py'])]:
            expected={}
            for path in paths:expected.update({n.name:ast.dump(n) for n in ast.parse((BASE/path).read_text()).body if isinstance(n,ast.ClassDef)})
            actual={n.name:ast.dump(n) for n in ast.parse((BASE/IDS[0]/'files'/filename).read_text()).body if isinstance(n,ast.ClassDef)}
            self.assertEqual(actual,expected)

    def test_gui_entrypoint_required(self):
        source=(BASE/IDS[-1]/'solution.py').read_text().split('# Okno vznikne')[0]
        with tempfile.TemporaryDirectory() as temp:
            result=run_check(BASE/IDS[-1],source,ROOT/'lib',Path(temp))
            self.assertNotIn('error',result,result);self.assertFalse(result['ok'],result)

    def test_real_sdl_entrypoints_png_and_standalone_teaching_snippets(self):
        from PIL import Image
        count=0
        for i,lid in enumerate(IDS):
            d=BASE/lid
            with self.subTest(lesson=lid),tempfile.TemporaryDirectory() as temp:
                work=Path(temp);shutil.copytree(d/'files',work,dirs_exist_ok=True)
                before={p.name:p.read_bytes() for p in work.glob('*.py')}
                (work/'main.py').write_bytes((d/'solution.py').read_bytes())
                events={79:[{'type':'QUIT'}]}
                if i==4:events[0]=[{'type':'KEYDOWN','key':'K_SPACE'}]
                if i==2:events[10]=[{'type':'KEYDOWN','key':'K_n'}]
                (work/'spec.json').write_text(json.dumps({'frames':100,'events':events}))
                result=subprocess.run([sys.executable,str(ROOT/'lib/dilna_check/pgrun.py'),'main.py','spec.json','out.json'],cwd=work,capture_output=True,text=True,timeout=15)
                self.assertEqual(result.returncode,0,result.stderr)
                out=json.loads((work/'out.json').read_text())
                self.assertIsNone(out['error']);self.assertTrue(out['ended']);self.assertEqual(out['frames'],80)
                if i==2:self.assertTrue(any(t['text']=='Vlna: 2/3' for t in out['texts']))
                with Image.open(work/'droni.png') as image:image.load();self.assertEqual((image.format,image.size),('PNG',(720,540)))
                for name,content in before.items():self.assertEqual((work/name).read_bytes(),content)
                for text in re.findall(r'\x60\x60\x60python\n(.*?)\x60\x60\x60',(d/'lesson.md').read_text(),re.S):
                    (work/'snippet.py').write_text(text,encoding='utf-8')
                    p=subprocess.run([sys.executable,'-X','utf8','snippet.py'],cwd=work,capture_output=True,text=True,timeout=10)
                    self.assertEqual(p.returncode,0,p.stdout+p.stderr);count+=1
        self.assertEqual(count,5)

    def test_full_mission_reproducible_route_can_win_and_idle_cannot(self):
        d=BASE/IDS[-1]
        script="""import json,math
import pygame
from predchozi import Kolo
def play():
    k=Kolo(23)
    for i in range(610):
        goal=pygame.Vector2(k.data.rect.center)
        def cost(v):
            p=k.hrac.pozice+v*12
            p.x=max(k.hranice.left+16,min(k.hranice.right-16,p.x))
            p.y=max(k.hranice.top+16,min(k.hranice.bottom-16,p.y))
            danger=min(((p-d.pozice).length() for d in k.drony),default=1000)
            return (p-goal).length()+6*max(0,80-danger)**2/80
        choices=[pygame.Vector2(math.cos(j*math.pi/8),math.sin(j*math.pi/8)) for j in range(16)]
        k.update(min(choices,key=cost),.05)
        if k.konec:break
    return [k.duvod,k.skore,k.zivoty,k.vlny.cislo,round(k.cas,6)]
a=play();b=play()
assert a==b,(a,b)
assert a[0]=='uspech' and a[1]>=6 and a[2]>0 and a[3]==3,a
idle=Kolo(23)
for i in range(610):
    idle.update((0,0),.05)
    if idle.konec:break
assert idle.konec and idle.duvod!='uspech' and idle.skore==0
print(json.dumps({'route':a,'idle':[idle.duvod,idle.zivoty,round(idle.cas,6)]}))
"""
        with tempfile.TemporaryDirectory() as temp:
            work=Path(temp);shutil.copytree(d/'files',work,dirs_exist_ok=True);(work/'mission.py').write_text(script)
            p=subprocess.run([sys.executable,'mission.py'],cwd=work,capture_output=True,text=True,timeout=15)
            self.assertEqual(p.returncode,0,p.stdout+p.stderr)

if __name__=='__main__':unittest.main()
