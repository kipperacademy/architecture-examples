#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
mkdir -p pratica/out
javac -encoding UTF-8 -d pratica/out pratica/Servidor.java
exec java -cp pratica/out Servidor
