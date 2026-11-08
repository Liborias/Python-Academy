import json
import sys
from urllib.parse import urlsplit, parse_qs
from unittest.mock import patch
import requests
from dilna_check import check

c=check();sys.path.insert(0,str(c.student.parent));ns=c.load()
if ns and callable(ns.get('nacti_kurz')):
    log=[];plan={}
    def request(self,method,url,**options):
        prepared=requests.Request(method,url,params=options.get('params')).prepare()
        log.append((method,prepared.url,options.get('timeout')))
        if plan.get('error'):raise plan['error']('Cvičná chyba')
        response=requests.Response();response.status_code=plan.get('status',200)
        response.encoding='utf-8';response.url=prepared.url
        response._content=(plan['body'] if 'body' in plan else json.dumps(plan['json'],ensure_ascii=False)).encode('utf-8')
        return response
    with patch.object(requests.sessions.Session,'request',request):
        for index,(base,currency,rate) in enumerate([('http://prvni.test/sluzba',' eur ',42.75),('http://druha.test/','gbp',17)]):
            data={'mena':currency.strip().upper(),'czk_za_jednotku':rate,'datum':'2026-02-28','zdroj':'Test Žofie','navic':True}
            plan.clear();plan.update(json=data)
            before=len(log)
            c.returns(ns,'nacti_kurz',(base,currency),data)
            entries=log[before:]
            try:
                method,url,timeout=entries[0]
                times=timeout if isinstance(timeout,(list,tuple)) else [timeout]
                ok=len(entries)==1 and method.upper()=='GET' and urlsplit(url).path==urlsplit(base.rstrip('/')+'/kurz').path
                ok=ok and urlsplit(url).netloc==urlsplit(base).netloc and parse_qs(urlsplit(url).query)=={'mena':[data['mena']]}
                ok=ok and all(isinstance(t,(int,float)) and 0<t<=3 for t in times)
            except (IndexError,TypeError,ValueError):ok=False
            c.add('Skutečný požadavek s parametry '+str(index),ok,'Použijte předaný základ, /kurz, parametr mena, GET a kladný timeout do 3 sekund.')
        plan.clear();plan.update(status=503,json=data)
        c.raises(ns,'nacti_kurz',('http://test.invalid','EUR'),requests.HTTPError,'I platný JSON se stavem 503 musí odmítnout raise_for_status.')
        plan.clear();plan.update(error=requests.Timeout)
        c.raises(ns,'nacti_kurz',('http://test.invalid','EUR'),requests.Timeout,'Chybu čekání nechte předat volajícímu.')
        plan.clear();plan.update(body='{')
        c.raises(ns,'nacti_kurz',('http://test.invalid','EUR'),ValueError,'Tělo odpovědi rozebírejte jako JSON.')
else:c.add('Funkce nacti_kurz',False,'Definujte nacti_kurz(adresa, mena).')
c.done()
