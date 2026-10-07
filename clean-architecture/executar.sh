#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
exec mvn -q compile exec:java "$@"
