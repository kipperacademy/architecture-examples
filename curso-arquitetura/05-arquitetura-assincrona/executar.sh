#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
case "${1:-DemoEventoPerdido}" in
  DemoEventoPerdido|DemoOutbox|DemoEntregaDuplicada|DemoConsumidorIdempotente) demo="${1:-DemoEventoPerdido}" ;;
  *) echo 'Use: DemoEventoPerdido | DemoOutbox | DemoEntregaDuplicada | DemoConsumidorIdempotente ' >&2; exit 1 ;;
esac
mkdir -p pratica/out
javac -encoding UTF-8 -d pratica/out pratica/*.java
java -cp pratica/out "$demo"
