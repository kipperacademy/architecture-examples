#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
case "${1:-DemoRetry}" in
  DemoRetry|DemoIdempotencia) demo="${1:-DemoRetry}" ;;
  *) echo 'Use: DemoRetry | DemoIdempotencia ' >&2; exit 1 ;;
esac
mkdir -p pratica/out
javac -encoding UTF-8 -d pratica/out pratica/*.java
java -cp pratica/out "$demo"
