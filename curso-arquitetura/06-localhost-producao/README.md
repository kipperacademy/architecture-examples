# Do localhost à produção

Java 21+. Docker é necessário apenas para o bloco de containers; esse bloco ainda não foi executado.

Partindo da **pasta do curso**:

```sh
INSTANCE=A PORT=8080 bash 05-localhost-producao/executar.sh
# Em outro terminal:
curl http://127.0.0.1:8080/curso
```

Cada comando compila antes de executar. Pare o servidor com Ctrl+C. Veja `roteiro.md` para ordem, previsões e causas dos resultados. `teoria.excalidraw` contém os diagramas editáveis. Links e estado da revisão estão em `../planejamento/estado-do-curso.md`.

## Excalidraw ao vivo

https://app.excalidraw.com/s/5pZP9SZcJC3/9nrf5Mfc7JU
