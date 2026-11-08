from pathlib import Path
import argparse
import pandas as pd
from predchozi import over_schema, vycisti_mereni, spoj_a_shrn, napis_zpravu, vytvor_vystupy

def main():
    parser=argparse.ArgumentParser(description="Analytická dílna: vlastní smyšlená měření")
    parser.add_argument("--mereni",default="mereni.csv")
    parser.add_argument("--mista",default="mista.csv")
    parser.add_argument("--vystup",default="vysledky")
    args=parser.parse_args()
    raw=pd.read_csv(args.mereni,sep=";",encoding="utf-8",dtype="str",keep_default_na=False)
    sites=pd.read_csv(args.mista,sep=";",encoding="utf-8",dtype="str",keep_default_na=False)
    if not over_schema(raw,["den","kod","teplota"]) or not over_schema(sites,["kod","nazev","oblast"]):
        raise ValueError("Nesprávné zdrojové sloupce.")
    cleaned=vycisti_mereni(raw)
    report=spoj_a_shrn(cleaned["cista"],sites)
    print(napis_zpravu(cleaned,report))
    print(vytvor_vystupy(cleaned,report,Path(args.vystup)))
if __name__=="__main__":main()
