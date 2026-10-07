#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

case "${1:-}" in
  clean-memoria) demo=DemoCleanMemoria ;;
  clean-arquivo) demo=DemoCleanArquivo ;;
  hex-terminal) demo=DemoHexagonalTerminal ;;
  hex-csv) demo=DemoHexagonalCsv ;;
  *) echo 'Use: bash executar.sh clean-memoria|clean-arquivo|hex-terminal|hex-csv [nome pagamento]'; exit 1 ;;
esac
shift
mkdir -p pratica/out
fontes=()
while IFS= read -r -d '' fonte; do fontes+=("$fonte"); done < <(find pratica -name '*.java' -print0)
javac -encoding UTF-8 -d pratica/out "${fontes[@]}"
java -cp pratica/out "demos.$demo" "$@"
