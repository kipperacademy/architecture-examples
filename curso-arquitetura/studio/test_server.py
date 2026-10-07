import json
import threading
import io
from types import SimpleNamespace
from email.message import Message
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
import urllib.error
from server import Studio, Handler, valid_origin
from pora_client import PoraClient

class StudioTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)/'studio'
        self.root.mkdir()
        self.write('content.json', {'editingStatus':'Edição pendente','lessons':[{'id':'one','number':1,'title':'Uma','poraContentId':'uuid-one'},{'id':'two','number':2,'title':'Duas','poraContentId':'uuid-two'}]})
        self.write('briefings.json',[{'id':'one','summary':'Resumo','points':['Ponto'],'audioPath':'studio/audio/one.mp3'}])
        self.write('examples.json',[])
        self.pora = Mock()
        self.app = Studio(self.root,self.pora,Mock())
    def tearDown(self):
        self.temp.cleanup()
    def write(self,name,value):
        (self.root/name).write_text(json.dumps(value))
    def test_finish_is_durable_before_remote_and_idempotent(self):
        self.app.start('one')
        self.app.finish('one')
        self.app.finish('one')
        persisted = json.loads((self.root/'runtime/state.json').read_text())
        self.assertEqual(persisted['one']['syncStatus'],'pending')
        self.pora.move_to_editing.assert_not_called()
        self.app.sync_due()
        self.app.sync_due()
        self.pora.move_to_editing.assert_called_once_with('uuid-one','Edição pendente')
        self.assertEqual(self.app.find('one')['syncStatus'],'synced')
    def test_failure_restart_and_retry(self):
        self.pora.move_to_editing.side_effect=RuntimeError('secret error')
        self.app.start('one'); self.app.finish('one'); self.app.sync_due()
        self.assertEqual(self.app.find('one')['syncStatus'],'error')
        self.assertNotIn('secret', (self.root/'runtime/state.json').read_text())
        restored = Studio(self.root,self.pora,Mock())
        restored.retry('one')
        self.pora.move_to_editing.side_effect=None
        restored.sync_due()
        self.assertEqual(restored.find('one')['syncStatus'],'synced')
    def test_pending_and_interrupted_sync_resume_after_restart(self):
        self.app.start('one'); self.app.finish('one')
        self.app.runtime['one']['syncStatus']='syncing'; self.app.save()
        restarted=Studio(self.root,self.pora,Mock())
        restarted.sync_due()
        self.pora.move_to_editing.assert_called_once()
    def test_single_recording_and_no_finish_without_start(self):
        with self.assertRaises(ValueError): self.app.finish('one')
        self.app.start('one'); self.app.start('one')
        with self.assertRaises(ValueError): self.app.start('two')
        self.app.finish('one'); self.app.start('two')
        with self.assertRaises(ValueError): self.app.start('one')
    def test_allowlisted_folder_no_client_command(self):
        folder=self.root.parent/'exemplos-para-gravar/safe';folder.mkdir(parents=True)
        self.write('examples.json',[{'id':'safe','path':str(folder),'command':'touch /tmp/never'}])
        self.app.open_example('safe')
        self.app.opener.assert_called_once_with(folder.resolve())
        self.write('examples.json',[{'id':'unsafe','path':'/tmp'}])
        with self.assertRaises(ValueError):self.app.open_example('unsafe')
        with self.assertRaises(ValueError):self.app.open_example('../../tmp')
    def test_audio_traversal_and_manifest_merge(self):
        (self.root/'audio').mkdir();(self.root/'audio/one.mp3').write_bytes(b'audio')
        self.assertEqual(self.app.find('one')['audioUrl'],'/audio/one.mp3')
        self.assertEqual(self.app.find('one')['summary'],'Resumo')
        self.assertIsNone(self.app.asset('/audio/%2e%2e/runtime/state.json'))
        self.assertIsNone(self.app.asset('/audio/%2e%2e/public/app.js'))
        self.assertIsNone(self.app.asset('/audio/one.txt'))
    def test_origin_and_dns_rebinding(self):
        self.assertTrue(valid_origin('127.0.0.1:8765','http://127.0.0.1:8765',8765))
        self.assertFalse(valid_origin('evil.test:8765','http://evil.test:8765',8765))
        self.assertFalse(valid_origin('127.0.0.1:8765','https://example.com',8765))
        self.assertFalse(valid_origin('127.0.0.1:8765','http://localhost:8766',8765))
    def handler(self,path,headers=None):
        handler=Handler.__new__(Handler)
        handler.server=SimpleNamespace(studio=self.app,server_port=8765)
        handler.path=path
        handler.headers=Message()
        handler.headers['Host']='127.0.0.1:8765'
        for key,value in (headers or {}).items():handler.headers[key]=value
        handler.wfile=io.BytesIO()
        handler.send_response=Mock();handler.send_header=Mock();handler.end_headers=Mock()
        return handler
    def test_audio_http_range(self):
        (self.root/'audio').mkdir();(self.root/'audio/one.mp3').write_bytes(b'abcdefghij')
        handler=self.handler('/audio/one.mp3',{'Range':'bytes=2-5'})
        handler.do_GET()
        handler.send_response.assert_called_once_with(206)
        self.assertEqual(handler.wfile.getvalue(),b'cdef')
        handler.send_header.assert_any_call('Content-Range','bytes 2-5/10')
        bad=self.handler('/audio/one.mp3',{'Range':'bytes=99-'})
        bad.do_GET();bad.send_response.assert_called_once_with(416)
    def test_cross_origin_mutation_is_rejected_before_changes(self):
        handler=self.handler('/api/lessons/one/start',{'Origin':'https://evil.test'})
        handler.do_POST()
        handler.send_response.assert_called_once_with(403)
        self.assertEqual(self.app.find('one')['status'],'queue')
        self.pora.move_to_editing.assert_not_called()
    def test_mcp_expired_session_clears_for_next_retry(self):
        config=self.root/'config.toml'
        config.write_text('[mcp_servers.pora]\nurl="https://example.test/mcp"\n')
        client=PoraClient(config)
        client.session='expired'
        with patch('pora_client.urllib.request.urlopen',side_effect=urllib.error.HTTPError('https://example.test/mcp',404,'expired',{},None)):
            with self.assertRaises(RuntimeError):client.rpc('tools/call',{})
        self.assertIsNone(client.session)
    def test_health_identifies_exact_workspace(self):
        handler=self.handler('/api/health')
        handler.do_GET()
        data=json.loads(handler.wfile.getvalue())
        self.assertEqual(data['app'],'kipperdev-architecture-studio')
        self.assertEqual(data['workspace'],str(self.root.resolve()))
    def test_source_folder_uses_new_zed_workspace(self):
        with patch('server.Path.is_file',return_value=True), patch('server.subprocess.run',return_value=SimpleNamespace(returncode=0)) as run:
            Studio.open_folder(Path('/safe/source'))
        self.assertEqual(run.call_args.args[0],['/Applications/Zed.app/Contents/MacOS/cli','--new','/safe/source'])
    def test_requeue_recording_is_local_and_persistent(self):
        self.app.start('one');self.app.requeue('one')
        restarted=Studio(self.root,self.pora,Mock())
        self.assertEqual(restarted.find('one')['status'],'queue')
        restarted.sync_due()
        self.pora.move_to_editing.assert_not_called()
        self.assertNotIn('syncTarget',restarted.find('one'))
    def test_requeue_editing_retries_target_after_restart(self):
        self.app.start('one');self.app.finish('one');self.app.requeue('one')
        self.assertEqual(self.app.find('one')['syncTarget'],'Gravação pendente')
        self.pora.move_to_editing.side_effect=RuntimeError('offline')
        self.app.sync_due()
        self.assertEqual(self.app.find('one')['status'],'queue')
        restarted=Studio(self.root,self.pora,Mock())
        restarted.retry('one')
        self.pora.move_to_editing.side_effect=None
        restarted.sync_due()
        self.assertEqual(restarted.find('one')['poraStatus'],'Gravação pendente')
        self.assertEqual(restarted.find('one')['syncStatus'],'synced')
        self.assertEqual(self.pora.move_to_editing.call_args.args,('uuid-one','Gravação pendente'))
    def test_requeue_supersedes_inflight_confirmation(self):
        self.app.start('one');self.app.finish('one')
        entered=threading.Event();release=threading.Event()
        def remote(*args):
            entered.set()
            self.assertTrue(release.wait(2))
        self.pora.move_to_editing.side_effect=remote
        worker=threading.Thread(target=self.app.sync_due)
        worker.start();self.assertTrue(entered.wait(2))
        self.app.requeue('one')
        new_version=self.app.find('one')['syncVersion']
        release.set();worker.join(2);self.assertFalse(worker.is_alive())
        lesson=self.app.find('one')
        self.assertEqual(lesson['status'],'queue')
        self.assertEqual(lesson['syncStatus'],'pending')
        self.assertEqual(lesson['syncVersion'],new_version)
        self.assertNotEqual(lesson.get('poraStatus'),'Edição pendente')
        self.pora.move_to_editing.side_effect=None
        self.app.sync_due()
        self.assertEqual(self.app.find('one')['poraStatus'],'Gravação pendente')
    def test_requeue_supersedes_inflight_failure(self):
        self.app.start('one');self.app.finish('one')
        def remote(*args):
            self.app.requeue('one')
            raise RuntimeError('obsolete failure')
        self.pora.move_to_editing.side_effect=remote
        self.app.sync_due()
        self.assertEqual(self.app.find('one')['syncStatus'],'pending')
        self.assertEqual(self.app.find('one')['attempts'],0)
        self.assertEqual(self.app.find('one')['syncTarget'],'Gravação pendente')
    def test_requeue_idempotent_and_metadata_unchanged(self):
        self.app.start('one');self.app.finish('one');self.app.requeue('one')
        before=self.app.find('one')['syncVersion']
        self.app.requeue('one')
        self.assertEqual(self.app.find('one')['syncVersion'],before)
        self.assertEqual(self.app.find('one')['title'],'Uma')
        with self.assertRaises(ValueError):self.app.requeue('published-intro')
    def test_lesson_deeplink_serves_app_without_allowing_traversal(self):
        self.assertEqual(self.app.asset('/aulas/one'),self.root/'public/index.html')
        self.assertEqual(self.app.asset('/aulas/unknown'),self.root/'public/index.html')
        self.assertIsNone(self.app.asset('/aulas/%2e%2e'))
        self.assertIsNone(self.app.asset('/aulas/%2e%2e/runtime/state.json'))
    def test_missing_zed_has_explicit_error_without_fallback(self):
        with patch('server.Path.is_file',return_value=False), patch('server.subprocess.run') as run:
            with self.assertRaisesRegex(ValueError,'Zed não está instalado'):
                Studio.open_folder(Path('/safe/source'))
            run.assert_not_called()
    def test_zed_error_has_no_editor_fallback(self):
        with patch('server.Path.is_file',return_value=True), patch('server.subprocess.run',return_value=SimpleNamespace(returncode=1)) as run:
            with self.assertRaisesRegex(ValueError,'nova janela do Zed'):
                Studio.open_folder(Path('/safe/source'))
            run.assert_called_once()
    def test_pora_requires_remote_readback(self):
        client=PoraClient()
        client.call=Mock(side_effect=[{}, {'contents':[{'id':'uuid-one','status':'Em criação'}]}])
        with self.assertRaises(RuntimeError): client.move_to_editing('uuid-one','Edição pendente')
        client.call=Mock(side_effect=[{}, {'contents':[{'id':'uuid-one','status':'Edição pendente'}]}])
        self.assertTrue(client.move_to_editing('uuid-one','Edição pendente'))
        self.assertEqual(client.call.call_args_list[1].args,('list_contents',{'creator':'Fernanda Kipper | Dev','type':'YOUTUBE','from':'2026-10-01','to':'2026-12-01'}))
        self.assertEqual(client.call.call_args_list[0].args,('update_content',{'contentId':'uuid-one','status':'Edição pendente'}))

if __name__ == '__main__':unittest.main()
