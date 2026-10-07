#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
case "${1:-DemoEntregaDuplicada}" in
  DemoEntregaDuplicada|DemoConsumidorIdempotente) demo="${1:-DemoEntregaDuplicada}" ;;
  *) echo 'Use: bash executar.sh DemoEntregaDuplicada | DemoConsumidorIdempotente' >&2; exit 1 ;;
esac
mkdir -p pratica/out
javac -encoding UTF-8 -d pratica/out pratica/*.java
java -cp pratica/out "$demo"
