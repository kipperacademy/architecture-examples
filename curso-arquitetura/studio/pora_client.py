"""Small authenticated MCP transport. Credentials never leave this module."""
import json
from pathlib import Path
import urllib.request
import urllib.error
import tomllib

class PoraClient:
    def __init__(self, config_path=None):
        self.config_path = Path(config_path or Path.home() / '.codex/config.toml')
        self.session = None
        self.counter = 0

    def rpc(self, method, params=None, notification=False):
        with self.config_path.open('rb') as file:
            config = tomllib.load(file)['mcp_servers']['pora']
        self.counter += 1
        body = {'jsonrpc': '2.0', 'method': method}
        if not notification:
            body['id'] = self.counter
        if params is not None:
            body['params'] = params
        headers = dict(config.get('http_headers', {}))
        headers.update({'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream', 'MCP-Protocol-Version': '2024-11-05'})
        if self.session:
            headers['Mcp-Session-Id'] = self.session
        req = urllib.request.Request(config['url'], data=json.dumps(body).encode(), headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=35) as response:
                self.session = response.headers.get('Mcp-Session-Id', self.session)
                raw = response.read().decode()
        except urllib.error.HTTPError as error:
            if error.code == 404:
                self.session = None
            raise RuntimeError('Não foi possível comunicar com o Pora; uma nova tentativa poderá reiniciar a sessão.') from None
        if not raw.strip():
            return {}
        if raw.lstrip().startswith('data:') or '\ndata:' in raw:
            messages = []
            for line in raw.splitlines():
                if line.startswith('data:'):
                    try:
                        messages.append(json.loads(line[5:].strip()))
                    except json.JSONDecodeError:
                        continue
            result = next((item for item in reversed(messages) if item.get('id') == body.get('id')), {})
        else:
            result = json.loads(raw)
        if 'error' in result:
            raise RuntimeError('O Pora recusou a solicitação MCP.')
        return result.get('result', result)

    def initialize(self):
        if not self.session:
            self.rpc('initialize', {'protocolVersion': '2024-11-05', 'capabilities': {}, 'clientInfo': {'name': 'kipperdev-studio', 'version': '1.0'}})
            self.rpc('notifications/initialized', notification=True)

    def call(self, name, arguments):
        self.initialize()
        result = self.rpc('tools/call', {'name': name, 'arguments': arguments})
        if result.get('isError'):
            raise RuntimeError('A ferramenta do Pora não concluiu a solicitação.')
        if 'structuredContent' in result:
            return result['structuredContent']
        values = []
        for block in result.get('content', []):
            if block.get('type') == 'text':
                try:
                    values.append(json.loads(block['text']))
                except (json.JSONDecodeError, KeyError):
                    pass
        return values[0] if len(values) == 1 else values or result

    def move_to_editing(self, content_id, target):
        self.call('update_content', {'contentId': content_id, 'status': target})
        contents = self.call('list_contents', {'creator': 'Fernanda Kipper | Dev', 'type': 'YOUTUBE', 'from': '2026-10-01', 'to': '2026-12-01'})
        def matches(value):
            if isinstance(value, dict):
                identity = value.get('id', value.get('contentId', value.get('content_id')))
                status = value.get('status')
                if isinstance(status, dict):
                    status = status.get('name', status.get('title'))
                if str(identity) == str(content_id) and status == target:
                    return True
                return any(matches(child) for child in value.values())
            if isinstance(value, list):
                return any(matches(child) for child in value)
            return False
        if not matches(contents):
            raise RuntimeError('O Pora ainda não confirmou a etapa de edição.')
        return True
