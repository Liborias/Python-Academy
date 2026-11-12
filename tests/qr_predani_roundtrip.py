"""Volitelný vývojový smoke: pip install 'qrcode[pil]>=8.2,<9' 'zxing-cpp>=2.3,<4'.
Nezávislý dekodér není závislost kurzu ani unittest sady.
"""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from PIL import Image
import zxingcpp

ROOT=Path(__file__).resolve().parent.parent
BASE=ROOT/'courses/databaze/lessons'
IDS=['27-volitelne-qr-stitky','30-moje-pujcovna-a-zaverecne-overeni']

def main():
    with tempfile.TemporaryDirectory() as tmp:
        for lid in IDS:
            w=Path(tmp)/lid;d=BASE/lid;shutil.copytree(d/'files',w);shutil.copy(d/'solution.py',w/'reseni.py')
            module='reseni' if lid.startswith('27-') else 'qr_export'
            for text in ['PY-AKADEMIE:PUJ:18','  Žofie; štítek\ndruhý řádek  ','ž'*256]:
                code=f'from {module} import qr_png; import sys; assert qr_png(sys.argv[1],"stitek.png") is not None'
                subprocess.run([sys.executable,'-X','utf8','-c',code,text],cwd=w,check=True,capture_output=True,timeout=15)
                with Image.open(w/'stitek.png') as png:
                    decoded=zxingcpp.read_barcode(png)
                    assert decoded is not None and decoded.bytes==text.encode('utf-8'),decoded
                    assert png.getpixel((0,0)) in (1,255,(255,255,255))
            if lid.startswith('27-'):
                (w/'stitek.png').unlink()
                result=subprocess.run([sys.executable,'-S','-X','utf8','reseni.py'],cwd=w,capture_output=True,text=True,timeout=15)
                assert result.returncode==0 and 'volitelný' in result.stdout and not (w/'stitek.png').exists(),result
            if lid.startswith('30-'):
                def cli(*args):
                    return subprocess.run([sys.executable,'-X','utf8',str(w/'spust_pujcovnu.py'),*args],cwd=tmp,check=True,capture_output=True,text=True,timeout=15).stdout
                assert 'kód: 18' in cli('pridat','Míč', '2')
                cli('qr','1',str(w/'final.png'))
                with Image.open(w/'final.png') as png:assert zxingcpp.read_barcode(png).bytes==b'PY-AKADEMIE:PUJ:18'
                result=subprocess.run([sys.executable,'-S','-X','utf8',str(w/'spust_pujcovnu.py'),'qr','1',str(w/'chybi.png')],cwd=tmp,capture_output=True,text=True,timeout=15)
                assert result.returncode==2 and 'volitelný' in result.stderr and not (w/'chybi.png').exists(),result
                result=subprocess.run([sys.executable,'-S','-X','utf8',str(w/'spust_pujcovnu.py'),'prehled'],cwd=tmp,capture_output=True,text=True,timeout=15)
                assert result.returncode==0 and 'Míč' in result.stdout,result
        print('OK: skutečný QR 27/30, 6 UTF-8 roundtrip včetně mezer a 512 bajtů, CLI štítek a fallback bez site-packages; nezávislý zxing-cpp dekodér')

if __name__=='__main__':main()
