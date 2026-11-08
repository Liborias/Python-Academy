import copy
import json
import sys
from unittest.mock import patch
import requests
from dilna_check import check

c=check();sys.path.insert(0,str(c.student.parent));ns=c.load()
valid={'mena':'EUR','czk_za_jednotku':27.5,'datum':'2026-02-28','zdroj':'  Test Žofie  ','navic':1}
expected={k:v for k,v in valid.items() if k!='navic'};expected['zdroj']='Test Žofie'
if ns and callable(ns.get('over_kurz')):
    data=copy.deepcopy(valid)
    c.returns(ns,'over_kurz',(data,' eur '),expected)
    c.add('Původní odpověď se nemění',data==valid,'Vraťte nový slovník a neupravujte původní data.')
    data=dict(valid,mena='USD',czk_za_jednotku=7,datum='2024-02-29',zdroj='Jiná data')
    c.returns(ns,'over_kurz',(data,'usd'),{k:v for k,v in data.items() if k!='navic'})
    bad=[None,[],{},dict(valid,mena='USD')]
    bad += [dict(valid,czk_za_jednotku=v) for v in [0,-1,True,'25',float('nan'),float('inf'),10**400]]
    bad += [dict(valid,datum=v) for v in [None,'','2026-02-30','20260228']]
    bad += [dict(valid,zdroj=v) for v in [None,0,'   ']]
    for i,data in enumerate(bad):
        ok,value=c.call(ns,'over_kurz',(data,'EUR'))
        c.add('Neplatný záznam '+str(i),not ok and isinstance(value,ValueError),'Ověřte typy, měnu, konečný kladný kurz, skutečné datum a neprázdný zdroj.')
    plan={};log=[]
    def request(self,method,url,**options):
        log.append((url,options))
        if plan.get('error'):raise plan['error']('Cvičná chyba')
        r=requests.Response();r.status_code=plan.get('status',200);r.encoding='utf-8';r.url=str(url)
        r._content=(plan['body'] if 'body' in plan else json.dumps(plan['json'],ensure_ascii=False)).encode('utf-8')
        return r
    with patch.object(requests.sessions.Session,'request',request):
        plan.update(json=valid)
        c.returns(ns,'nacti_kurz',('http://test.invalid',' eur '),expected,kwargs={'timeout':.25})
        c.add('Volající určuje timeout',bool(log) and log[-1][1].get('timeout')==.25,'Předejte parametr timeout do requests.')
        plan.clear();plan.update(status=503,json=valid)
        c.raises(ns,'nacti_kurz',('http://test.invalid','EUR'),requests.HTTPError)
        plan.clear();plan.update(error=requests.Timeout)
        c.raises(ns,'nacti_kurz',('http://test.invalid','EUR'),requests.Timeout)
        plan.clear();plan.update(body='{')
        c.raises(ns,'nacti_kurz',('http://test.invalid','EUR'),ValueError)
        plan.clear();plan.update(json=dict(valid,czk_za_jednotku=-1))
        c.raises(ns,'nacti_kurz',('http://test.invalid','EUR'),ValueError,'nacti_kurz musí skutečně použít ověření dat.')
else:c.add('Funkce over_kurz',False,'Definujte over_kurz(data, mena).')
c.done()
