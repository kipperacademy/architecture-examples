#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
case "${1:-DemoSemCache}" in
  DemoSemCache|DemoCache|DemoEstadoLocal|DemoEstadoCompartilhado|DemoLimite) demo="${1:-DemoSemCache}" ;;
  *) echo 'Use: DemoSemCache | DemoCache | DemoEstadoLocal | DemoEstadoCompartilhado | DemoLimite ' >&2; exit 1 ;;
esac
mkdir -p pratica/out
javac -encoding UTF-8 -d pratica/out pratica/*.java
java -cp pratica/out "$demo"
