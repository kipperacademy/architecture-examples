#!/usr/bin/env python3
"""Local studio, durable recording queue and verified Pora synchronization."""
import argparse
import json
import mimetypes
import os
from pathlib import Path
import subprocess
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit, unquote
from pora_client import PoraClient

ROOT = Path(__file__).resolve().parent

def read_json(path, fallback):
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        return fallback

def entries(value):
    return value if isinstance(value, list) else value.get('lessons', [])

class Studio:
    def __init__(self, root=ROOT, pora=None, opener=None):
        self.root = Path(root)
        self.lock = threading.RLock()
        self.pora = pora or PoraClient()
        self.opener = opener or self.open_folder
        self.inflight = set()
        self.runtime_file = self.root / 'runtime/state.json'
        self.runtime = read_json(self.runtime_file, {})

    def save(self):
        self.runtime_file.parent.mkdir(parents=True, exist_ok=True)
        temp = self.runtime_file.with_suffix('.tmp')
        with temp.open('w') as file:
            json.dump(self.runtime, file, ensure_ascii=False, indent=2)
            file.flush()
            os.fsync(file.fileno())
        os.replace(temp, self.runtime_file)

    def state(self):
        with self.lock:
            content = read_json(self.root / 'content.json', {'lessons': []})
            result = dict(content) if isinstance(content, dict) else {}
            briefings = entries(read_json(self.root / 'briefings.json', []))
            examples = read_json(self.root / 'examples.json', [])
            if isinstance(examples, dict):
                examples = examples.get('examples', [])
            lessons = []
            for base in entries(content):
                lesson = dict(base)
                number = lesson.get('number', lesson.get('lessonNumber'))
                lesson['number'] = number
                briefing = next((b for b in briefings if b.get('id') == lesson['id'] or b.get('lessonNumber') == number), {})
                lesson.update({k:v for k,v in briefing.items() if k not in ('id','lessonNumber')})
                lesson['examples'] = [e for e in examples if e.get('lessonNumber') == number]
                lesson.update(self.runtime.get(lesson['id'], {}))
                lesson.setdefault('status', 'queue')
                audio_path = lesson.get('audioPath')
                if audio_path:
                    candidate = (self.root.parent / audio_path).resolve()
                    if candidate.is_relative_to((self.root / 'audio').resolve()) and candidate.is_file():
                        lesson['audioUrl'] = '/audio/' + candidate.relative_to((self.root / 'audio').resolve()).as_posix()
                    else:
                        lesson.pop('audioUrl', None)
                lessons.append(lesson)
            result['lessons'] = lessons
            return result

    def find(self, identity):
        lesson = next((l for l in self.state()['lessons'] if l['id'] == identity), None)
        if not lesson:
            raise ValueError('Aula não encontrada.')
        return lesson

    def start(self, identity):
        with self.lock:
            lesson = self.find(identity)
            if lesson['status'] == 'editing':
                raise ValueError('Esta aula já foi concluída.')
            if any(l['status'] == 'recording' and l['id'] != identity for l in self.state()['lessons']):
                raise ValueError('Conclua a aula em gravação antes de iniciar outra.')
            if lesson['status'] != 'recording':
                self.runtime.setdefault(identity, {}).update(status='recording', startedAt=time.time())
                self.save()
            return self.state()

    def finish(self, identity):
        with self.lock:
            lesson = self.find(identity)
            if lesson['status'] == 'editing':
                return self.state()
            if lesson['status'] != 'recording':
                raise ValueError('Inicie a gravação desta aula antes de concluir.')
            current = self.runtime.setdefault(identity, {})
            current.update(status='editing', finishedAt=time.time(), syncStatus='pending', syncTarget=self.state().get('editingStatus','Edição'), syncVersion=current.get('syncVersion',0)+1, attempts=0, retryAt=0)
            self.save()
            return self.state()

    def requeue(self, identity):
        with self.lock:
            lesson = self.find(identity)
            if lesson['status'] == 'queue':
                return self.state()
            current = self.runtime.setdefault(identity, {})
            needs_remote = lesson['status'] == 'editing' or current.get('remoteAttempted') or current.get('syncTarget')
            current.update(status='queue', requeuedAt=time.time())
            current.pop('finishedAt', None)
            current.pop('startedAt', None)
            if needs_remote:
                current.update(syncTarget='Gravação pendente', syncVersion=current.get('syncVersion',0)+1, syncStatus='pending', attempts=0, retryAt=0)
            self.save()
            return self.state()

    def retry(self, identity):
        with self.lock:
            lesson = self.find(identity)
            if lesson.get('syncStatus') == 'synced':
                return self.state()
            current = self.runtime.get(identity, {})
            if not current.get('syncTarget') and lesson['status'] != 'editing':
                raise ValueError('Esta aula não tem uma mudança pendente no Pora.')
            current = self.runtime.setdefault(identity, current)
            current.setdefault('syncTarget', self.state().get('editingStatus','Edição'))
            current.update(syncStatus='pending', retryAt=0)
            self.save()
            return self.state()

    def sync_due(self):
        for lesson in self.state()['lessons']:
            identity = lesson['id']
            with self.lock:
                current = self.runtime.get(identity, {})
                if current.get('syncStatus') not in ('pending','error','syncing') or current.get('retryAt',0) > time.time() or identity in self.inflight:
                    continue
                self.inflight.add(identity)
                version = current.get('syncVersion',0)
                target = current.get('syncTarget', self.state().get('editingStatus','Edição'))
                current.update(syncStatus='syncing', remoteAttempted=True)
                self.save()
            try:
                content_id = lesson.get('poraContentId', lesson.get('poraId', lesson.get('contentId')))
                if not content_id:
                    raise RuntimeError('Esta aula não tem um conteúdo associado no Pora.')
                self.pora.move_to_editing(content_id, target)
                with self.lock:
                    if current.get('syncVersion',0) == version:
                        current.update(syncStatus='synced', poraStatus=target, syncedAt=time.time())
                        current.pop('syncError', None)
            except Exception:
                with self.lock:
                    if current.get('syncVersion',0) == version:
                        attempt = current.get('attempts',0)+1
                        current.update(syncStatus='error', attempts=attempt, retryAt=time.time()+min(300, 5*2**min(attempt-1,6)), syncError='Não foi possível confirmar a mudança no Pora. Uma nova tentativa será feita automaticamente.')
            finally:
                with self.lock:
                    self.inflight.discard(identity)
                    self.save()

    def open_example(self, identity):
        examples = read_json(self.root/'examples.json', [])
        if isinstance(examples, dict):
            examples = examples.get('examples', [])
        example = next((e for e in examples if e['id'] == identity), None)
        if not example:
            raise ValueError('Exemplo não encontrado.')
        folder = Path(example['path']).resolve()
        allowed = (self.root.parent/'exemplos-para-gravar').resolve()
        if folder == allowed or not folder.is_relative_to(allowed) or not folder.is_dir():
            raise ValueError('A pasta do exemplo está indisponível.')
        self.opener(folder)
        return {'ok':True}

    @staticmethod
    def open_folder(folder):
        cli = Path('/Applications/Zed.app/Contents/MacOS/cli')
        if not cli.is_file():
            raise ValueError('O Zed não está instalado em /Applications/Zed.app. Instale-o para abrir os exemplos.')
        result = subprocess.run([str(cli),'--new',str(folder)], capture_output=True)
        if result.returncode:
            raise ValueError('Não foi possível abrir o exemplo em uma nova janela do Zed.')

    def asset(self, route):
        route = unquote(urlsplit(route).path)
        if route in ('/','/index.html') or route.startswith('/aulas/') and len(route.strip('/').split('/')) == 2 and route.split('/')[-1] not in ('.','..'):
            return self.root/'public/index.html'
        if route in ('/app.js','/style.css'):
            return self.root/'public'/route[1:]
        if route.startswith('/audio/'):
            folder = (self.root/'audio').resolve()
            candidate = (folder/route[len('/audio/'):]).resolve()
            if candidate.is_relative_to(folder) and candidate.suffix.lower() in ('.mp3','.wav','.m4a','.aiff'):
                return candidate
        return None

def valid_origin(host, origin, port):
    allowed = {f'127.0.0.1:{port}', f'localhost:{port}'}
    if host not in allowed:
        return False
    if origin:
        parsed = urlsplit(origin)
        return parsed.scheme == 'http' and parsed.netloc in allowed and not parsed.path
    return True

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        # Never log request URLs or arbitrary client data.
        print('Estúdio HTTP:', self.command, getattr(self,'response_code',''), flush=True)

    def json_response(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Content-Length',str(len(body)))
        self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if not valid_origin(self.headers.get('Host',''),None,self.server.server_port):
            return self.json_response({'error':'Host não permitido.'},403)
        route = urlsplit(self.path).path
        if route == '/api/health':
            return self.json_response({'app':'kipperdev-architecture-studio','version':1,'workspace':str(self.server.studio.root.resolve())})
        if route == '/api/state':
            return self.json_response(self.server.studio.state())
        file = self.server.studio.asset(route)
        if not file or not file.is_file():
            return self.json_response({'error':'Arquivo não encontrado.'},404)
        size = file.stat().st_size
        start, end, status = 0, size-1, 200
        value = self.headers.get('Range')
        if value:
            try:
                if not value.startswith('bytes=') or ',' in value:
                    raise ValueError()
                lo,hi = value[6:].split('-',1)
                start = int(lo) if lo else max(0,size-int(hi))
                end = min(int(hi),size-1) if hi and lo else size-1
                if start < 0 or start >= size or end < start:
                    raise ValueError()
                status = 206
            except ValueError:
                self.send_response(416)
                self.send_header('Content-Range',f'bytes */{size}')
                self.end_headers()
                return
        self.send_response(status)
        self.send_header('Content-Type',mimetypes.guess_type(file.name)[0] or 'application/octet-stream')
        self.send_header('Content-Length',str(end-start+1))
        self.send_header('Accept-Ranges','bytes')
        self.send_header('X-Content-Type-Options','nosniff')
        if status == 206:
            self.send_header('Content-Range',f'bytes {start}-{end}/{size}')
        self.end_headers()
        with file.open('rb') as stream:
            stream.seek(start)
            remaining = end-start+1
            while remaining:
                chunk = stream.read(min(65536,remaining))
                if not chunk:
                    break
                self.wfile.write(chunk)
                remaining -= len(chunk)

    def do_POST(self):
        if not valid_origin(self.headers.get('Host',''),self.headers.get('Origin'),self.server.server_port):
            return self.json_response({'error':'Origem não permitida.'},403)
        if self.headers.get('Sec-Fetch-Site') == 'cross-site':
            return self.json_response({'error':'Origem não permitida.'},403)
        route = [unquote(p) for p in urlsplit(self.path).path.strip('/').split('/')]
        try:
            if len(route) == 4 and route[:2] == ['api','lessons']:
                method = {'start':self.server.studio.start,'finish':self.server.studio.finish,'retry-sync':self.server.studio.retry,'requeue':self.server.studio.requeue}.get(route[3])
                if method:
                    return self.json_response(method(route[2]))
            if len(route) == 4 and route[:2] == ['api','examples'] and route[3] == 'open':
                return self.json_response(self.server.studio.open_example(route[2]))
            return self.json_response({'error':'Ação não encontrada.'},404)
        except ValueError as error:
            self.json_response({'error':str(error)},409)
        except Exception:
            self.json_response({'error':'Não foi possível concluir a ação. Seu progresso salvo foi preservado.'},500)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port',type=int,default=int(os.environ.get('STUDIO_PORT','8765')))
    args = parser.parse_args()
    studio = Studio()
    server = ThreadingHTTPServer(('127.0.0.1',args.port),Handler)
    server.studio = studio
    stop = threading.Event()
    def worker():
        while not stop.is_set():
            studio.sync_due()
            stop.wait(1)
    threading.Thread(target=worker,daemon=True).start()
    print(f'Estúdio disponível: http://127.0.0.1:{args.port}',flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        stop.set()
        server.server_close()

if __name__ == '__main__':
    main()
