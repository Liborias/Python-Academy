"""PNG náhledy: skutečný běh, kontext úkolu, limity, token a dočasné soubory."""
import base64
import http.client
import json
import struct
import sys
import tempfile
import threading
import time
import unittest
import zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from server.app import create_server
from server.runner import collect_images, RunManager, MAX_IMAGE_BYTES, MAX_IMAGES_BYTES


def png(width=1,height=1):
    def chunk(kind,data):
        return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data))
    return (b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',width,height,8,6,0,0,0))
            +chunk(b'IDAT',zlib.compress(b'\x00\xff\x00\x00\xff'*height))+chunk(b'IEND',b''))


def code_png():
    data=base64.b64encode(png()).decode()
    return f'import base64\nfrom pathlib import Path\np=Path("vystupy/český graf.png");p.parent.mkdir()\np.write_bytes(base64.b64decode({data!r}))\nprint("hotovo")\n'


class PlotPreviewTest(unittest.TestCase):
    def wait(self,run):
        end=time.monotonic()+10
        while time.monotonic()<end:
            result=run.poll(0)
            if result['done']:return result
            time.sleep(0.02)
        self.fail('Běh neskončil')

    def test_nested_pngs_are_preserved_as_bytes_and_cleanup_removes_nested_files(self):
        with tempfile.TemporaryDirectory() as temp:
            manager=RunManager(Path(temp));run=manager.start(code_png(),preview_images=True)
            result=self.wait(run)
            self.assertEqual(result['exit'],0)
            self.assertEqual([x['name'] for x in result['images']],['vystupy/český graf.png'])
            self.assertEqual(base64.b64decode(result['images'][0]['data']),png())
            self.assertFalse(run.dir.exists())
            self.assertEqual(run.poll(result['next'])['images'],result['images'])

    def test_plain_run_has_no_image_payload_and_no_graphics_library_import(self):
        with tempfile.TemporaryDirectory() as temp:
            run=RunManager(Path(temp)).start(code_png()+'import sys\nassert "matplotlib" not in sys.modules\n')
            result=self.wait(run)
            self.assertEqual(result['exit'],0);self.assertNotIn('images',result)
            self.assertFalse(run.dir.exists())

    def test_invalid_large_images_and_symbolic_links_are_skipped(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);directory=root/'run';directory.mkdir()
            (directory/'text.png').write_text('<script>bad</script>')
            (directory/'huge.png').write_bytes(png(100000,100000))
            (directory/'large.png').write_bytes(png()+b'0'*MAX_IMAGE_BYTES)
            (root/'outside.png').write_bytes(png())
            try:
                (directory/'link.png').symlink_to(root/'outside.png')
                (directory/'dirlink').symlink_to(root,target_is_directory=True)
            except OSError:pass
            images,notice=collect_images(directory)
            self.assertEqual(images,[]);self.assertTrue(notice)
            self.assertEqual((root/'outside.png').read_bytes(),png())

    def test_count_and_total_byte_limits_report_partial_previews(self):
        with tempfile.TemporaryDirectory() as temp:
            directory=Path(temp)
            for i in range(8):(directory/f'{i}.png').write_bytes(png())
            images,notice=collect_images(directory)
            self.assertEqual(len(images),6);self.assertTrue(notice)
        with tempfile.TemporaryDirectory() as temp:
            directory=Path(temp)
            for i in range(3):(directory/f'{i}.png').write_bytes(png()+b'0'*1_500_000)
            images,notice=collect_images(directory)
            self.assertEqual(len(images),2);self.assertTrue(notice)
            self.assertLessEqual(sum(len(base64.b64decode(p['data'])) for p in images),MAX_IMAGES_BYTES)

    def test_error_can_show_already_created_graph_without_hiding_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            run=RunManager(Path(temp)).start(code_png()+'raise ValueError("chyba po grafu")',preview_images=True)
            result=self.wait(run)
            self.assertNotEqual(result['exit'],0);self.assertEqual(len(result['images']),1)
            self.assertIn('ValueError',''.join(c['text'] for c in result['chunks']))

    def test_api_uses_main_lesson_metadata_for_extra_task_and_guards_poll(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);d=root/'courses/pokus/lessons/01-graf';d.mkdir(parents=True)
            (d/'lesson.json').write_text(json.dumps({'preview_images':True}));(d/'check.py').write_text('')
            task=d/'tasks/task-5';task.mkdir(parents=True);(task/'check.py').write_text('')
            server=create_server(root,'127.0.0.1',0)
            threading.Thread(target=server.serve_forever,daemon=True).start()
            def req(method,path,body=None,token=True):
                connection=http.client.HTTPConnection('127.0.0.1',server.server_address[1],timeout=10)
                try:
                    connection.request(method,path,body=json.dumps(body) if body else None,
                                       headers={'X-Dilna-Token':server.token} if token else {})
                    response=connection.getresponse();return response.status,json.loads(response.read())
                finally:connection.close()
            try:
                status,data=req('POST','/api/run',{'code':code_png(),'course':'pokus','lesson':'01-graf','task':'task-5'})
                self.assertEqual(status,200,data)
                self.assertEqual(req('GET',f'/api/run/poll?id={data["id"]}',token=False)[0],401)
                result=self.wait(server.runs.get(data['id']));self.assertEqual(len(result['images']),1)
                status,data=req('POST','/api/run',{'code':code_png(),'preview_images':True})
                self.assertEqual(status,200);self.assertNotIn('images',self.wait(server.runs.get(data['id'])))
                self.assertEqual(req('POST','/api/run',{'code':'pass','course':'pokus','lesson':'01-graf','task':'task-6'})[0],404)
            finally:server.runs.stop_all();server.shutdown();server.server_close()


if __name__=='__main__':unittest.main()
