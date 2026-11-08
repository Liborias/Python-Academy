"""Stahování CSV/XLSX: skutečné bajty, opt-in metadata, token a omezené soubory."""
import base64
import http.client
import io
import json
import sys
import tempfile
import threading
import time
import unittest
import zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from server.app import create_server
from server.runner import collect_exports,RunManager,MAX_IMAGE_BYTES,MAX_IMAGES_BYTES
CSV='kod;název\n001;Čaj\n'.encode('utf-8')

def xlsx():
    stream=io.BytesIO()
    with zipfile.ZipFile(stream,'w') as z:
        z.writestr('[Content_Types].xml','<Types/>');z.writestr('xl/workbook.xml','<workbook/>')
    return stream.getvalue()


def code():
    return 'from pathlib import Path\np=Path("vystupy/český přehled.csv");p.parent.mkdir();p.write_bytes('+repr(CSV)+')\nprint("hotovo")\n'


class FileDownloadTest(unittest.TestCase):
    def wait(self,run):
        end=time.monotonic()+10
        while time.monotonic()<end:
            result=run.poll(0)
            if result['done']:return result
            time.sleep(0.02)
        self.fail('Běh neskončil')

    def test_exact_csv_and_xlsx_bytes_names_mime_and_input_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'zdroj.csv').write_bytes(CSV);(root/'pod').mkdir();(root/'pod/přehled.xlsx').write_bytes(xlsx())
            files,notice=collect_exports(root)
            self.assertFalse(notice);self.assertEqual([x['name'] for x in files],['pod/přehled.xlsx','zdroj.csv'])
            self.assertEqual(base64.b64decode(files[0]['data']),xlsx());self.assertEqual(base64.b64decode(files[1]['data']),CSV)
            self.assertEqual(files[1]['mime'],'text/csv;charset=utf-8')
            self.assertTrue(files[0]['mime'].endswith('spreadsheetml.sheet'))

    def test_unsupported_invalid_files_and_links_are_not_sent(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);work=root/'run';work.mkdir()
            (work/'tajne.txt').write_text('neodesílat');(work/'chyba.csv').write_bytes(b'\xff\xfe')
            (work/'chyba.xlsx').write_text('csv není xlsx');(work/'jen_zip.xlsx').write_bytes(b'PK\x03\x04')
            outside=root/'mimo.csv';outside.write_bytes(CSV)
            try:
                (work/'link.csv').symlink_to(outside);(work/'adresar').symlink_to(root,target_is_directory=True)
            except OSError:pass
            files,notice=collect_exports(work);self.assertEqual(files,[]);self.assertTrue(notice)
            self.assertEqual(outside.read_bytes(),CSV)

    def test_per_file_total_and_count_limits(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            for i in range(8):(root/f'{i}.csv').write_bytes(CSV)
            files,notice=collect_exports(root);self.assertEqual(len(files),6);self.assertTrue(notice)
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            for i in range(3):(root/f'{i}.csv').write_bytes(b'a'*1_500_000)
            (root/'velky.csv').write_bytes(b'a'*(MAX_IMAGE_BYTES+1))
            files,notice=collect_exports(root);self.assertEqual(len(files),2);self.assertTrue(notice)
            self.assertLessEqual(sum(len(base64.b64decode(f['data'])) for f in files),MAX_IMAGES_BYTES)

    def test_run_copies_before_cleanup_and_plain_runs_stay_plain(self):
        with tempfile.TemporaryDirectory() as temp:
            manager=RunManager(Path(temp));run=manager.start(code(),download_files=True)
            result=self.wait(run);self.assertEqual(result['exit'],0);self.assertFalse(run.dir.exists())
            self.assertEqual(base64.b64decode(result['files'][0]['data']),CSV)
            self.assertEqual(run.poll(result['next'])['files'],result['files'])
            self.assertNotIn('files',self.wait(manager.start(code())))

    def test_error_after_export_keeps_file_and_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            result=self.wait(RunManager(Path(temp)).start(code()+'raise ValueError("chyba")',download_files=True))
            self.assertNotEqual(result['exit'],0);self.assertEqual(len(result['files']),1)

    def test_project_markdown_and_notebook_are_explicit_opt_in(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            (root/'README.md').write_text('# Český návod',encoding='utf-8')
            notebook={'nbformat':4,'nbformat_minor':5,'cells':[],'metadata':{}}
            (root/'analyza.ipynb').write_text(json.dumps(notebook),encoding='utf-8')
            (root/'tajne.py').write_text('nevydávat')
            self.assertEqual(collect_exports(root)[0],[])
            files,notice=collect_exports(root,['.md','.ipynb','.py'])
            self.assertFalse(notice);self.assertEqual({f['name'] for f in files},{'README.md','analyza.ipynb'})
            self.assertEqual(json.loads(base64.b64decode(next(f['data'] for f in files if f['name'].endswith('.ipynb')))),notebook)
            (root/'analyza.ipynb').write_text('{není JSON')
            files,notice=collect_exports(root,['.md','.ipynb'])
            self.assertEqual([f['name'] for f in files],['README.md']);self.assertTrue(notice)
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            for i in range(13):(root/f'{i}.md').write_text('# Výsledek',encoding='utf-8')
            files,notice=collect_exports(root,['.md'])
            self.assertEqual(len(files),12);self.assertTrue(notice)

    def test_project_formats_come_from_server_metadata(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);lesson=root/'courses/pokus/lessons/01-projekt';lesson.mkdir(parents=True)
            (lesson/'lesson.json').write_text(json.dumps({'download_files':True,'download_formats':['.md','.ipynb','.py']}))
            (lesson/'check.py').write_text('')
            server=create_server(root,'127.0.0.1',0);threading.Thread(target=server.serve_forever,daemon=True).start()
            def start(context):
                c=http.client.HTTPConnection('127.0.0.1',server.server_address[1],timeout=10)
                try:
                    code='from pathlib import Path\nPath("README.md").write_text("Návod",encoding="utf-8")\nPath("tajne.py").write_text("nevydávat")'
                    c.request('POST','/api/run',body=json.dumps({'code':code,**context}),headers={'X-Dilna-Token':server.token})
                    r=c.getresponse();self.assertEqual(r.status,200);return self.wait(server.runs.get(json.loads(r.read())['id']))
                finally:c.close()
            try:
                self.assertEqual([f['name'] for f in start({'course':'pokus','lesson':'01-projekt'})['files']],['README.md'])
                self.assertNotIn('files',start({'download_files':True,'download_formats':['.md']}))
            finally:server.runs.stop_all();server.shutdown();server.server_close()

    def test_api_main_lesson_opt_in_extra_tasks_and_token(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);lesson=root/'courses/pokus/lessons/01-soubory';lesson.mkdir(parents=True)
            (lesson/'lesson.json').write_text(json.dumps({'download_files':True}));(lesson/'check.py').write_text('')
            task=lesson/'tasks/task-2';task.mkdir(parents=True);(task/'check.py').write_text('')
            server=create_server(root,'127.0.0.1',0);threading.Thread(target=server.serve_forever,daemon=True).start()
            def req(method,path,body=None,token=True):
                c=http.client.HTTPConnection('127.0.0.1',server.server_address[1],timeout=10)
                try:
                    c.request(method,path,body=json.dumps(body) if body else None,headers={'X-Dilna-Token':server.token} if token else {})
                    r=c.getresponse();return r.status,json.loads(r.read())
                finally:c.close()
            try:
                status,result=req('POST','/api/run',{'code':code(),'course':'pokus','lesson':'01-soubory','task':'task-2'})
                self.assertEqual(status,200);rid=result['id']
                self.assertEqual(req('GET',f'/api/run/poll?id={rid}',token=False)[0],401)
                self.assertEqual(len(self.wait(server.runs.get(rid))['files']),1)
                status,result=req('POST','/api/run',{'code':code(),'download_files':True})
                self.assertEqual(status,200);self.assertNotIn('files',self.wait(server.runs.get(result['id'])))
            finally:server.runs.stop_all();server.shutdown();server.server_close()


if __name__=='__main__':unittest.main()
