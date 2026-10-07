#!/usr/bin/env bash
set -euo pipefail

cd -- "$(dirname -- "$0")"

case "${1:-DemoEmail}" in
    ok|DemoEmail) demos=(DemoEmail) ;;
    acoplamento|DemoAcoplamento) demos=(DemoAcoplamento) ;;
    desacoplamento|DemoDesacoplamento) demos=(DemoDesacoplamento) ;;
    whatsapp|DemoWhatsApp) demos=(DemoWhatsApp) ;;
    pendente|DemoPagamentoPendente) demos=(DemoPagamentoPendente) ;;
    falha) demos=(DemoAcoplamento DemoDesacoplamento) ;;
    *)
        echo "Use: DemoEmail | DemoAcoplamento | DemoDesacoplamento | DemoWhatsApp | DemoPagamentoPendente" >&2
        exit 1
        ;;
esac

mkdir -p pratica/out
javac -encoding UTF-8 -d pratica/out pratica/*.java
for demo in "${demos[@]}"; do
    java -cp pratica/out "$demo"
done
