"""Součásti větší hry: chybné/správné varianty, pixely, skutečný mixer a živý režim."""
import ast
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from server.checker import run_check
from server.content import lesson_view,solution_view
BASE=ROOT/'courses/pygame-2/lessons'
IDS=['16-spolecne-obrazky-fonty-a-zvuky','17-animace-podle-casu','18-masky-a-presnost-kolize','19-svet-a-kamera','20-skladani-hernich-rezimu']

# Každý z 25 úkolů má dva chybné zápisy a jiný správný postup.
CASES=[[
([('return self._obrazy[jmeno].copy()','return self._obrazy[jmeno]'),('self.nacti(jmeno).copy()','self.nacti(jmeno)')],('return self._obrazy[jmeno].copy()','return pygame.Surface.copy(self._obrazy[jmeno])')),
([('if velikost not in self._fonty:','if True:'),('return self._fonty[velikost]','return self.vytvor(velikost)')],('self._fonty[velikost] = self.vytvor(velikost)','font = self.vytvor(velikost)\n            self._fonty[velikost] = font')),
([('self.original = original.copy()','self.original = original'),('klic = tuple(rozmer)','klic = (rozmer[0], rozmer[0])')],('klic = tuple(rozmer)','klic = (rozmer[0], rozmer[1])')),
([('except pygame.error:','except Exception:'),('return zvuk.play() is not None','zvuk.play()\n            return True')],('return zvuk.play() is not None','kanal = zvuk.play()\n            return kanal is not None')),
([('if jmeno not in vysledek:','if True:'),('for jmeno in jmena:','for jmeno in sorted(set(jmena)):')],('for jmeno in jmena:','for jmeno in dict.fromkeys(jmena):')),
],[
([('kroky = math.floor(celkem / self.trvani + 1e-9)','kroky = min(1, math.floor(celkem / self.trvani + 1e-9))'),('self.zbytek = max(0, celkem - kroky * self.trvani)','self.zbytek = 0.0')],('math.floor(celkem / self.trvani + 1e-9)','int(celkem / self.trvani + 1e-9)')),
([('self.hotovo = kroky >= len(self.snimky)','self.hotovo = kroky >= len(self.snimky) - 1'),('self.index = min(kroky, len(self.snimky) - 1)','self.index = kroky % len(self.snimky)')],('min(kroky, len(self.snimky) - 1)','min(len(self.snimky) - 1, kroky)')),
([('pas.subsurface((x, 0, sirka, pas.get_height())).copy()','pas.subsurface((x, 0, sirka, pas.get_height()))'),('pas.subsurface((x, 0, sirka, pas.get_height()))','pas.subsurface((0, 0, sirka, pas.get_height()))')],('pas.subsurface((x, 0, sirka, pas.get_height())).copy()','pygame.Surface.subsurface(pas, (x, 0, sirka, pas.get_height())).copy()')),
([('stred = self.rect.center','stred = self.rect.topleft'),('self.rect = self.image.get_rect(center=stred)\n\n#','self.rect = self.rect\n\n#')],('self.rect = self.image.get_rect(center=stred)','self.rect = pygame.Rect((0, 0), self.image.get_size())\n        self.rect.center = stred')),
([('if jmeno == self.stav:','if False:'),('self.animace[self.stav].update(dt)','[a.update(dt) for a in self.animace.values()]')],('self.animace = dict(animace)','self.animace = {jmeno: a for jmeno, a in animace.items()}')),
],[
([('self.image = obraz.copy()','self.image = obraz'),('pygame.mask.from_surface(self.image, prah)','pygame.mask.from_surface(self.image, 127)')],('pygame.mask.from_surface(self.image, prah)','pygame.mask.from_surface(obraz, prah)')),
([('b.rect.x - a.rect.x, b.rect.y - a.rect.y','a.rect.x - b.rect.x, a.rect.y - b.rect.y'),('return a.mask.overlap(b.mask, posun) is not None','return a.rect.colliderect(b.rect)')],('return a.mask.overlap(b.mask, posun) is not None','return bool(a.mask.overlap(b.mask, posun))')),
([('sprite.mask = pygame.mask.from_surface(sprite.image, prah)','sprite.mask = sprite.mask'),('stred = sprite.rect.center','stred = sprite.rect.topleft')],('sprite.image = novy_obraz.copy()','sprite.image = pygame.Surface.copy(novy_obraz)')),
([('a is not b and zasah_maskou(a, b)','zasah_maskou(a, b)'),('vysledek.append((a, b))','vysledek.append((a, b))\n                b.kill()')],('vysledek.append((a, b))','vysledek += [(a, b)]')),
([("'maska': zasah_maskou(a, b)","'maska': a.rect.colliderect(b.rect)"),('<= (a.radius + b.radius) ** 2','< (a.radius + b.radius) ** 2')],('rozdil.length_squared() <= (a.radius + b.radius) ** 2','rozdil.length() <= a.radius + b.radius')),
],[
([('self.vyhled = pygame.Rect(vyhled)','self.vyhled = vyhled'),('self.posun.x = max(self.svet.left, min(max_x, x))','self.posun.x = x')],('self.vyhled = pygame.Rect(vyhled)','self.vyhled = pygame.Rect(tuple(vyhled))')),
([(' - kamera.posun + kamera.vyhled.topleft',' - kamera.posun'),('return pygame.Vector2(bod) - kamera.posun + kamera.vyhled.topleft','bod -= kamera.posun\n    return bod + kamera.vyhled.topleft')],('pygame.Vector2(bod) - kamera.posun + kamera.vyhled.topleft','pygame.Vector2(bod) + kamera.vyhled.topleft - kamera.posun')),
([(' + kamera.posun - kamera.vyhled.topleft',' - kamera.posun - kamera.vyhled.topleft'),('return pygame.Vector2(bod) + kamera.posun - kamera.vyhled.topleft','return tuple(pygame.Vector2(bod) + kamera.posun - kamera.vyhled.topleft)')],('pygame.Vector2(bod) + kamera.posun','pygame.Vector2(kamera.posun) + bod')),
([('o.rect.right > x','o.rect.right >= x'),('x, y = kamera.posun','x, y = (round(v) for v in kamera.posun)')],('w, h = kamera.vyhled.size','w = kamera.vyhled.width\n    h = kamera.vyhled.height')),
([('puvodni.clip(kamera.vyhled)','kamera.vyhled'),('finally:\n        plocha.set_clip(puvodni)','finally:\n        pass')],('puvodni.clip(kamera.vyhled)','kamera.vyhled.clip(puvodni)')),
],[
([('self.aktualni.update(dt)','[r.update(dt) for r in self.rezimy]'),('for rezim in self.rezimy:','for rezim in reversed(self.rezimy):')],('self.rezimy[-1]','self.rezimy[len(self.rezimy) - 1]')),
([('pygame.KEYDOWN and udalost.key','pygame.KEYUP and udalost.key'),('(10, 18, 30, 170)','(10, 18, 30, 255)')],('def update(self, dt):\n        pass','def update(self, dt):\n        return None')),
([('self.rect = pygame.Rect(rect)','self.rect = rect'),('udalost.button == 1','udalost.button == 3')],('self.rect = pygame.Rect(rect)','self.rect = pygame.Rect(tuple(rect))')),
([('self.tlacitka = list(tlacitka)','self.tlacitka = tlacitka'),('reversed(self.tlacitka)','self.tlacitka')],('self.tlacitka = list(tlacitka)','self.tlacitka = [*tlacitka]')),
([('self.zasobnik.vloz(self.vytvor(akce))','self.zasobnik = ZasobnikRezimu(self.vytvor(akce))'),('if self.bezi:\n            self.zasobnik.update(dt)','if True:\n            self.zasobnik.update(dt)')],("akce in ('hra', 'nabidka')","akce in {'nabidka', 'hra'}")),
]]


class SoucastiTest(unittest.TestCase):
    def directory(self,stage,task):
        d=BASE/IDS[stage]
        return d if task==0 else d/'tasks'/f'task-{task+1}'

    def variants(self,stage):
        for task,(wrong,correct) in enumerate(CASES[stage]):
            d=self.directory(stage,task);source=(d/'solution.py').read_text()
            for expected,change in [(False,c) for c in wrong]+[(True,correct)]:
                before,after=change;self.assertIn(before,source)
                code=source.replace(before,after)
                with self.subTest(stage=stage,task=task,expected=expected,change=change),tempfile.TemporaryDirectory() as temp:
                    result=run_check(d,code,ROOT/'lib',Path(temp))
                    self.assertNotIn('error',result,result);self.assertEqual(result['ok'],expected,result)

    def test_resources_cache_copies_keys_fonts_and_sound_fallback(self):self.variants(0)
    def test_animation_time_catchup_finish_crop_and_state(self):self.variants(1)
    def test_masks_alpha_offsets_refresh_identity_and_rules(self):self.variants(2)
    def test_camera_coordinates_visibility_and_clip_restoration(self):self.variants(3)
    def test_modes_layers_delegation_menu_and_controller(self):self.variants(4)

    def test_scope_solutions_and_exact_prepared_dependencies(self):
        definitions={}
        for stage in range(5):
            for task in range(5):
                tree=ast.parse((self.directory(stage,task)/'solution.py').read_text())
                definitions.update({n.name:ast.dump(n) for n in tree.body if isinstance(n,(ast.ClassDef,ast.FunctionDef))})
        course=json.loads((BASE.parent/'course.json').read_text())
        self.assertEqual(next(m for m in course['modules'] if m['id']=='m04')['lessons'],IDS)
        for stage,lid in enumerate(IDS):
            view=lesson_view(ROOT/'courses','pygame-2',lid)
            self.assertEqual((view['kind'],view['run_timeout'],len(view['examples']),len(view['tasks']),len(view['quiz'])),('console',20,2,4,3))
            self.assertTrue(view['preview_images'])
            for task in range(5):
                d=self.directory(stage,task)
                self.assertEqual(solution_view(ROOT/'courses','pygame-2',lid,f'task-{task+1}')['code'],(d/'solution.py').read_text())
                for helper in (d/'files').glob('*.py'):
                    if helper.name in ['zdroje.py','animator.py','masky.py','kamera.py','ovladace.py','rezimy.py']:
                        for n in ast.parse(helper.read_text()).body:
                            if isinstance(n,(ast.ClassDef,ast.FunctionDef)):self.assertEqual(ast.dump(n),definitions[n.name],str(helper))

    def test_standalone_png_examples_solutions_and_teaching_snippets(self):
        from PIL import Image
        count=0
        for stage,lid in enumerate(IDS):
            root=BASE/lid
            programs=[(self.directory(stage,t),(self.directory(stage,t)/'solution.py').read_text(),True) for t in range(5)]
            programs += [(root,e['code'],True) for e in json.loads((root/'examples.json').read_text())]
            programs += [(root,s,False) for s in re.findall(r'```python\n(.*?)```',(root/'lesson.md').read_text(),re.S)]
            for directory,code,png in programs:
                with self.subTest(lesson=lid,source=code[:80]),tempfile.TemporaryDirectory() as temp:
                    work=Path(temp);shutil.copytree(directory/'files',work,dirs_exist_ok=True)
                    before={p.name:p.read_bytes() for p in work.glob('*.py')}
                    (work/'main.py').write_text(code,encoding='utf-8')
                    p=subprocess.run([sys.executable,'-X','utf8','main.py'],cwd=work,capture_output=True,text=True,timeout=10,env=dict(os.environ,SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy'))
                    self.assertEqual(p.returncode,0,p.stdout+p.stderr)
                    if png:
                        with Image.open(work/'soucasti.png') as img:img.load();self.assertEqual((img.format,img.size),('PNG',(720,420)))
                    for name,content in before.items():self.assertEqual((work/name).read_bytes(),content)
                    count+=1
        self.assertEqual(count,40)

    def test_real_dummy_mixer_wav_decode_and_opt_in_audio_probe(self):
        d=self.directory(0,3)
        with tempfile.TemporaryDirectory() as temp:
            work=Path(temp);shutil.copytree(d/'files',work,dirs_exist_ok=True)
            (work/'reseni.py').write_bytes((d/'solution.py').read_bytes())
            (work/'audio_test.py').write_text("import pygame, wave\nfrom reseni import Zvuky\nfrom podklady import priprav_media\np=priprav_media()/'ton.wav'\nwith wave.open(str(p),'rb') as f:assert (f.getnchannels(),f.getsampwidth(),f.getframerate(),f.getnframes())==(1,2,22050,4410)\npygame.mixer.init()\ntry:\n s=pygame.mixer.Sound(str(p));assert abs(s.get_length()-.2)<.01\n bank=Zvuky(lambda name:s);assert bank.prehraj('ton',.15) is True\n assert pygame.mixer.get_busy()\nfinally:pygame.mixer.quit()\n",encoding='utf-8')
            env=dict(os.environ,SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy')
            p=subprocess.run([sys.executable,'audio_test.py'],cwd=work,env=env,capture_output=True,text=True,timeout=10)
            self.assertEqual(p.returncode,0,p.stdout+p.stderr)
            for args in [[],['--play']]:
                p=subprocess.run([sys.executable,'prehraj_ton.py',*args],cwd=work,env=env,capture_output=True,text=True,timeout=8)
                self.assertEqual(p.returncode,0,p.stdout+p.stderr)
                self.assertIn('přehr' if args else '--play',p.stdout.lower())

    def test_optional_live_modes_real_sdl_events_and_png(self):
        d=self.directory(4,4)
        with tempfile.TemporaryDirectory() as temp:
            work=Path(temp);shutil.copytree(d/'files',work,dirs_exist_ok=True)
            (work/'reseni.py').write_bytes((d/'solution.py').read_bytes())
            events={0:[{'type':'MOUSEBUTTONDOWN','button':1,'pos':[300,150]}],2:[{'type':'KEYDOWN','key':'K_p'}],4:[{'type':'KEYDOWN','key':'K_p'}],6:[{'type':'KEYDOWN','key':'K_m'}],8:[{'type':'QUIT'}]}
            (work/'spec.json').write_text(json.dumps({'frames':20,'events':events}))
            p=subprocess.run([sys.executable,str(ROOT/'lib/dilna_check/pgrun.py'),'ziva_dilna.py','spec.json','out.json'],cwd=work,capture_output=True,text=True,timeout=15)
            self.assertEqual(p.returncode,0,p.stderr);result=json.loads((work/'out.json').read_text())
            self.assertIsNone(result['error']);self.assertTrue(result['ended']);self.assertEqual((result['frames'],result['size']),(9,[720,420]))
            self.assertTrue(any(t['text']=='PAUZA' for t in result['texts']))
            self.assertTrue((work/'rezimy-zive.png').read_bytes().startswith(b'\x89PNG'))


if __name__=='__main__':unittest.main()
