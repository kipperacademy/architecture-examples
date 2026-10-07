# Arquitetura Assíncrona

Java 21+. Fila, outbox e deduplicação são modelos em memória; não são duráveis nem concorrentes.

Partindo da **pasta do curso**:

```sh
bash 08-arquitetura-assincrona/executar.sh DemoEventoPerdido
bash 08-arquitetura-assincrona/executar.sh DemoOutbox
bash 08-arquitetura-assincrona/executar.sh DemoEntregaDuplicada
bash 08-arquitetura-assincrona/executar.sh DemoConsumidorIdempotente
```

Cada comando compila antes de executar. Veja `roteiro.md` para ordem, previsões e causas dos resultados. `teoria.excalidraw` contém os diagramas editáveis. Links e estado da revisão estão em `../planejamento/estado-do-curso.md`.

## Excalidraw ao vivo

https://app.excalidraw.com/s/5pZP9SZcJC3/2niqhnTrKS1
