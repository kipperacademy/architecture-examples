# Curso de arquitetura

Para a gravação de 07/10, abra **[Abrir estúdio.command](Abrir%20estúdio.command)** com dois cliques no Finder. O sistema abre a fila local no navegador. Requer Python 3.11+; demos Java requerem JDK 21+.

No estúdio: selecione a aula, ouça o resumo, confira os pontos e abra o Excalidraw/código. Use **Iniciar gravação** e, quando terminar, **Concluir gravação**. A conclusão é salva localmente e enviada à coluna **Edição** no Pora, com confirmação e novas tentativas automáticas.

Os botões de código abrem somente a pasta do exemplo em uma nova janela. Em `exemplos-para-gravar/`, cada pasta contém apenas fontes; roteiros, áudio, compilação e dados de execução ficam fora dela. Para executar use `studio/run-example.sh ID` a partir desta pasta, ou o comando individual registrado em `studio/examples.json`.

[Instruções do estúdio](studio/README.md) · [Auditoria da preparação](planejamento/estado-do-curso.md)

## Material de autoria

Cada aula tem sua própria pasta. Os comandos abaixo usam o material original, preservado; para apresentar ao aluno use os exemplos isolados pelo estúdio.

## Aula 01 — SOLID, acoplamento e coesão

Nesta pasta, cada comando compila e executa uma demo independente:

```sh
bash 01-solid-acoplamento-coesao/executar.sh DemoEmail
bash 01-solid-acoplamento-coesao/executar.sh DemoAcoplamento
bash 01-solid-acoplamento-coesao/executar.sh DemoDesacoplamento
bash 01-solid-acoplamento-coesao/executar.sh DemoWhatsApp
bash 01-solid-acoplamento-coesao/executar.sh DemoPagamentoPendente
```

## Aula 02 — Design Patterns

Factory, Singleton, Strategy e Adapter: 5 minutos cada + 10 de prática integrada. DI na montagem.

```sh
bash 02-design-patterns/executar.sh sem-adapter
bash 02-design-patterns/executar.sh compra
bash 02-design-patterns/executar.sh sem-desconto
bash 02-design-patterns/executar.sh outro-fornecedor
bash 02-design-patterns/executar.sh singleton
```

## Aula 03 — Clean Architecture e Hexagonal

```sh
bash 03-clean-architecture-hexagonal/executar.sh clean-memoria
bash 03-clean-architecture-hexagonal/executar.sh clean-arquivo
bash 03-clean-architecture-hexagonal/executar.sh hex-terminal Ana CONFIRMADO
bash 03-clean-architecture-hexagonal/executar.sh hex-csv
```

Os áudios atualizados das oito aulas estão em `studio/audio/`, ligados diretamente ao player do estúdio.

## Continuação — aulas 04 a 08

Agenda do Pora, auditoria do material e links: [estado do curso](planejamento/estado-do-curso.md).

- [04 — Monólito Modular](04-monolito-modular/README.md)
- [05 — Do localhost à produção](05-localhost-producao/README.md)
- [06 — Sistemas Escaláveis](06-sistemas-escalaveis/README.md)
- [07 — Monólito vs Microserviços](07-monolito-vs-microservicos/README.md)
- [08 — Arquitetura Assíncrona](08-arquitetura-assincrona/README.md)

As oito aulas têm roteiro, slides no Excalidraw, exemplos isolados e áudio de preparação. As aulas 07–08 têm prazo editorial em novembro no Pora; a sessão de gravação reúne as oito em 07/10.
