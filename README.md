# Matrículas em Java: Clean Architecture e Hexagonal

Dois projetos independentes, sem framework, para comparar a organização por políticas/camadas e por portas/adaptadores. Ambos usam a mesma regra: **só uma cobrança confirmada libera a matrícula**.

## Projetos

- [`clean-architecture/`](clean-architecture/README.md): domínio e caso de uso no núcleo; portas de saída definidas pela aplicação; adaptadores externos e montagem na borda.
- [`hexagonal/`](hexagonal/README.md): portas de entrada e saída explícitas; adaptadores de console, AppMax simulado e repositório.

Cada pasta é um projeto separado e pode ser compilada/executada sem Maven, Gradle, Spring ou dependências externas. Requer JDK 17+.

```sh
cd clean-architecture && ./executar.sh
cd ../hexagonal && ./executar.sh
```

O adaptador AppMax é uma simulação local. Não envia cobranças nem implementa autenticação ou chamadas HTTP reais. Ele demonstra a fronteira e o mapeamento entre estados externos e internos.

## De onde veio o exemplo

A transcrição integral do encontro de 29/09 promete exemplos de código de Clean Architecture e Hexagonal “sem usar o Spring, fazendo na mão mesmo” e descreve o contrato `PaymentProvider` com `charge`, definido pela aplicação e implementado por diferentes fornecedores. Também usa matrícula e cobrança para explicar que a matrícula precisa conhecer somente o estado de pagamento, sem depender dos campos ou do SDK do provedor.

O material da Aula 03 usa Ana (confirmada), Bia (pendente) e Clara (confirmada) e apresenta matrícula como uma regra única. A Aula 02 demonstra o contrato interno de pagamento em centavos e um Adapter que traduz para uma API externa. AppMax não aparece nessas aulas: esta pasta a usa como o fornecedor solicitado agora, numa implementação simulada.

## Referências arquiteturais

- Robert C. Martin, [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html): políticas no núcleo e regra de dependência apontando para dentro.
- Martin Fowler e Badri Janakiraman, [Badri on Hexagonal Rails](https://martinfowler.com/articles/badri-hexagonal/): núcleo isolado de integrações externas, com escolhas proporcionais às necessidades reais.
- Martin Fowler, [Dependency Composition](https://martinfowler.com/articles/dependency-composition.html): composição de dependências e fronteiras numa aplicação concreta.
- Alistair Cockburn, [Hexagonal Architecture / Ports and Adapters](https://alistair.cockburn.us/hexagonal-architecture): portas como conversas da aplicação e adaptadores como tradução entre tecnologia e essas conversas.
- Appmax, [Quickstart da API](https://docs.appmax.com.br/quickstart): fluxo real de autenticação, cliente, pedido e pagamento. Não é implementado nestas demos.
