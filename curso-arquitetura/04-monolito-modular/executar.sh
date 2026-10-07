#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
case "${1:-modulos}" in
  modulos)
    mkdir -p pratica/out
    javac -encoding UTF-8 -d pratica/out pratica/financeiro/*.java pratica/academico/*.java pratica/DemoModulos.java
    java -cp pratica/out DemoModulos ;;
  *) echo 'Use: bash executar.sh modulos' >&2; exit 1 ;;
esac
