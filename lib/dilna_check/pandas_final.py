"""Nezávislé kontroly závěrečného projektu: audit, obsah, exporty a předání."""
from copy import deepcopy
from datetime import datetime
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
import pandas as pd
from .pandas_tools import equivalent
from .pandas_files import invoke, csv_matches, same_rows, rows

RAW = pd.DataFrame({'den':['2026-03-01','2026-03-01','2026-03-02','2026-03-02','2026-03-02','2026-03-02','2026-02-30','2026-03-03','2026-03-03','2026-03-03','2026-03-03'],
                    'kod':[' 001 ','010','001','NA','999','001','010','','010','010','010'],
                    'teplota':[' 8,0 ','2,0','10,0','-2,0','7,0','10,0','3,0','5,0','chyba','inf','0']})
SITES = pd.DataFrame({'kod':['001','010','NA','777'],'nazev':['Dílna','Knihovna','Severní altán','Záloha'],'oblast':['jih','střed','sever','střed']})


def clean_oracle(source):
    good,bad=[],[]
    for i,(day,code,value) in enumerate(source[['den','kod','teplota']].itertuples(index=False,name=None),1):
        reason='';day_value=None;number=float('nan')
        try:day_value=datetime.strptime(day.strip(),'%Y-%m-%d')
        except ValueError:pass
        try:number=float(value.strip().replace(',','.'))
        except ValueError:pass
        if not code.strip():reason='chybi_kod'
        elif day_value is None:reason='neplatne_datum'
        elif not math.isfinite(number):reason='neplatna_teplota'
        if reason:bad.append({'radek':i,'den':day,'kod':code,'teplota':value,'duvod':reason})
        else:good.append({'radek':i,'den':day_value,'kod':code.strip(),'teplota':number})
    good=pd.DataFrame(good,columns=['radek','den','kod','teplota']).astype({'radek':'int64','den':'datetime64[us]','kod':'str','teplota':'float64'})
    bad=pd.DataFrame(bad,columns=['radek','den','kod','teplota','duvod']).astype({'radek':'int64','den':'str','kod':'str','teplota':'str','duvod':'str'})
    return {'cista':good,'odmitnuta':bad}


def report_oracle(clean,sites):
    known={row.kod:(row.nazev,row.oblast) for row in sites.itertuples(index=False)}
    matched,unknown=[],[];groups={};days={}
    for row in clean.to_dict('records'):
        if row['kod'] not in known:unknown.append(row);continue
        name,region=known[row['kod']];matched.append({**row,'nazev':name,'oblast':region})
        groups.setdefault((row['kod'],name),[]).append(row['teplota']);days.setdefault(row['den'],[]).append(row['teplota'])
    frame=pd.DataFrame(matched,columns=['radek','den','kod','teplota','nazev','oblast']).astype({'radek':'int64','den':'datetime64[us]','kod':'str','teplota':'float64','nazev':'str','oblast':'str'})
    missing=pd.DataFrame(unknown,columns=['radek','den','kod','teplota']).astype({'radek':'int64','den':'datetime64[us]','kod':'str','teplota':'float64'})
    stations=pd.DataFrame([{'kod':k,'nazev':n,'pocet':len(v),'prumer':sum(v)/len(v)} for (k,n),v in sorted(groups.items())],columns=['kod','nazev','pocet','prumer']).astype({'kod':'str','nazev':'str','pocet':'int64','prumer':'float64'})
    date_frame=pd.DataFrame([{'den':k,'pocet':len(v),'prumer':sum(v)/len(v)} for k,v in sorted(days.items())],columns=['den','pocet','prumer']).astype({'den':'datetime64[us]','pocet':'int64','prumer':'float64'})
    return {'spojena':frame,'nesparovana':missing,'podle_mist':stations,'podle_dnu':date_frame}


def sources():
    raw=RAW.copy();raw.index=['opakovaný']*len(raw)
    priority=pd.DataFrame({'den':['špatně','špatně','2024-02-29','2024-02-30','2026-01-01','2026-01-01'],
                           'kod':[' ','010','NA','001','010','999'],'teplota':['chyba','chyba','-0,125','3','nan','-inf']})
    precise=pd.DataFrame({'den':['2025-12-31','2026-01-01','2026-01-01'],'kod':['010','001','010'],'teplota':['-7,1256789','0','2,5']})
    return [raw,RAW.head(0),priority,precise,RAW.iloc[[4]].copy()]


def matches_text(text,cleaned,report):
    if not isinstance(text,str):return False
    fields={'Přijaté záznamy':len(cleaned['cista']),'Odmítnuté záznamy':len(cleaned['odmitnuta']),
            'Spárovaná měření':len(report['spojena']),'Nespárovaná měření':len(report['nesparovana'])}
    if not all(re.search(re.escape(key)+r':\s*'+str(value)+r'(?:\D|$)',text) for key,value in fields.items()):return False
    if len(report['spojena']):
        total=f"{report['spojena']['teplota'].mean():.2f}".replace('.',',')
        if 'Celkový průměr: '+total+' °C' not in text:return False
    elif 'neurčen' not in text:return False
    return 'Cvičná data' in text and 'neprokazují příčinu' in text and 'průměrem průměrů' in text


def audit_book_matches(path,cleaned,report):
    from openpyxl import load_workbook
    wb=load_workbook(path)
    try:
        expected={'Stanice':report['podle_mist'],'Dny':report['podle_dnu'],'Nespárovaná':report['nesparovana'],'Odmítnutá':cleaned['odmitnuta']}
        if wb.sheetnames!=list(expected):return False
        for name,frame in expected.items():
            actual=list(wb[name].values);wanted=rows(frame)
            if len(actual)!=len(wanted) or any(len(a)!=len(b) for a,b in zip(actual,wanted)):return False
            # XLSX neodlišuje prázdný text od prázdné buňky; původní text zůstává v auditu DataFrame/CSV.
            actual=[["" if x is None and y=="" else x for x,y in zip(a,b)] for a,b in zip(actual,wanted)]
            if not same_rows(actual,wanted):return False
        return True
    finally:wb.close()


def export_valid(paths,cleaned,report,captured):
    from PIL import Image
    from .matplotlib_tools import figure_matches
    try:
        if set(paths)!= {'csv','excel','graf','zprava'} or not all(isinstance(p,Path) and p.is_file() for p in paths.values()):return False
        if not csv_matches(paths['csv'].read_bytes(),report['podle_mist']):return False
        if not audit_book_matches(paths['excel'],cleaned,report):return False
        if not matches_text(paths['zprava'].read_text('utf-8'),cleaned,report):return False
        with Image.open(paths['graf']) as image:
            image.load()
            if image.format!='PNG' or image.size!=(720,480):return False
        stations=report['podle_mist']
        spec={'size':[6,4],'axes':[{'title':'Průměrné teploty podle stanic','xlabel':'Stanice (kód)','ylabel':'Teplota (°C)',
                                  'bars':stations['prumer'].tolist(),'ticks':stations['kod'].tolist()}]}
        if len(captured)!=1 or not figure_matches(captured[0],spec):return False
        low,high=captured[0].axes[0].get_ylim()
        values=stations['prumer'].tolist()+[0]
        return low<=min(values) and high>=max(values)
    except (OSError,ValueError,TypeError,KeyError,AttributeError,zipfile.BadZipFile):return False


def valid_notebook(notebook,expected_sources):
    try:
        notebook=json.loads(json.dumps(notebook,ensure_ascii=False))
        if type(notebook['nbformat']) is not int or notebook['nbformat']!=4:return False
        if type(notebook['nbformat_minor']) is not int or notebook['nbformat_minor']<5:return False
        cells=notebook['cells']
        if not isinstance(cells,list) or len(cells)!=len(expected_sources)+1:return False
        if not isinstance(notebook['metadata'],dict) or not all(isinstance(cell['metadata'],dict) for cell in cells):return False
        ids=[cell['id'] for cell in cells]
        if len(ids)!=len(set(ids)) or not all(isinstance(v,str) and re.fullmatch(r'[A-Za-z0-9_-]{1,64}',v) for v in ids):return False
        if cells[0]['cell_type']!='markdown' or '# Analytická dílna' not in ''.join(cells[0]['source']):return False
        code=[cell for cell in cells if cell['cell_type']=='code']
        if len(code)!=len(expected_sources):return False
        for cell,source in zip(code,expected_sources):
            if cell['execution_count'] is not None or cell['outputs']!=[] or ''.join(cell['source']).strip()!=source.strip():return False
        kernel=notebook['metadata']['kernelspec']
        return isinstance(kernel['name'],str) and bool(kernel['name']) and isinstance(kernel['display_name'],str) and bool(kernel['display_name']) and kernel['language']=='python' and notebook['metadata']['language_info']['name']=='python'
    except (KeyError,TypeError,ValueError,AttributeError):return False


def check_stage(c,ns,stage):
    if stage==0:
        cases=[(pd.DataFrame({'den':[],'kod':[],'teplota':[]}),['den','kod','teplota'],True),
               (RAW,['teplota','kod'],True),(RAW[['kod']],['den','kod'],False),
               (pd.DataFrame([[1,2,3]],columns=['den','kod','kod']),['den','kod'],False),
               (pd.DataFrame({'den':[],'kod':[]}),['den'],True),(['den','kod'],['den'],False)]
        for data,required,expected in cases:
            ok,value=invoke(c,ns,'over_schema',(data,required));c.add('Schéma a jedinečnost sloupců',ok and equivalent(value,expected),'Ověřte DataFrame, přítomnost všech požadovaných sloupců a jedinečnost názvů, ne počet řádků.')
    elif stage==1:
        for source in sources():
            ok,result=invoke(c,ns,'vycisti_mereni',(source,))
            c.add('Čistá data a přesný přehled odmítnutí',ok and equivalent(result,clean_oracle(source)),'Zachovejte číslo záznamu i původní text odmítnutých, prioritu důvodů, nuly, záporná čísla a platná opakování. Inf není měření.')
    elif stage==2:
        for source in sources():
            cleaned=clean_oracle(source)
            for sites in [SITES,SITES.head(0),SITES.assign(nazev=['Stejné jméno','Stejné jméno','Altán','Záloha'])]:
                ok,result=invoke(c,ns,'spoj_a_shrn',(cleaned['cista'],sites))
                c.add('Původ řádků a skutečné skupinové hodnoty',ok and equivalent(result,report_oracle(cleaned['cista'],sites)),'Neznámé kódy oddělte; skupiny určujte podle kódu i názvu. Ověřte data, typy, pořadí a prázdné výsledky.')
        for sites in [pd.concat([SITES,SITES.iloc[[0]]]),pd.concat([SITES,SITES.iloc[[-1]]])]:
            values=clean_oracle(RAW)['cista'];before=deepcopy((values,sites))
            c.raises(ns,'spoj_a_shrn',(values,sites),pd.errors.MergeError)
            c.add('Zachování při odmítnutí klíčů',equivalent((values,sites),before,exact=True),'Nejednoznačný katalog odmítněte bez deduplikace a bez změny vstupů.')
    elif stage==3:
        from matplotlib.figure import Figure
        from unittest.mock import patch
        for source in [RAW,RAW.head(0),sources()[3]]:
            cleaned=clean_oracle(source);report=report_oracle(cleaned['cista'],SITES)
            ok,text=invoke(c,ns,'napis_zpravu',(cleaned,report))
            c.add('Zpráva s fakty a omezením',ok and matches_text(text,cleaned,report),'Uveďte skutečné počty a celkový průměr ze všech spárovaných měření; u prázdných dat neurčený. Připojte vymezení cvičných dat a příčinných závěrů.')
            with tempfile.TemporaryDirectory() as temp:
                folder=Path(temp)/'výsledky';folder.mkdir();sentinel=folder/'poznamka.txt';sentinel.write_text('zachovat')
                captured=[];original=Figure.savefig
                def save(fig,*args,**kwargs):captured.append(fig);return original(fig,*args,**kwargs)
                with patch.object(Figure,'savefig',save):ok,paths=invoke(c,ns,'vytvor_vystupy',(cleaned,report,folder))
                expected={'csv':folder/'stanice.csv','excel':folder/'prehled.xlsx','graf':folder/'teploty.png','zprava':folder/'zprava.md'}
                c.add('Skutečné CSV/XLSX/PNG/MD',ok and paths==expected and export_valid(paths,cleaned,report,captured) and sentinel.read_text()=='zachovat','Vytvořte všechny čtyři soubory, správné listy a graf včetně záporných teplot, zachovejte přehled i jiné soubory.')
    elif stage==4:
        reference=report_oracle(clean_oracle(RAW)['cista'],SITES)
        cases=[(reference,deepcopy(reference),True),(report_oracle(clean_oracle(RAW.head(0))['cista'],SITES),report_oracle(clean_oracle(RAW.head(0))['cista'],SITES),True)]
        for key in reference:
            wrong=deepcopy(reference);wrong[key]=wrong[key].iloc[::-1].reset_index(drop=True);cases.append((reference,wrong,False if len(wrong[key])>1 else True))
        wrong=deepcopy(reference);wrong['podle_mist'].loc[0,'prumer']+=0.01;cases.append((reference,wrong,False))
        near=deepcopy(reference);near['podle_mist'].loc[0,'prumer']+=1e-13;cases.append((reference,near,True))
        wrong=deepcopy(reference);wrong['podle_mist']['pocet']=wrong['podle_mist']['pocet'].astype(float);cases.append((reference,wrong,False))
        wrong=deepcopy(reference);wrong.pop('spojena');cases.append((reference,wrong,False))
        for a,b,expected in cases:
            ok,result=invoke(c,ns,'over_prehled',(a,b));c.add('Obsah, struktura a tolerance',ok and equivalent(result,expected),'Porovnejte všechny tabulky, popisky, pořadí i dtype, čísla s tolerancí 1e-12; vraťte bool.')
        from test_dilna import spust_testy
        ok,result=c.call({'run':spust_testy},'run',((ns or {}).get('over_prehled'),))
        c.add('Osm veřejných testů',ok and result is True,'Spusťte veřejné testy, samotný shodný součet nestačí.')
    elif stage==5:
        from bunky import BUNKY
        ok,notebook=invoke(c,ns,'vytvor_notebook',())
        valid=ok and valid_notebook(notebook,BUNKY)
        c.add('Platná čistá struktura notebooku',valid,'Zachovejte dodané buňky ve správném pořadí, unikátní id, prázdné outputs a execution_count=None; formát 4.5 a Python kernel.')
        if valid:
            try:
                namespace={'__name__':'notebook'}
                for cell in notebook['cells']:
                    if cell['cell_type']=='code':exec(''.join(cell['source']),namespace)
                c.add('Spuštění od čistého jmenného prostoru',all(Path(p).is_file() for p in namespace['vystupy'].values()),'Notebook musí dojít od zdrojů ke skutečným výstupům bez skrytého stavu.')
            except Exception as error:c.add('Spuštění notebooku',False,f'{type(error).__name__}: {error}')
    elif stage==6:
        from matplotlib.figure import Figure
        from unittest.mock import patch
        for source in [RAW,sources()[3]]:
            with tempfile.TemporaryDirectory() as temp:
                root=Path(temp);rawpath=root/'nová měření.csv';sitespath=root/'katalog.csv';folder=root/'hotový projekt'
                folder.mkdir();sentinel=folder/'moje.txt';sentinel.write_text('zachovat')
                source.to_csv(rawpath,sep=';',encoding='utf-8',index=False);SITES.to_csv(sitespath,sep=';',encoding='utf-8',index=False)
                cleaned=clean_oracle(source);report=report_oracle(cleaned['cista'],SITES)
                captured=[];original=Figure.savefig
                def save(fig,*args,**kwargs):captured.append(fig);return original(fig,*args,**kwargs)
                with patch.object(Figure,'savefig',save):ok,result=invoke(c,ns,'spust_dilnu',(rawpath,sitespath,folder),[rawpath,sitespath])
                try:
                    valid=ok and sentinel.read_text()=='zachovat' and result['projekt']==folder and isinstance(result['projekt'],Path)
                    valid=valid and (result['prijato'],result['odmitnuto'],result['nesparovano'])==(len(cleaned['cista']),len(cleaned['odmitnuta']),len(report['nesparovana']))
                    valid=valid and export_valid(result['vystupy'],cleaned,report,captured)
                    valid=valid and (folder/'mereni.csv').read_bytes()==rawpath.read_bytes() and (folder/'mista.csv').read_bytes()==sitespath.read_bytes()
                    for file in Path('projekt').rglob('*'):
                        if file.is_file() and '__pycache__' not in file.parts:valid=valid and (folder/file.relative_to('projekt')).read_bytes()==file.read_bytes()
                    nb=json.loads((folder/'analyticka_dilna.ipynb').read_text('utf-8'))
                    from bunky import BUNKY
                    valid=valid and valid_notebook(nb,BUNKY)
                    if valid:
                        isolated=root/'samostatne';shutil.copytree(folder,isolated)
                        env=dict(os.environ);env.pop('PYTHONPATH',None);env['MPLCONFIGDIR']=str(root/'mpl')
                        for args in [('analyza.py',),('-m','unittest','-v','test_dilna')]:
                            run=subprocess.run([sys.executable,*args],cwd=isolated,env=env,capture_output=True,text=True,timeout=15)
                            valid=valid and run.returncode==0
                        valid=valid and csv_matches((isolated/'vysledky/stanice.csv').read_bytes(),report['podle_mist'])
                except (OSError,KeyError,TypeError,ValueError,subprocess.TimeoutExpired):valid=False
                c.add('Samostatně spustitelný předaný projekt',valid,'Předaný adresář musí obsahovat skutečné vstupy, podklady, notebook i výstupy a fungovat v jiné složce bez importů Akademie.')
