# Aula 03 — Clean Architecture e Hexagonal

Java 21 ou superior. No terminal:

```bash
cd /Users/fernanda/Desktop/kipperdev/curso-arquitetura/03-clean-architecture-hexagonal
bash executar.sh clean-memoria
bash executar.sh clean-arquivo
bash executar.sh hex-terminal Ana CONFIRMADO
bash executar.sh hex-terminal Bia PENDENTE
bash executar.sh hex-csv
```

O script compila antes de executar e também aceita seu caminho completo, a partir de qualquer pasta.

- Demos: `pratica/demos/` (um exemplo por arquivo).
- Entrada do lote: `dados/pedidos.csv` (nome;pagamento, sem cabeçalho).
- Saída persistida: `dados/matriculas.txt`, criada pela demo de arquivo.
- Roteiro: `roteiro.md`. Slides: `teoria.excalidraw` ou [Excalidraw online](https://app.excalidraw.com/s/5pZP9SZcJC3/9nu1j8fbpQ3).
- Áudio: `preparacao-para-gravar.mp3` (3min42s), versão 1; não acompanha a introdução conceitual dos slides revisados.

Resultado esperado com os dados originais: Ana e Clara matriculadas; Bia pendente. A memória começa vazia a cada instância; o arquivo preserva matrículas entre execuções. Para recomeçar, apague somente `dados/matriculas.txt`, se existir.
