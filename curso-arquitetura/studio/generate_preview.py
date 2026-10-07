#!/usr/bin/env python3
"""Generate read-only file:// QA artifact from actual studio manifests."""
import json
from pathlib import Path
from server import Studio
root = Path(__file__).resolve().parent
state = Studio(root).state()
for lesson in state['lessons']:
    if lesson.get('audioUrl'):
        lesson['audioUrl'] = (root / lesson['audioUrl'].lstrip('/')).as_uri()
html = (root/'public/index.html').read_text()
css = (root/'public/style.css').read_text()
js = (root/'public/app.js').read_text()
# File URLs are permitted solely in this local QA artifact, never in production.
js = js.replace("['http:','https:'].includes(parsed.protocol)","['http:','https:','file:'].includes(parsed.protocol)")
payload=json.dumps(state,ensure_ascii=False).replace('</','<\\/')
mock=f'''<script>
window.fetch = async (path, options = {{}}) => {{
  if ((options.method || 'GET') !== 'GET') return new Response(JSON.stringify({{error:'Prévia somente para revisão. Inicie o estúdio para gravar, abrir exemplos ou sincronizar o Pora.'}}), {{status:503}});
  if (path === '/api/state') return new Response(JSON.stringify({payload}), {{status:200}});
  return new Response('{{}}', {{status:404}});
}};
</script>'''
html=html.replace('<link rel="stylesheet" href="/style.css">',f'<style>{css}</style>')
html=html.replace('<main>','<div style="padding:10px;text-align:center;background:#efe0b9;color:#6d542d;font-size:12px">PRÉVIA SOMENTE PARA REVISÃO · Os botões de gravação e abertura de exemplos estão indisponíveis.</div><main>')
html=html.replace('<script src="/app.js"></script>',mock+'<script>'+js.replace('</script>','<\\/script>')+'</script>')
(root/'preview.html').write_text(html)
print(root/'preview.html')
