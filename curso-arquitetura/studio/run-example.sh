#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "$0")/.." && pwd)"
MANIFEST="$ROOT/studio/examples.json"
ID="${1:-}"
if [[ -z "$ID" ]]; then
  echo 'Uso: ./studio/run-example.sh <id-do-exemplo>' >&2
  exit 2
fi

read -r KIND SOURCE_DIR MAIN_CLASS < <(python3 - "$MANIFEST" "$ID" <<'PY'
import json, sys
item = next((x for x in json.load(open(sys.argv[1], encoding="utf-8")) if x["id"] == sys.argv[2]), None)
if item is None: raise SystemExit(2)
print(item["kind"], item["path"], item["mainClass"] or "")
PY
)
WORK="$ROOT/studio/runtime/$ID"
mkdir -p "$WORK"

case "$KIND" in
  java|compile-only)
    CLASSES="$WORK/classes"
    mkdir -p "$CLASSES"
    SOURCES=()
    while IFS= read -r -d '' SOURCE; do SOURCES+=("$SOURCE"); done < <(find "$SOURCE_DIR" -name '*.java' -print0)
    javac -encoding UTF-8 -d "$CLASSES" "${SOURCES[@]}"
    if [[ "$KIND" == java ]]; then
      case "$ID" in
        aula-03-hex-terminal) java -cp "$CLASSES" "demos.$MAIN_CLASS" Ana CONFIRMADO ;;
        aula-03-hex-csv) mkdir -p "$WORK/dados"; cp "$ROOT/studio/fixtures/pedidos.csv" "$WORK/dados/pedidos.csv"; (cd "$WORK" && java -cp "$CLASSES" "demos.$MAIN_CLASS") ;;
        aula-03-clean-memoria) java -cp "$CLASSES" "demos.$MAIN_CLASS" ;;
        aula-03-clean-arquivo) (cd "$WORK" && java -cp "$CLASSES" "demos.$MAIN_CLASS") ;;
        *) java -cp "$CLASSES" "${MAIN_CLASS}" ;;
      esac
    else
      echo "Fontes compilados. A demonstração HTTP não foi iniciada pelo runner."
    fi
    ;;
  python-sql)
    (cd "$WORK" && python3 "$SOURCE_DIR/executar.py" "$ROOT/studio/fixtures/sql/estrutura.sql")
    ;;
  *) echo "Tipo de exemplo desconhecido: $KIND" >&2; exit 2 ;;
esac
