"""Pygame 2, součásti 16–20: skutečné pixely, čas a předávání řízení."""
import math
import os
from pathlib import Path
import struct
from types import SimpleNamespace

os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import pygame

NAMES=[['BankaObrazu','BankaFontu','BankaVelikosti','Zvuky','priprav_obrazy'],
       ['Animace','AnimaceJednou','vyrez_snimky','AnimovanySprite','StavoveAnimace'],
       ['MaskovySprite','zasah_maskou','obnov_masku','dvojice_masek','porovnej_kolize'],
       ['Kamera','na_obrazovku','do_sveta','viditelne','vykresli_svet'],
       ['ZasobnikRezimu','Pauza','Tlacitko','Nabidka','RidicScen']]


def require(ok, message):
    if not ok:raise AssertionError(message)


def close(a,b):
    return len(a)==len(b) and all(math.isclose(x,y,abs_tol=1e-8,rel_tol=1e-9) for x,y in zip(a,b))


def pixels(surface):return pygame.image.tobytes(surface,'RGBA')


def image(size=(7,5), color=(80,180,255,255)):
    result=pygame.Surface(size,pygame.SRCALPHA);result.fill(color)
    return result


def frames():return [image(size,(20+i*50,60,150,255)) for i,size in enumerate([(5,8),(9,4),(3,11)])]


def resource(ns, task):
    target=ns[NAMES[0][task]]
    if task==0:
        source=image();saved=pixels(source);calls=[]
        def load(name):
            calls.append(name)
            if name=='chyba' and calls.count(name)==1:raise pygame.error('zkouška')
            return source
        bank=target(load)
        a,b=bank.obraz('hrac'),bank.obraz('hrac')
        require(calls==['hrac'] and a is not b and a is not source and pixels(a)==saved, 'Stejný zdroj načtěte jednou, každému požadavku vraťte vlastní nezměněnou kopii.')
        a.fill((1,2,3));source.fill((4,5,6))
        require(pixels(b)==saved and pixels(bank.obraz('hrac'))==saved, 'Cache musí být nezávislá i na obrázku vráceném načítací funkcí.')
        bank.obraz('stit');target(load).obraz('hrac')
        require(calls==['hrac','stit','hrac'], 'Různá jména i různé banky mají vlastní načtení.')
        try:bank.obraz('chyba')
        except pygame.error:pass
        else:require(False,'Chybu načtení neukrývejte jako obrázek.')
        require(isinstance(bank.obraz('chyba'),pygame.Surface) and calls.count('chyba')==2, 'Neúspěšné načtení se nesmí uložit do cache.')
    elif task==1:
        pygame.font.init();calls=[]
        def make(size):calls.append(size);return pygame.font.Font(None,size)
        bank=target(make);a=bank.font(21);b=bank.font(21);c=bank.font(38)
        require(a is b and a is not c and calls==[21,38] and a.render('A',True,(255,255,255)).get_height()>0, 'Font stejné velikosti sdílejte, jiné velikosti vytvářejte odděleně.')
        require(target(make).font(21) is not a and calls==[21,38,21], 'Cache fontů patří instanci.')
    elif task==2:
        original=image();saved=pixels(original);calls=[]
        def scale(source,size):calls.append(size);return pygame.transform.scale(source,size)
        bank=target(original,scale);original.fill((1,2,3))
        a=bank.obraz([10,8]);b=bank.obraz((10,8));c=bank.obraz((3,11))
        require(calls==[(10,8),(3,11)] and a.get_size()==(10,8) and c.get_size()==(3,11), 'Klíčem jsou oba rozměry; seznam a tuple stejné velikosti znamenají tentýž požadavek.')
        require(a.get_at((1,1))[:3]==(80,180,255) and a is not b, 'Banka kopíruje originál při vzniku a vrací vlastní kopie.')
        a.fill((2,3,4));require(b.get_at((1,1))[:3]==(80,180,255), 'Vrácené rozměrové kopie se nesmějí ovlivnit.')
    elif task==3:
        calls=[]
        class Sound:
            def __init__(self):self.volumes=[];self.plays=0;self.busy=False;self.fail=False
            def set_volume(self,v):self.volumes.append(v)
            def play(self):
                self.plays+=1
                if self.fail:raise pygame.error('kanál')
                return None if self.busy else self
        sound=Sound()
        def make(name):
            calls.append(name)
            if name=='vadny' and calls.count(name)==1:raise pygame.error('soubor')
            if name=='program':raise ValueError('programová chyba')
            return sound
        bank=target(make,False)
        require(bank.prehraj('ton') is False and not calls, 'Vypnutý zvuk nesmí ani vytvářet zvukový objekt.')
        bank.povoleno=True
        require(bank.prehraj('ton',2) is True and bank.prehraj('ton',-1) is True and calls==['ton'] and sound.volumes==[1,0], 'Použijte cache a hlasitost omezte na 0..1.')
        sound.busy=True;require(bank.prehraj('ton') is False,'Žádný volný kanál znamená False, ne přijaté přehrání.')
        sound.busy=False;sound.fail=True
        require(bank.prehraj('ton') is False,'Pygame.error při přehrávání nesmí shodit celou hru.')
        sound.fail=False;require(bank.prehraj('ton') is True and calls==['ton'],'Neúspěšné přehrání nezahazuje už načtený zvuk.')
        require(bank.prehraj('vadny') is False and bank.prehraj('vadny') is True and calls.count('vadny')==2,'Vadné načtení se při dalším pokusu zkusí znovu.')
        try:bank.prehraj('program')
        except ValueError:pass
        else:require(False,'Zachytávejte pygame.error, ne všechny programové chyby.')
    else:
        calls=[]
        class Bank:
            def obraz(self,name):calls.append(name);return image()
        names=['b','a','b','c','a'];before=names.copy()
        result=target(names,Bank())
        require(list(result)==['b','a','c'] and calls==['b','a','c'] and names==before,'Sada zachová první pořadí, pro každé jméno zavolá banku jednou a nemění vstup.')
        require(all(isinstance(o,pygame.Surface) for o in result.values()) and target([],Bank())=={},'Vrátí nový slovník obrázků, prázdný vstup je platný.')
    return True


def animation(ns,task):
    target=ns[NAMES[1][task]]
    if task in (0,1):
        source=frames();saved=[pixels(s) for s in source];obj=target(source,.1)
        require(len(obj.snimky)==3 and all(a is not b and pixels(a)==pixels(b) for a,b in zip(obj.snimky,source)), 'Animace potřebuje vlastní snímky a stejnou první fázi.')
        source[0].fill((1,2,3));require(pixels(obj.snimky[0])==saved[0],'Změna zdroje nesmí změnit animaci.')
        require(obj.index==0 and obj.obraz() is obj.snimky[0], 'Obraz vrací právě uložený aktivní snímek.')
        if task==0:
            total=0
            for dt in [0,.05,.05,.25,1.025,.025]:
                total+=dt;obj.update(dt)
                steps=math.floor(total/.1+1e-8)
                require(obj.index==steps%3 and math.isclose(obj.zbytek,max(0,total-steps*.1),abs_tol=1e-8), 'Počítejte všechny celé snímky, zachovejte zbytek a oběhněte smyčku.')
            obj.restart();require(obj.index==0 and obj.zbytek==0, 'Restart obnoví index i zbytek času.')
        else:
            obj.update(.2);require(obj.index==2 and obj.hotovo is False,'Poslední snímek musí nejprve trvat celou svoji dobu.')
            obj.update(.1);require(obj.hotovo is True and obj.index==2,'Jednorázová animace končí až po posledním intervalu.')
            before=obj.index,obj.cas;obj.update(50)
            require((obj.index,obj.cas)==before and obj.obraz() is obj.snimky[2],'Dokončená animace se už neposouvá ani neobíhá.')
            one=target([image()],.25);one.update(.125);require(not one.hotovo,'I jeden snímek má nenulové trvání.')
            one.update(.125);require(one.hotovo,'Jednosnímková animace skončí po svém intervalu.')
        for seq,duration in [([],1),(frames(),0),(frames(),-1)]:
            try:target(seq,duration)
            except ValueError:pass
            else:require(False,'Prázdné snímky nebo nekladné trvání odmítněte ValueError.')
    elif task==2:
        strip=image((12,5),(0,0,0,0))
        for x in range(12):
            for y in range(5):strip.set_at((x,y),(x*19,y*41,80,100+x*10))
        before=pixels(strip);result=target(strip,4)
        require(len(result)==3 and all(s.get_size()==(4,5) for s in result),'Rozdělte celý vodorovný pás na stejně široké výřezy.')
        for i,s in enumerate(result):
            require(all(s.get_at((x,y))==strip.get_at((i*4+x,y)) for x in range(4) for y in range(5)),'Výřezy mají původní pixely včetně alfa kanálu ve správném pořadí.')
        result[0].fill((1,2,3));require(pixels(strip)==before,'Subsurface bez copy sdílí paměť s původním pásem.')
        for width in [0,-1,5]:
            try:target(strip,width)
            except ValueError:pass
            else:require(False,'Neplatnou šířku nebo neúplný poslední snímek odmítněte.')
    elif task==3:
        obj=target(frames(),(80,90));require(isinstance(obj,pygame.sprite.Sprite),'Animovaný objekt musí být skutečný Sprite.')
        obj.rect.move_ip(17,-12);obj.update(.125)
        require(obj.rect.center==(97,78) and obj.image.get_size()==obj.rect.size and obj.animace.index==1 and obj.image is obj.animace.obraz(),'Změna obrázku zachová aktuální střed a aktualizuje rozměr rect.')
        group=pygame.sprite.Group(obj);group.update(.25);require(obj.animace.index==0,'Sprite musí fungovat také přes Group.update.')
    else:
        class Probe:
            def __init__(self):self.time=0;self.resets=0;self.surface=image()
            def update(self,dt):self.time+=dt
            def restart(self):self.time=0;self.resets+=1
            def obraz(self):return self.surface
        a,b=Probe(),Probe();mapping={'klid':a,'beh':b};obj=target(mapping,'klid');mapping['jiny']=Probe()
        obj.update(.3);require(a.time==.3 and b.time==0 and obj.obraz() is a.surface,'Posouvá se pouze aktivní složka, obraz pochází od ní.')
        require(obj.prepni('klid') is False and a.time==.3,'Opakovaná volba stavu nerestartuje jeho fázi.')
        b.time=8;require(obj.prepni('beh') is True and b.time==0 and b.resets==1,'Změna stavu restartuje nově zvolenou animaci.')
        obj.update(.2);require(b.time==.2 and a.time==.3,'Neaktivní animace zůstává stejná.')
        for name in ['neni','jiny']:
            try:obj.prepni(name)
            except KeyError:pass
            else:require(False,'Mapa se kopíruje; neznámý stav odmítne KeyError před změnou.')
        require(obj.stav=='beh','Neúspěšné přepnutí nesmí změnit aktivní stav.')
    return True


class Body(pygame.sprite.Sprite):
    def __init__(self, surface, point, radius=4):
        super().__init__();self.image=surface.copy();self.rect=self.image.get_rect(topleft=point)
        self.mask=pygame.mask.from_surface(self.image);self.radius=radius


def occupied(obj):
    return {(obj.rect.x+x,obj.rect.y+y) for x in range(obj.mask.get_size()[0]) for y in range(obj.mask.get_size()[1]) if obj.mask.get_at((x,y))}


def mask_matches(mask,surface,threshold):
    if mask.get_size()!=surface.get_size():return False
    key=surface.get_colorkey()
    return all(bool(mask.get_at((x,y))) == (surface.get_at((x,y))[:3]!=key[:3] if key is not None else surface.get_at((x,y)).a>threshold) for x in range(surface.get_width()) for y in range(surface.get_height()))


def collision(ns,task):
    target=ns[NAMES[2][task]]
    surface=image((8,6),(0,0,0,0));surface.set_at((0,0),(80,180,255,255));surface.set_at((3,2),(80,180,255,100));surface.set_at((7,5),(80,180,255,200))
    if task==0:
        before=pixels(surface)
        for threshold in [50,100,127,200,220]:
            a,b=target(surface,(-10,20),threshold),target(surface,(-10,20),threshold)
            require(isinstance(a,pygame.sprite.Sprite) and a.image is not surface and a.image is not b.image and a.rect.topleft==(-10,20),'Maskový sprite vlastní kopii obrazu a rect s levým horním rohem.')
            require(mask_matches(a.mask,surface,threshold),'Maska musí přesně odpovídat alfa prahu obrazu.')
            a.image.fill((1,2,3));require(pixels(surface)==before and pixels(b.image)==before,'Instance ani zdroj nesmějí sdílet měnitelné pixely.')
        keyed=pygame.Surface((6,4));keyed.fill((255,0,255));keyed.set_at((1,2),(80,180,255));keyed.set_colorkey((255,0,255))
        obj=target(keyed,(0,0));require(mask_matches(obj.mask,keyed,127),'Respektujte také barevný klíč RGB obrázku.')
    elif task in (1,4):
        for offset in [(0,0),(7,5),(-7,-5),(8,0),(10,0),(2,2),(-50,20)]:
            second=image((8,6),(0,0,0,0));second.set_at((0,0),(90,220,175,255))
            a,b=Body(surface,(-12,14),4),Body(second,(-12+offset[0],14+offset[1]),6)
            before=tuple(a.rect),tuple(b.rect),pixels(a.image),pixels(b.image)
            expected=bool(occupied(a)&occupied(b))
            result=target(a,b)
            if task==1:require(result is expected,'Offset masek je b.rect.topleft − a.rect.topleft; testujte skutečné společné pixely i záporné posuny.')
            else:
                dx=a.rect.centerx-b.rect.centerx;dy=a.rect.centery-b.rect.centery
                require(result=={'rect':a.rect.colliderect(b.rect),'kruh':dx*dx+dy*dy<=100,'maska':expected} and all(type(v) is bool for v in result.values()),'Vraťte tři různá bool pravidla: Rect, kruh včetně dotyku, skutečné masky.')
            require((tuple(a.rect),tuple(b.rect),pixels(a.image),pixels(b.image))==before,'Kolize nic neposouvá ani nemaže.')
    elif task==2:
        obj=Body(surface,(15,25));center=obj.rect.center
        new=image((13,9),(10,20,30,50));new.set_at((8,2),(200,100,90,255));before=pixels(new)
        target(obj,new,80)
        require(obj.rect.center==center and obj.rect.size==new.get_size() and obj.image is not new and pixels(obj.image)==before and mask_matches(obj.mask,new,80),'Přestavte obraz, rozměr rect a masku, ale zachovejte střed.')
        obj.image.fill((1,2,3));require(pixels(new)==before,'Nový zdrojový obrázek zůstává nezměněný.')
    else:
        a,b,c,d=[Body(surface,p) for p in [(0,0),(0,0),(7,5),(100,100)]]
        first,second=pygame.sprite.Group(c,a,d),pygame.sprite.Group(b,a,c)
        before=first.sprites(),second.sprites()
        expected=[(x,y) for x in first for y in second if x is not y and occupied(x)&occupied(y)]
        require(target(first,second)==expected and (first.sprites(),second.sprites())==before,'Vraťte původní dvojice v pořadí skupin, bez párování objektu se sebou a bez mazání.')
        require(target(pygame.sprite.Group(),second)==[],'Prázdná skupina vrací prázdný seznam.')
    return True


def camera(ns,task):
    target=ns[NAMES[3][task]]
    if task==0:
        for view,world in [(pygame.Rect(17,23,80,60),pygame.Rect(-100,-70,400,300)),(pygame.Rect(20,30,600,400),pygame.Rect(-25,-15,70,60))]:
            saved=tuple(view),tuple(world);obj=target(view,world)
            require(obj.vyhled is not view and obj.svet is not world and isinstance(obj.posun,pygame.Vector2) and tuple(obj.posun)==world.topleft,'Kamera vlastní kopie Rect a přesný počáteční posun na začátku světa.')
            for point in [pygame.Vector2(-500,-500),pygame.Vector2(4.5,17.25),pygame.Vector2(9999,9999)]:
                before=tuple(point);obj.sleduj(point)
                expected=(max(world.left,min(max(world.left,world.right-view.width),point.x-view.width/2)),max(world.top,min(max(world.top,world.bottom-view.height),point.y-view.height/2)))
                require(close(obj.posun,expected) and tuple(point)==before and (tuple(view),tuple(world))==saved,'Sledujte střed, omezte obě osy na svět; menší svět kotví vlevo nahoře, vstupy neměňte.')
    elif task in (1,2):
        obj=SimpleNamespace(vyhled=pygame.Rect(17,23,70,50),posun=pygame.Vector2(140.25,-90.5))
        for point in [pygame.Vector2(-5.3,14.2),pygame.Vector2(500,700)]:
            before=tuple(point),tuple(obj.posun),tuple(obj.vyhled)
            expected=(point.x-140.25+17,point.y+90.5+23) if task==1 else (point.x+140.25-17,point.y-90.5-23)
            result=target(obj,point)
            require(isinstance(result,pygame.Vector2) and result is not point and close(result,expected) and (tuple(point),tuple(obj.posun),tuple(obj.vyhled))==before,'Převádějte i desetinné souřadnice s offsetem výhledu, bez změny vstupů.')
    elif task==3:
        obj=SimpleNamespace(vyhled=pygame.Rect(17,23,70,50),posun=pygame.Vector2(140.25,-90.5))
        objects=[Body(image((5,5)),p) for p in [(135,-85),(136,-85),(210,-85),(211,-85),(150,-40),(150,-100),(150,-90)]]
        objects=[objects[2],objects[0],objects[6],objects[1],objects[4],objects[3],objects[5],objects[2]]
        before=[tuple(o.rect) for o in objects]
        expected=[o for o in objects if o.rect.left<210.25 and o.rect.right>140.25 and o.rect.top<-40.5 and o.rect.bottom>-90.5]
        require(target(objects,obj)==expected and [tuple(o.rect) for o in objects]==before,'Viditelnost je kladný průnik se světovým výhledem, zachovejte pořadí i identity.')
        obj.posun=pygame.Vector2(140,-90)
        require(objects[1] not in target(objects,obj),'Pouhý dotyk hran neznamená viditelnost.')
    else:
        surface=image((180,140),(13,23,33,255));surface.set_clip((30,35,100,90));old=surface.get_clip();expected=surface.copy();expected.set_clip(None)
        obj=SimpleNamespace(vyhled=pygame.Rect(20,25,90,70),posun=pygame.Vector2(-4.25,8.75))
        objects=[Body(image((12,9),color),p) for color,p in [((80,180,255,255),(-8,5)),((90,220,175,255),(30,35)),((235,160,85,255),(75,65)),((195,145,255,255),(150,90))]]
        originals=[(tuple(o.rect),pixels(o.image)) for o in objects]
        clip=old.clip(obj.vyhled)
        for o in objects:
            dx=round(o.rect.x+4.25+20);dy=round(o.rect.y-8.75+25)
            for x in range(o.image.get_width()):
                for y in range(o.image.get_height()):
                    if clip.collidepoint(dx+x,dy+y):expected.set_at((dx+x,dy+y),o.image.get_at((x,y)))
        target(surface,objects,obj)
        require(pixels(surface)==pixels(expected) and surface.get_clip()==old and [(tuple(o.rect),pixels(o.image)) for o in objects]==originals,'Kreslete v obrazovkových souřadnicích, průnikem původního clip a výhledu; obnovte clip a svět neměňte.')
        class Broken:
            rect=pygame.Rect(30,35,5,5)
            @property
            def image(self):raise RuntimeError('kreslení')
        try:target(surface,[Broken()],obj)
        except RuntimeError:pass
        else:require(False,'Chyba kreslení se má předat volajícímu.')
        require(surface.get_clip()==old,'Clip se obnovuje také při chybě, použijte finally.')
    return True


class Mode:
    def __init__(self,name):self.name=name;self.events=[];self.times=[];self.draws=[];self.action=None
    def zpracuj(self,event):self.events.append(event);return self.action
    def update(self,dt):self.times.append(dt)
    def kresli(self,surface):self.draws.append(surface);surface.append(self.name) if isinstance(surface,list) else None


def modes(ns,task):
    target=ns[NAMES[4][task]];pygame.font.init()
    event=pygame.event.Event(pygame.USEREVENT)
    if task==0:
        a,b=Mode('hra'),Mode('pauza');obj=target(a);require(obj.aktualni is a and obj.odeber() is False,'Zásobník vždy zachovává základní režim.')
        obj.update(.2);obj.vloz(b);b.action='zpet'
        require(obj.zpracuj(event)=='zpet' and b.events==[event] and not a.events,'Události předávejte jen vršku a vraťte jeho akci.')
        obj.update(.3);draws=[];obj.kresli(draws)
        require(a.times==[.2] and b.times==[.3] and draws==['hra','pauza'],'Aktualizuje se vršek, kreslí všechny vrstvy odspodu.')
        require(obj.odeber() is True and obj.aktualni is a and obj.odeber() is False,'Po odebrání pokračuje původní podklad, ne jeho kopie.')
    elif task==1:
        obj=target(pygame.font.Font(None,24))
        require(obj.zpracuj(pygame.event.Event(pygame.KEYDOWN,key=pygame.K_p))=='zpet','Pauza na P požádá o návrat.')
        for e in [event,pygame.event.Event(pygame.KEYUP,key=pygame.K_p),pygame.event.Event(pygame.KEYDOWN,key=pygame.K_m)]:
            require(obj.zpracuj(e) is None,'Ostatní události pauzu neruší.')
        obj.update(10);surface=image((120,80),(200,180,160,255));obj.kresli(surface)
        expected=[(old*85+new*170)/255 for old,new in zip((200,180,160),(10,18,30))]
        require(close(surface.get_at((0,0))[:3],surface.get_at((1,1))[:3]) and all(abs(a-b)<=2 for a,b in zip(surface.get_at((0,0))[:3],expected)),'Pauza míchá průhlednou vrstvu s podkladem, nevymaže jej plnou barvou.')
        require(any(surface.get_at((x,y)).r>220 for x in range(20,100) for y in range(20,60)),'Nápis PAUZA musí být skutečně vykreslený.')
    elif task==2:
        rect=pygame.Rect(20,30,100,40)
        class Font:
            def render(self,text,aa,color):require(text=='Start' and tuple(color)==(240,245,255),'Vykreslete správný popisek.');return image((10,6),color)
        obj=target(rect,'Start','hra',Font());rect.x=0
        require(obj.rect==pygame.Rect(20,30,100,40),'Tlačítko kopíruje předaný rect.')
        for point,expected in [((20,30),'hra'),((119,69),'hra'),((120,69),None),((119,70),None),((10,10),None)]:
            require(obj.zpracuj(pygame.event.Event(pygame.MOUSEBUTTONDOWN,button=1,pos=point))==expected,'Test kliknutí používá udalost.pos a polootevřený Rect.')
        require(obj.zpracuj(event) is None and obj.zpracuj(pygame.event.Event(pygame.MOUSEBUTTONUP,button=1,pos=(50,50))) is None and obj.zpracuj(pygame.event.Event(pygame.MOUSEBUTTONDOWN,button=3,pos=(50,50))) is None,'Pouze levý stisk spouští akci.')
        surface=image((150,100),(1,2,3,255));obj.kresli(surface)
        require(surface.get_at((70,50))[:3]==(240,245,255) and surface.get_at((5,5))[:3]==(1,2,3),'Popisek je uprostřed, okolí tlačítka zůstává stejné.')
    elif task==3:
        a,b=Mode('spodni'),Mode('horni');a.action='hra';b.action='konec';items=[a,b];obj=target(items);items.clear()
        require(obj.zpracuj(event)=='konec' and b.events==[event] and not a.events,'Při překrytí rozhodne horní tlačítko; seznam se při konstrukci kopíruje.')
        b.action=None;require(obj.zpracuj(event)=='hra','Pokračujte ke spodnímu tlačítku, pokud horní akci nemá.')
        obj.update(10);draws=[];obj.kresli(draws)
        require(not a.times and not b.times and draws==['spodni','horni'],'Nabídka neposouvá herní čas a kreslí tlačítka v pořadí.')
        require(target([]).zpracuj(event) is None,'Prázdná nabídka je platná.')
    else:
        a=Mode('hra');stack=ns['ZasobnikRezimu'](a);created=[]
        def make(name):mode=Mode(name);created.append(mode);return mode
        obj=target(stack,make);obj.update(.2);a.action='pauza';obj.zpracuj(event)
        pause=created[-1];obj.update(.3)
        require(obj.zasobnik is stack and stack.aktualni is pause and a.times==[.2] and pause.times==[.3],'Pauza se vkládá na původní zásobník, podklad stojí.')
        pause.action='zpet';obj.zpracuj(event);require(stack.aktualni is a,'Návrat jen odebere vršek.')
        a.action='nabidka';before=list(stack.rezimy);obj.zpracuj(event)
        require(obj.zasobnik is not stack and obj.zasobnik.aktualni is created[-1] and stack.rezimy==before,'Přechod do nabídky vytvoří nový zásobník, staré objekty nemění.')
        active=created[-1];active.action='neznamy';count=len(created);obj.zpracuj(event)
        require(len(created)==count,'Neznámá akce nespouští továrnu.')
        active.action='hra';obj.zpracuj(event);require(created[-1].name=='hra','Nová hra také používá předanou továrnu.')
        active=created[-1];active.action='konec';obj.zpracuj(event);before=len(active.events),len(active.times),len(created)
        obj.zpracuj(event);obj.update(3);require(obj.bezi is False and (len(active.events),len(active.times),len(created))==before,'Ukončený řidič už nepředává vstup ani čas.')
        obj=target(ns['ZasobnikRezimu'](Mode('zaloha')),make);obj.zpracuj(pygame.event.Event(pygame.QUIT));require(obj.bezi is False,'QUIT ukončí aplikaci bez ohledu na režim.')
        active=Mode('hra');active.action='nabidka';old=ns['ZasobnikRezimu'](active)
        def fail(name):raise RuntimeError('továrna')
        obj=target(old,fail)
        try:obj.zpracuj(event)
        except RuntimeError:pass
        else:require(False,'Chybu továrny neukrývejte.')
        require(obj.zasobnik is old and old.rezimy==[active],'Neúspěšná továrna nesmí rozbít původní zásobník.')
    return True


def over(c,ns,stage,task):
    probe=[resource,animation,collision,camera,modes][stage]
    ok,result=c.call({'probe':lambda:probe(ns or {},task)},'probe')
    c.add('Chování herní součásti',ok and result is True,'' if ok and result is True else f'{type(result).__name__}: {result}')
    c.add('Model bez okna a zvukového zařízení',pygame.display.get_surface() is None and pygame.mixer.get_init() is None,'Při importu neotevírejte okno ani mixer; zvuk je volitelný.')
    run=c.run(timeout=8)
    if c.no_error(run):
        path=Path('soucasti.png');data=path.read_bytes() if path.is_file() else b''
        c.add('Skutečný obrázkový náhled',data.startswith(b'\x89PNG\r\n\x1a\n') and len(data)>24 and struct.unpack('>II',data[16:24])==(720,420),'Ponechte připravený blok __main__, který vytvoří soucasti.png.')
