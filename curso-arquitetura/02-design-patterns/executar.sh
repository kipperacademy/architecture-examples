#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

case "${1:-compra}" in
  compra|DemoCompra) demo=DemoCompra ;;
  sem-adapter|DemoSemAdapter) demo=DemoSemAdapter ;;
  sem-desconto|DemoSemDesconto) demo=DemoSemDesconto ;;
  outro-fornecedor|DemoOutroFornecedor) demo=DemoOutroFornecedor ;;
  singleton|DemoSingleton) demo=DemoSingleton ;;
  *) echo 'Use: bash executar.sh compra|sem-adapter|sem-desconto|outro-fornecedor|singleton'; exit 1 ;;
esac
mkdir -p pratica/out
javac -encoding UTF-8 -d pratica/out pratica/*.java
java -cp pratica/out "$demo"
