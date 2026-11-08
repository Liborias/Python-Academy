"""Volitelné I/O kontroly: skutečné CSV/XLSX, význam hodnot a zachování zdrojů."""
from copy import deepcopy
import csv
import io
import math
import os
from pathlib import Path
import tempfile
import zipfile
import pandas as pd
from openpyxl import Workbook, load_workbook
from .pandas_tools import equivalent

PRICE = pd.DataFrame({'kod':['001','010','NA'],'nazev':['Čaj; med','Řádek\nnový','Voda'],'cena':[1.25,0.0,3.5]})
MEASURE = PRICE.rename(columns={'cena':'hodnota'})
SALES = pd.DataFrame({'kod':['010','001','001'],'kusy':[0,2,3]})


def book(path, sheets):
    wb=Workbook();wb.remove(wb.active)
    for name,rows in sheets.items():
        ws=wb.create_sheet(name)
        for row in rows:ws.append(row)
    wb.save(path);wb.close()


def rows(df):
    return [list(df.columns),*df.itertuples(index=False,name=None)]


def invoke(c,ns,fn,args,readonly=()):
    values=deepcopy(args);before=deepcopy(values)
    files={Path(p):Path(p).read_bytes() for p in readonly}
    ok,result=c.call(ns,fn,values)
    if not ok:c.add(f'{fn}: volání',False,f'{type(result).__name__}: {result}')
    c.add(f'{fn}: vstupy zachovány',equivalent(values,before,exact=True),'Vstupní tabulky a seznamy neměňte.')
    for path,data in files.items():
        c.add(f'{fn}: zdroj {path.name}',path.is_file() and path.read_bytes()==data,'Zdrojový soubor nepřepisujte ani nemažte.')
    return ok,result


def same_rows(actual,expected):
    if len(actual)!=len(expected):return False
    for a,b in zip(actual,expected):
        if len(a)!=len(b):return False
        for x,y in zip(a,b):
            if isinstance(y,(float,int)) and not isinstance(y,bool):
                if isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isclose(x,y,rel_tol=1e-12,abs_tol=1e-12):return False
            elif x!=y:return False
    return True


def excel_matches(path,sheets):
    try:
        wb=load_workbook(path,data_only=False)
        try:
            if wb.sheetnames!=list(sheets):return False
            for name,df in sheets.items():
                ws=wb[name];actual=list(ws.values)
                if not same_rows(actual,rows(df)):return False
                for col in df.columns:
                    if pd.api.types.is_string_dtype(df[col].dtype):
                        j=list(df.columns).index(col)+1
                        if any(ws.cell(i+2,j).data_type!='s' for i in range(len(df))):return False
            return True
        finally:wb.close()
    except (OSError,ValueError,KeyError,TypeError,zipfile.BadZipFile):return False


def csv_matches(text,df,*,bom=False):
    try:
        if isinstance(text,bytes):
            if text.startswith(b'\xef\xbb\xbf')!=bom:return False
            text=text.decode('utf-8-sig' if bom else 'utf-8')
        if not isinstance(text,str):return False
        content=list(csv.reader(io.StringIO(text,newline=''),delimiter=';'))
        if not content or content[0]!=list(df.columns) or len(content)!=len(df)+1:return False
        if any(len(row)!=len(df.columns) for row in content[1:]):return False
        if any('.' in value for row in content[1:] for value,col in zip(row,df.columns) if pd.api.types.is_numeric_dtype(df[col].dtype)):return False
        converted=[]
        for row in content[1:]:
            converted.append([float(v.replace(',','.')) if pd.api.types.is_numeric_dtype(df[col].dtype) else v for v,col in zip(row,df.columns)])
        return same_rows(converted,list(df.itertuples(index=False,name=None)))
    except (UnicodeError,ValueError,csv.Error):return False


def read_cases(c,ns,task):
    fn=['nacti_cenik','nazvy_listu','nacti_vybrane_sloupce','preskoc_poznamku','nacti_dva_listy'][task-1]
    for n in range(3):
        price=(PRICE if n==0 else PRICE.iloc[::-1] if n==1 else PRICE.head(0)).reset_index(drop=True)
        if n==1:price.loc[0,'cena']=0.1234567890123
        sales=(SALES if n!=2 else SALES.head(0)).copy()
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/f'český ceník {n}.xlsx'
            target='Jiný ceník' if n==1 and task==1 else 'Ceník'
            selected='Jiný výběr' if n==1 and task==3 else 'Výběr'
            note='Jiná poznámka' if n==1 and task==4 else 'S poznámkou'
            sheets={'Poznámky':[['info'],['Nesprávný první list']], target:rows(price),'Prodeje':rows(sales),
                    selected:rows(price.assign(poznamka='').loc[:,['cena','nazev','poznamka','kod']]),
                    note:[['Cvičný soubor'],['kod','cena'],*price[['kod','cena']].itertuples(index=False,name=None)]}
            book(path,sheets)
            if task==1:args=(str(path) if n==0 else path,target);expected=price
            elif task==2:args=(path,);expected=list(sheets)
            elif task==3:args=(path,selected);expected=price[['kod','nazev']]
            elif task==4:args=(path,note);expected=price[['kod','cena']]
            else:args=(path,);expected={'cenik':price,'prodeje':sales.reset_index(drop=True)}
            ok,result=invoke(c,ns,fn,args,[path])
            c.add(f'{fn}: list, data, textové kódy ({n+1})',ok and equivalent(result,expected),
                  'Vyberte správný list/hlavičku, pořadí sloupců a typy. Kódy 001 a text NA zachovejte.')


def csv_cases(c,ns,task):
    fn=['uloz_csv','csv_text','uloz_vyber','uloz_pro_excel','over_csv'][task-1]
    for n in range(3):
        data=(MEASURE if n==0 else MEASURE.iloc[::-1] if n==1 else MEASURE.head(0)).copy()
        if n==1:data.iloc[0,data.columns.get_loc('hodnota')]=0.1234567890123
        data.index=[f'řádek-{i+7}' for i in range(len(data))]
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'výstup.csv'
            if task==5:
                for changed in [False,True]:
                    other=data.copy()
                    if changed:
                        if len(other):other.iloc[0,other.columns.get_loc('hodnota')]+=0.01
                        else:other=MEASURE.iloc[[0]].copy()
                    other.to_csv(path,index=False,sep=';',decimal=',',encoding='utf-8')
                    ok,result=invoke(c,ns,fn,(data,path),[path])
                    c.add(f'{fn}: obsah {n}/{changed}',ok and equivalent(result,not changed),'Ověřte skutečný obsah, ne pouze existenci souboru.')
                continue
            chosen=['hodnota','kod'] if n!=1 else ['nazev']
            args=(data,) if task==2 else (data,path,chosen) if task==3 else (data,str(path) if n==0 else path)
            ok,result=invoke(c,ns,fn,args)
            try:
                raw=result if task==2 else path.read_bytes()
                expected=data[chosen] if task==3 else data
                valid=ok and csv_matches(raw,expected,bom=task==4)
                if task!=2:valid=valid and isinstance(result,Path) and result==path
            except OSError:valid=False
            c.add(f'{fn}: skutečné CSV ({n+1})',valid,'CSV má mít správné hlavičky/pořadí, středník, desetinnou čárku a UTF-8 bez indexu; BOM vyžaduje jen Úkol 4.')


def excel_cases(c,ns,task):
    fn=['uloz_excel','uloz_dva_listy','uloz_listy','zachovej_kody','over_excel'][task-1]
    for n in range(3):
        price=(PRICE if n==0 else PRICE.iloc[::-1] if n==1 else PRICE.head(0)).copy()
        if n==1:price.iloc[0,price.columns.get_loc('cena')]=0.1234567890123
        price.index=[f'X{i}' for i in range(len(price))]
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'nový přehled.xlsx'
            name='Ceník' if n==0 else 'Jiný list'
            if task==5:
                for changed in [False,True]:
                    other=price.copy()
                    if changed:
                        if len(other):other.iloc[0,other.columns.get_loc('cena')]+=0.01
                        else:other=PRICE.iloc[[0]].copy()
                    book(path,{'Nepoužít':[['info'],['První list není ceník']],name:rows(other)})
                    ok,result=invoke(c,ns,fn,(price,path,name),[path])
                    c.add(f'{fn}: obsah {n}/{changed}',ok and equivalent(result,not changed),'Přečtěte zadaný list, textové kódy a porovnejte obsah bez původního indexu.')
                continue
            if task==1:args=(price,str(path) if n==0 else path,name);sheets={name:price}
            elif task==2:args=(price,SALES.copy(),path);sheets={'Ceník':price,'Prodeje':SALES}
            elif task==3:
                sheets={'Záznamy':price[['kod','cena']],'Ceník jiný':SALES.copy()};args=(sheets,path)
            else:
                codes=SALES.rename(columns={'kusy':'pocet'}).copy()
                codes['kod']=['001','NA','010'];args=(codes,path);sheets={'Data':codes}
            ok,result=invoke(c,ns,fn,args)
            c.add(f'{fn}: skutečný sešit ({n+1})',ok and isinstance(result,Path) and result==path and excel_matches(path,sheets),
                  'Ověřte názvy/pořadí listů, hlavičky bez indexu, číselné hodnoty a skutečné textové kódy v XLSX.')


RAW='misto;hodnota;poznamka\n Brno ; 1,5 ;x\nPraha;2,5;x\nNA;0;x\nBrno;chyba;x\n;3,0;x\nOstrava; ;x\n Brno ;1,5;x\n'
CLEAN=pd.DataFrame({'misto':['Brno','Praha','NA','Brno'],'hodnota':[1.5,2.5,0.,1.5]})
SUMMARY=pd.DataFrame({'misto':['Brno','NA','Praha'],'pocet':[2,1,1],'prumer':[1.5,0.,2.5]})


def pipeline_cases(c,ns,task):
    fn=['zpracuj_mereni','souhrn_mist','zpracuj_soubory','uloz_souhrn','analyzuj_mereni'][task-1]
    for n in range(3):
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp);source=folder/'zdroj.csv';out=folder/'souhrn.csv'
            source.write_text(RAW if n==0 else 'misto;hodnota;poznamka\n' if n==1 else 'misto;hodnota;poznamka\n Zlín ;0;x\nZlín;4,25;x\n',encoding='utf-8')
            clean=CLEAN.copy() if n==0 else CLEAN.head(0) if n==1 else pd.DataFrame({'misto':['Zlín','Zlín'],'hodnota':[0.,4.25]})
            summary=SUMMARY.copy() if n==0 else SUMMARY.head(0) if n==1 else pd.DataFrame({'misto':['Zlín'],'pocet':[2],'prumer':[2.125]})
            if task==1:args=(source,);expected=clean
            elif task==2:args=(clean.copy(),);expected=summary
            elif task==3:
                paths=[source,source] if n==0 else [] if n==1 else [source]
                args=(paths,);expected=pd.concat([clean,clean],ignore_index=True) if n==0 else clean
            elif task==4:args=(summary,out);expected=out
            else:args=(source,out);expected=summary
            ok,result=invoke(c,ns,fn,args,[source])
            valid=ok and equivalent(result,expected)
            if task in (4,5):
                try:valid=valid and csv_matches(out.read_bytes(),summary)
                except OSError:valid=False
            c.add(f'{fn}: celý postup ({n+1})',valid,'Zachovejte NA jako název místa, nuly a opakovaná měření; vynechte jen prázdná místa a neplatné/neurčené hodnoty. Ověřte i prázdný vstup a skutečný export.')


def expected_report(data,month):
    days,products={},{}
    total={'radky':0,'kusy':0,'trzba':0.0}
    for day,product,qty,price in data[['den','produkt','kusy','cena']].itertuples(index=False,name=None):
        if day.strftime('%Y-%m')!=month:continue
        revenue=qty*price
        for collection,key in [(days,day.strftime('%Y-%m-%d')),(products,product)]:
            values=collection.setdefault(key,{'radky':0,'kusy':0,'trzba':0.0})
            values['radky']+=1;values['kusy']+=qty;values['trzba']+=revenue
        total['radky']+=1;total['kusy']+=qty;total['trzba']+=revenue
    def frame(values,key):
        return pd.DataFrame([{key:k,**values[k]} for k in sorted(values)],columns=[key,'radky','kusy','trzba']).astype({key:'str','radky':'int64','kusy':'int64','trzba':'float64'})
    return {'podle_dnu':frame(days,'den'),'podle_produktu':frame(products,'produkt'),'celkem':total}


def project_cases(c,ns):
    # Očekávané součty jsou nezávislý cyklus bez groupby a bez studentových helperů.
    data=pd.DataFrame({'den':pd.array(['2026-01-31','2026-02-01','2026-02-01','2026-02-28','2026-03-01','2026-02-28'],dtype='datetime64[us]'),
                       'produkt':['X','A','B','A','A','A'],'kusy':[7,2,1,0,3,2],'cena':[0.1,2.257,3.0,8.0,9.0,2.5]},index=['z','b','c','d','e','f'])
    data=pd.concat([data,data.iloc[[-1]]])
    leap=pd.DataFrame({'den':pd.array(['2024-02-29','2024-03-01','2024-12-31','2025-01-01'],dtype='datetime64[us]'),'produkt':['A','B','NA','A'],'kusy':[1,2,3,1],'cena':[0.1,0.2,0.3,1.5]})
    for source,month in [(data,'2026-02'),(data.iloc[::-1],'2026-01'),(data,'2026-04'),(data.head(0),'2026-02'),(leap,'2024-02'),(leap,'2024-12')]:
        positions=[i for i,d in enumerate(source['den']) if d.strftime('%Y-%m')==month]
        ok,filtered=invoke(c,ns,'vyber_mesic',(source,month))
        c.add(f'Měsíc {month}: přesný výběr',ok and equivalent(filtered,source.iloc[positions]),'Použijte celý měsíc od první půlnoci včetně do dalšího měsíce bez něj, zachovejte index/pořadí.')
        ok,report=invoke(c,ns,'prehled_mesice',(source,month))
        c.add(f'Měsíc {month}: skutečné souhrny',ok and equivalent(report,expected_report(source,month)),'Počítejte řádkovou tržbu kusy*cena, zachovejte opakované položky a prázdné souhrny.')
    os.environ.setdefault('MPLBACKEND','Agg')
    os.environ.setdefault('MPLCONFIGDIR',str(Path('.matplotlib').resolve()))
    from matplotlib.figure import Figure
    from .matplotlib_tools import figure_matches
    from unittest.mock import patch
    from PIL import Image
    for source in [data,data.head(0)]:
        report=expected_report(source,'2026-02');before=deepcopy(report)
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp)/'výstupy'/'únor'
            folder.mkdir(parents=True);sentinel=folder/'poznamka.txt';sentinel.write_text('zachovat')
            captured=[];original=Figure.savefig
            def save(fig,*args,**kwargs):
                captured.append(fig);return original(fig,*args,**kwargs)
            with patch.object(Figure,'savefig',save):ok,result=invoke(c,ns,'uloz_report',(report,folder))
            paths={'csv':folder/'podle_dnu.csv','excel':folder/'prehled.xlsx','graf':folder/'trzby.png'}
            try:
                valid=ok and result==paths and all(isinstance(p,Path) for p in result.values())
                valid=valid and csv_matches(paths['csv'].read_bytes(),report['podle_dnu'])
                valid=valid and excel_matches(paths['excel'],{'Dny':report['podle_dnu'],'Produkty':report['podle_produktu'],'Celkem':pd.DataFrame([report['celkem']])})
                with Image.open(paths['graf']) as image:
                    image.load();valid=valid and image.format=='PNG' and image.size==(720,480)
                products=report['podle_produktu']
                spec={'size':[6,4],'axes':[{'title':'Měsíční tržby podle produktů','xlabel':'Produkt','ylabel':'Tržba (Kč)','bars':products['trzba'].tolist(),'ticks':products['produkt'].tolist(),'zero':'y'}]}
                valid=valid and len(captured)==1 and figure_matches(captured[0],spec)
                valid=valid and sentinel.read_text()=='zachovat' and equivalent(report,before,exact=True)
            except (OSError,TypeError,AttributeError,ValueError):valid=False
            c.add('Skutečný měsíční report CSV/XLSX/PNG',valid,'Ověřte všechny tři výstupy, tabulky i datové sloupce grafu. Zdrojový přehled a jiné soubory ve složce zachovejte.')
