"""Hon na dronech: reálné modely, nezávislá geometrie a skutečný vstupní soubor."""
import math,os,random,struct
from pathlib import Path
from types import SimpleNamespace
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT','1')
import pygame

def require(ok,message):
    if not ok:raise AssertionError(message)

def near(a,b):
    return len(a)==len(b) and all(math.isclose(x,y,abs_tol=1e-8,rel_tol=1e-9) for x,y in zip(a,b))

def place(obj,point):
    obj.pozice=pygame.Vector2(point)
    obj.rect.center=tuple(round(v) for v in point)

def actors(ns):
    Player,Drone,World=ns['Hrac'],ns['Dron'],ns['Svet']
    require(isinstance(Player,type) and isinstance(Drone,type) and issubclass(Player,pygame.sprite.Sprite) and issubclass(Drone,pygame.sprite.Sprite),'Hrac a Dron jsou skutečné třídy Sprite.')
    bounds=pygame.Rect(-100,-80,400,300);source=pygame.Vector2(40.25,90.75)
    a,b=Player(source,bounds),Player(source,bounds)
    require(a.image.get_size()==(32,32) and a.radius==14 and a.rychlost==240 and a.pozice is not source and a.hranice is not bounds,'Hráč má vlastní obraz/polohu/hranice a předepsané rozměry.')
    a.rychlost=1
    for _ in range(100):a.update((3,4),.01)
    require(near(a.pozice,(40.85,91.55)) and a.rect.center==(41,92),'Normalizujte směr a uchovejte malé desetinné kroky.')
    require(near(b.pozice,source) and tuple(source)==(40.25,90.75),'Instance ani vstup nesmějí sdílet měnitelnou polohu.')
    for vector,point in [((1,1),(284,204)),((-1,-1),(-84,-64))]:
        obj=Player((40,40),bounds);direction=pygame.Vector2(vector);obj.update(direction,10)
        require(near(obj.pozice,point) and bounds.contains(obj.rect) and tuple(direction)==vector,'Omezte celou loď všemi čtyřmi hranami, vstupní směr neměňte.')
    obj=Player((40,40),bounds);obj.update((0,0),1);require(near(obj.pozice,(40,40)),'Nulový směr je platný.')
    d,e=Drone(source,37),Drone(source,37)
    target=d.cil(b);target.x+=50
    require(d.image.get_size()==(28,28) and d.radius==12 and d.rychlost==37 and d.pozice is not source and near(b.pozice,source),'Dron uchovává předané parametry a vrací vlastní kopii cíle.')
    before=e.image.get_at((14,14));d.image.fill((1,2,3));require(e.image.get_at((14,14))==before,'Obrázky dronů jsou nezávislé kopie.')
    w,other=World(),World()
    require(w.hranice is not ns['HRANICE'] and w.hrac is not other.hrac and w.drony is not other.drony and len(w.drony)==3 and w.skore==0 and w.cas==0,'Svet skládá vlastní začínající hráče, drony, data a čítače.')
    require([x.rect.center for x in w.drony]==[(110,140),(610,140),(610,430)],'Tréninkové pozice mají být předepsané.')
    require(w.seber_data() is False,'Vzdálená data se nesbírají.')
    for i in range(7):
        old=w.data;extra=pygame.sprite.Group(old);w.hrac.rect.center=old.rect.center
        require(w.seber_data() is True and w.skore==i+1 and w.data is not old and not extra and w.data.rect.center==ns['DATOVE_BODY'][(i+1)%5],'Sběr odstraní původní bod všude a posune cyklickou posloupnost, jeden bod na volání.')
    fresh=World();positions=[tuple(d.pozice) for d in fresh.drony];fresh.update((1,0),.05)
    require(fresh.cas==.05 and near(fresh.hrac.pozice,(372,300)) and [tuple(d.pozice) for d in fresh.drony]==positions,'Základní svět předává směr/čas, drony v prvním kroku ještě stojí.')
    return True

def movement_oracle(objects,player,dt,bounds,gap):
    positions=[tuple(d.pozice) for d in objects];result=[]
    for i,d in enumerate(objects):
        x,y=positions[i]
        target=tuple(player.pozice)
        if hasattr(d,'kotva') and math.dist(target,d.kotva)>d.dosah:target=tuple(d.kotva)
        dx,dy=target[0]-x,target[1]-y;distance=math.hypot(dx,dy)
        ux,uy=(dx/distance,dy/distance) if distance else (0,0)
        ax=ay=0
        for j,(ox,oy) in enumerate(positions):
            if i==j:continue
            length=math.hypot(x-ox,y-oy)
            if 0<length<gap:
                weight=(gap-length)/gap
                ax+=(x-ox)/length*weight;ay+=(y-oy)/length*weight
        ux+=ax*1.6;uy+=ay*1.6;length=math.hypot(ux,uy);step=d.rychlost*dt
        if ax==0 and ay==0:step=min(step,distance)
        if length:x+=ux/length*step;y+=uy/length*step
        result.append((max(bounds.left+14,min(bounds.right-14,x)),max(bounds.top+14,min(bounds.bottom-14,y))))
    return result

def steering(ns):
    Guard,Drone=ns['HlidacBodu'],ns['Dron'];player=SimpleNamespace(pozice=pygame.Vector2(260,200))
    anchor=pygame.Vector2(100,200);g=Guard(anchor,61,160)
    require(isinstance(g,Drone) and g.kotva is not anchor and g.rychlost==61 and g.dosah==160,'Hlídač dědí Dron a uchovává vlastní kotvu/parametry.')
    require(near(g.cil(player),(260,200)),'Dotyk dosahu se počítá.')
    place(g,(260,200));player.pozice.x=260.01;target=g.cil(player)
    require(near(target,anchor) and target is not g.kotva,'Dosah měřte od kotvy a mimo něj vraťte její kopii.')
    player.pozice.update(310,260);bounds=pygame.Rect(0,0,600,450)
    for dt in [0,.125,2]:
        specs=[((120,200),90),((142,202),60),((320,260),40),((120,200),70)]
        a=[Drone(p,s) for p,s in specs];b=[Drone(p,s) for p,s in specs]
        a.append(Guard((400,200),55,70));b.append(Guard((400,200),55,70))
        before=tuple(player.pozice),tuple(bounds);expected=movement_oracle(a,player,dt,bounds,42)
        ns['posun_drony'](pygame.sprite.Group(a),player,dt,bounds)
        ns['posun_drony'](list(reversed(b)),player,dt,bounds)
        require(all(near(d.pozice,p) and d.rect.center==tuple(round(v) for v in p) for d,p in zip(a,expected)),'Pohyb musí odpovídat normalizované cestě i odpuzování ze společných původních pozic.')
        require(all(near(x.pozice,y.pozice) for x,y in zip(a,b)),'Výsledek nesmí záviset na pořadí průchodu.')
        require((tuple(player.pozice),tuple(bounds))==before,'Pohyb dronů nemění cíl ani hranice.')
    player.pozice.update(101,100);d=Drone((100,100),95)
    ns['posun_drony']([d],player,1,bounds);require(near(d.pozice,(101,100)),'Osamělý dron nepřeletí svůj cíl.')
    ns['posun_drony']([d],player,.1,bounds);require(near(d.pozice,(101,100)),'Při nulové cestě nenormalizujte nulu.')
    for point,goal,expected in [((585,435),(1000,1000),(586,436)),((15,15),(-1000,-1000),(14,14))]:
        player.pozice.update(goal);d=Drone(point,95)
        ns['posun_drony']([d],player,1,bounds)
        require(near(d.pozice,expected) and bounds.contains(d.rect),'Respektujte všechny okraje celého obrazu.')
    ns['posun_drony']([],player,.1,bounds)
    return True

def entrances(bounds):
    l,r,t,b=bounds.left+14,bounds.right-14,bounds.top+14,bounds.bottom-14
    x,y=bounds.center
    return [(l,t),(x,t),(r,t),(r,y),(r,b),(x,b),(l,b),(l,y)]

def waves(ns):
    cls=ns['Vlny'];a,b=cls(17,.5),cls(17,.5)
    require(a.cislo==1 and a.cekaji==3 and a.cas==0 and a.vytvoreno==0 and not a.drony and a.drony is not b.drony,'První vlna má tři čekající, prázdnou vlastní skupinu a nulový čas.')
    require(isinstance(a.rng,random.Random) and a.rng.getstate()==random.Random(17).getstate(),'Použijte vlastní generátor s předaným seedem bez předčasného losování.')
    player=SimpleNamespace(pozice=pygame.Vector2(360,300));bounds=pygame.Rect(24,90,672,390)
    rng=random.Random(17);options=[p for p in entrances(bounds) if math.dist(p,player.pozice)>=150]
    for i in range(4):
        obj=a.pridej(player,bounds)
        require(obj in a.drony and obj.rect.center==rng.choice(options) and isinstance(obj,ns['HlidacBodu'] if i%2 else ns['Dron']),'Losujte ze vzdálených vstupů a střídejte původní typy.')
        require(obj.rychlost==(80 if i%2 else 90) and a.cekaji==3 and a.vytvoreno==i+1,'Pridej používá rychlost vlny a nemění frontu ani čas.')
    group=a.drony;extra=pygame.sprite.Group(*a.drony)
    a.zahaj();require(a.drony is group and not extra and a.cislo==2 and a.cekaji==4 and a.vytvoreno==0,'Nová vlna killne všechna členství, zachová tutéž skupinu a obnoví frontu.')
    a.update(.25,player,bounds);require(not a.drony and a.cas==.25,'Před intervalem nic nevytvářejte.')
    a.update(1,player,bounds);require(len(a.drony)==2 and a.cekaji==2 and a.cas==.25,'Dohánějte více intervalů se zbytkem.')
    positions=[tuple(d.pozice) for d in a.drony]
    a.update(3,player,bounds);require(a.cekaji==0 and len(a.drony)==4 and a.cas==0 and [tuple(d.pozice) for d in a.drony][:2]==positions,'Vlny neposouvají existující drony a po vyčerpání vynulují čas.')
    before=a.rng.getstate();a.update(5,player,bounds);require(a.rng.getstate()==before and a.cas==0,'Prázdná fronta nic nedělá.')
    a=cls(17);a.cislo=30;a.cekaji=0
    class NoRng:
        def choice(self,items):raise AssertionError('Náhradní vstup nesmí losovat.')
    a.rng=NoRng();tiny=pygame.Rect(-20,-20,40,40);player.pozice.update(0,0)
    obj=a.pridej(player,tiny)
    expected=max(entrances(tiny),key=lambda p:math.hypot(*p))
    require(obj.rect.center==expected and obj.rychlost==140,'V malé aréně použijte nejvzdálenější vstup bez losování a strop rychlosti.')
    for interval in [0,-1]:
        try:cls(interval=interval)
        except ValueError:pass
        else:require(False,'Nekladný interval odmítněte ValueError.')
    return True

def world_state(k):
    return (k.cas,k.skore,k.zivoty,k.zbyva,k.stit.energie,k.nezranitelnost,k.duvod,k.vlny.cislo,k.vlny.cekaji,k.vlny.cas,k.vlny.rng.getstate(),tuple(k.hrac.pozice),tuple(k.data.rect),[(id(d),tuple(d.pozice)) for d in k.drony])

def rounds(ns):
    Shield,Round=ns['StitZakladny'],ns['Kolo']
    s=Shield();require(s.update(.5,True) is True and s.energie==2,'Štít spotřebovává čas uvnitř.')
    s.energie=.1;require(s.update(.2,True) is False and s.energie==0,'Částečná energie nechrání celý krok.')
    require(s.update(0,True) is False,'Prázdný štít nechrání ani při dt=0.')
    require(s.update(1,False) is False and s.energie==.5,'Mimo přístav se dobíjí, ale nechrání.')
    s.update(10,False);require(s.energie==2.5,'Obnova nepřekročí kapacitu.')
    custom=Shield(1,2);require(custom.update(1,True) is True and custom.energie==0,'Přesná kapacita pokryje interval.')
    custom.update(.2,False);require(math.isclose(custom.energie,.4),'Použijte vlastní rychlost obnovy.')
    k=Round(17)
    require(isinstance(k,ns['Svet']) and k.drony is k.vlny.drony and not k.drony and k.zona is not ns['ZONA'] and k.zivoty==3 and k.zbyva==10 and k.vlny.cislo==1,'Kolo skládá nové vlny a štít, sdílí jejich skupinu a kopíruje zónu.')
    require(k.vlny.rng.getstate()==random.Random(17).getstate(),'Seed projde do vln.')
    k.vlny.cekaji=0
    for i in range(2):k.drony.add(ns['Dron'](k.hrac.rect.center,0))
    k.drony.add(ns['Dron']((600,450),0))
    extra=pygame.sprite.Group(*k.drony)
    k.update((0,0),.05);require(k.chraneno and k.zivoty==3 and math.isclose(k.stit.energie,2.45),'Přístav s energií pohltí kontakty a spotřebuje ochranu.')
    k.stit.energie=.01;k.update((0,0),.02)
    require(not k.chraneno and k.zivoty==2 and k.nezranitelnost==.9 and len(extra)==3,'Bez energie dávka ubere jediný život a drony zůstanou.')
    k.update((0,0),.05);require(k.zivoty==2 and math.isclose(k.nezranitelnost,.85),'Kontakty neprodlužují nezranitelnost.')
    for dx,expected in [(15,False),(16,True)]:
        t=Round();t.vlny.cekaji=0;place(t.hrac,(t.zona.left+dx,t.zona.centery));t.update((0,0),.01)
        require(t.chraneno is expected,'Zóna vyžaduje celý obrázek, ne jen střed.')
    for offset,expected in [((26,0),2),((25,25),3)]:
        t=Round();t.vlny.cekaji=0;place(t.hrac,(100,200));t.drony.add(ns['Dron']((100+offset[0],200+offset[1]),0));t.update((0,0),0)
        require(t.zivoty==expected,'Použijte kruhy včetně přesného dotyku, ne pouze Rect.')
    t=Round();t.vlny.cekaji=0;place(t.hrac,(100,200));t.drony.add(ns['Dron']((100,200),0))
    t.zivoty=1;t.skore=5;t.data.rect.center=t.hrac.rect.center;t.zbyva=.01;t.vlny.cislo=3;t.update((0,0),.02)
    require(t.konec and t.duvod=='zivoty' and t.skore==5,'Smrtelný kontakt předchází sběru a úspěchu.')
    before=world_state(t);t.update((1,0),.05);require(world_state(t)==before,'Konec zmrazí celý svět i náhodu.')
    t=Round();t.vlny.cekaji=0;place(t.hrac,(100,200));t.skore=4;t.zivoty=2;t.stit.energie=.7;t.nezranitelnost=.5;t.zbyva=.01
    data=t.data;t.update((0,0),.02)
    require(t.vlny.cislo==2 and t.zbyva==10 and t.zivoty==2 and t.skore==4 and t.data is data and math.isclose(t.stit.energie,.71) and math.isclose(t.nezranitelnost,.48),'Nová vlna zachová data, životy i štít; čas vlny se obnoví.')
    for score,reason in [(5,'data'),(6,'uspech')]:
        t=Round();t.vlny.cekaji=0;place(t.hrac,(100,200));t.vlny.cislo=3;t.zbyva=.01;t.skore=score;t.update((0,0),.02)
        require(t.konec and t.duvod==reason and t.zbyva==0,'Třetí vlna rozlišuje dostatek a nedostatek dat.')
    return True

def game(ns):
    cls=ns['Hra'];key=lambda k:pygame.event.Event(pygame.KEYDOWN,key=k)
    h=cls(17);require(h.bezi is True and h.stav=='nabidka' and h.kolo is None,'Nabídka ještě nemá běžící kolo.')
    for e in [key(pygame.K_r),key(pygame.K_p),pygame.event.Event(pygame.KEYUP,key=pygame.K_SPACE)]:h.zpracuj(e)
    h.update((1,0),.05);require(h.kolo is None,'Nabídka nezačne na R/P/KEYUP.')
    h.zpracuj(key(pygame.K_SPACE));k=h.kolo;let=h.zasobnik.aktualni;direction=pygame.Vector2(1,0)
    h.update(direction,.02)
    require(h.stav=='hra' and k.cas==.02 and let.smer is not direction and tuple(direction)==(1,0),'Směr kopírujte, předávejte čas právě jednou.')
    h.zpracuj(key(pygame.K_p));before=world_state(k)
    h.update((1,1),.05);h.zpracuj(pygame.event.Event(pygame.KEYUP,key=pygame.K_p))
    require(h.stav=='pauza' and world_state(k)==before,'Pauza zachová svět, frontu, energii i čas.')
    h.zpracuj(key(pygame.K_p));require(h.stav=='hra' and h.kolo is k and h.zasobnik.aktualni is let,'Pokračuje stejný podklad.')
    k.vlny.pridej(k.hrac,k.hranice);before=world_state(k);old_stack=h.zasobnik
    h.zpracuj(key(pygame.K_p));h.zpracuj(key(pygame.K_r))
    require(h.stav=='hra' and h.kolo is not k and h.zasobnik is not old_stack and world_state(k)==before and h.kolo.zivoty==3 and h.kolo.skore==0 and h.kolo.vlny.rng.getstate()==random.Random(17).getstate(),'Restart v pauze vytvoří čistý svět se seedem bez ničení starého.')
    old=h.kolo;old.konec=True;old.duvod='uspech';h.update((0,0),0)
    require(h.stav=='vysledek' and h.kolo is old and h.zasobnik.aktualni.kolo is old,'Výsledek drží právě dokončený model.')
    h.zpracuj(key(pygame.K_p));require(h.stav=='vysledek','P ve výsledku nic nedělá.')
    h.zpracuj(key(pygame.K_r));require(h.stav=='hra' and h.kolo is not old,'R z výsledku spouští nový let.')
    h.kolo.konec=True;h.kolo.duvod='data';h.update((0,0),0);h.zpracuj(key(pygame.K_SPACE))
    require(h.stav=='nabidka' and h.kolo is None,'Mezerník z výsledku vrací nabídku.')
    for state in ['nabidka','hra','pauza','vysledek']:
        h=cls(17)
        if state!='nabidka':h.novy_let()
        if state=='pauza':h.zpracuj(key(pygame.K_p))
        if state=='vysledek':h.kolo.konec=True;h.kolo.duvod='data';h.update((0,0),0)
        k=h.kolo;before=world_state(k) if k is not None else None
        h.zpracuj(pygame.event.Event(pygame.QUIT));h.zpracuj(key(pygame.K_r));h.zpracuj(key(pygame.K_SPACE));h.update((1,0),.05)
        require(h.bezi is False and h.kolo is k and (world_state(k) if k is not None else None)==before,'QUIT funguje všude a další vstup neobnoví program.')
    h=cls();h.zpracuj(key(pygame.K_ESCAPE));require(h.bezi is False,'Escape funguje v nabídce.')
    atomic=cls(17);atomic.novy_let();old_kolo,old_stack=atomic.kolo,atomic.zasobnik
    env=cls.novy_let.__globals__;original=env['Kolo']
    def fail(seed):raise RuntimeError('konstrukce')
    env['Kolo']=fail
    try:
        try:atomic.novy_let()
        except RuntimeError:pass
        else:require(False,'Chybu konstrukce neukrývejte.')
        require(atomic.kolo is old_kolo and atomic.zasobnik is old_stack,'Neúspěšná konstrukce nesmí změnit starou hru.')
    finally:env['Kolo']=original
    seen=[];h.zasobnik=SimpleNamespace(kresli=lambda p:seen.append(p));target=object();h.kresli(target);require(seen==[target],'Kreslení deleguje do zásobníku i pro poslední snímek.')
    return True

def over(c,ns,stage):
    op=[actors,steering,waves,rounds,game][stage]
    ok,result=c.call({'probe':lambda:op(ns or {})},'probe')
    c.add('Pravidla nové části projektu',ok and result is True,'' if ok and result is True else f'{type(result).__name__}: {result}')
    c.add('Model bez otevření okna a mixeru',pygame.display.get_surface() is None and pygame.mixer.get_init() is None,'Displej otevírejte až pod __main__, zvuk není nutný.')
    events={64:[{'type':'QUIT'}]}
    if stage==4:
        events[0]=[{'type':'KEYDOWN','key':'K_SPACE'}];events[62]=[{'type':'KEYDOWN','key':'K_p'}]
    r=c.pygame_run(frames=80,pixels=[(383,300)],colors=[(245,135,90,24,90,672,390)],events=events,held={0:['K_RIGHT']})
    if c.pg_no_error(r):
        c.add('Viditelný hráč reaguje na vstup',r.size==[720,540] and 'Hon na dronech' in (r.caption or '') and r.frames==65 and r.pixel((383,300),frame=7)==(80,185,255),'Použijte skutečné okno a tentýž model pro pohyb/kreslení.')
        c.add('Viditelní droni a zavření',r.ended and r.color_count((245,135,90),region=(24,90,672,390))>10,'Fronta musí vytvořit skutečný dron a QUIT ukončit i pauzu.')
        c.add('Omezená smyčka',bool(r.fps) and all(v==60 for v in r.fps),'Použijte Clock.tick(60).')
        p=Path('droni.png');data=p.read_bytes() if p.is_file() else b''
        c.add('Poslední snímek',data.startswith(b'\x89PNG\r\n\x1a\n') and len(data)>24 and struct.unpack('>II',data[16:24])==(720,540),'Běžné ukončení uloží droni.png před pygame.quit.')
