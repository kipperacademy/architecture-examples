#!/bin/zsh
cd "${0:A:h}"
mkdir -p runtime
port="${STUDIO_PORT:-8765}"
health=$(/usr/bin/curl -fsS "http://127.0.0.1:${port}/api/health" 2>/dev/null)
if [[ -n "$health" ]]; then
  if print -r -- "$health" | python3 -c 'import json,sys,pathlib; data=json.load(sys.stdin); sys.exit(0 if data.get("app")=="kipperdev-architecture-studio" and data.get("workspace")==str(pathlib.Path.cwd().resolve()) else 1)' 2>/dev/null; then
    /usr/bin/open "http://127.0.0.1:${port}"
    exit 0
  fi
  print "A porta ${port} está ocupada por outro serviço. Execute STUDIO_PORT=8766 ./start.command"
  exit 1
fi
nohup python3 server.py --port "$port" < /dev/null > runtime/server.log 2>&1 &
server_pid=$!
for attempt in {1..30}; do
  health=$(/usr/bin/curl -fsS "http://127.0.0.1:${port}/api/health" 2>/dev/null)
  if print -r -- "$health" | python3 -c 'import json,sys,pathlib; data=json.load(sys.stdin); sys.exit(0 if data.get("app")=="kipperdev-architecture-studio" and data.get("workspace")==str(pathlib.Path.cwd().resolve()) else 1)' 2>/dev/null; then
    /usr/bin/open "http://127.0.0.1:${port}"
    print "Estúdio iniciado. Log: ${PWD}/runtime/server.log"
    exit 0
  fi
  if ! kill -0 "$server_pid" 2>/dev/null; then
    print "Não foi possível iniciar o estúdio. Veja ${PWD}/runtime/server.log"
    exit 1
  fi
  sleep 0.2
done
print "O estúdio ainda está iniciando. Log: ${PWD}/runtime/server.log"
