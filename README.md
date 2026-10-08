# Matrículas em Java: Clean Architecture e Hexagonal

## Aula 05 — Do localhost à produção

O exemplo da Aula 05 é uma API simples em Node.js com `GET /cursos` e Dockerfile: [`05-localhost-producao/`](05-localhost-producao/README.md).

Dois projetos Java independentes e sem Spring, para comparar a organização por políticas/camadas e por portas/adaptadores. Ambos usam JPA com Hibernate e H2 em arquivo para persistir matrículas e pagamentos Pix pendentes. A regra é a mesma: **só uma cobrança confirmada libera a matrícula**.

## Projetos

- [`clean-architecture/`](clean-architecture/README.md): Entities, Use Cases, Interface Adapters, Frameworks & Drivers e regra de dependência para dentro.
- [`hexagonal/`](hexagonal/README.md): application core com primary/secondary ports e adapters, conforme Ports & Adapters de Cockburn.

Cada pasta pode ser compilada e executada sem Spring, com dependências externas gerenciadas por Maven. Requer JDK 17+ e Maven 3.9+.

```sh
cd clean-architecture && ./executar.sh
cd ../hexagonal && ./executar.sh
```

O simulador local continua como modo padrão. As duas pastas também contêm adapters HTTP para criar cobranças Pix na AppMax sandbox/produção com credenciais do merchant configuradas no ambiente. Em Clean Architecture, webhooks apenas disparam uma consulta autenticada ao pedido; em Hexagonal, `pix-check` faz essa consulta manualmente. Nenhuma versão aceita dados de cartão. Não há chamada real à AppMax configurada ou verificada neste workspace.

## Referências arquiteturais

- Robert C. Martin, [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html): Entities, Use Cases, Interface Adapters, Frameworks & Drivers e regra de dependência apontando para dentro.
- Martin Fowler e Badri Janakiraman, [Badri on Hexagonal Rails](https://martinfowler.com/articles/badri-hexagonal/): núcleo isolado de integrações externas, com escolhas proporcionais às necessidades reais.
- Martin Fowler, [Dependency Composition](https://martinfowler.com/articles/dependency-composition.html): composição de dependências e fronteiras numa aplicação concreta.
- Alistair Cockburn, [Hexagonal Architecture / Ports and Adapters](https://alistair.cockburn.us/hexagonal-architecture): primary/secondary ports e adapters, também chamados driving/driven.
- Appmax, [Quickstart da API](https://docs.appmax.com.br/quickstart), [Pix](https://docs.appmax.com.br/api-reference/payments/pix), [autenticação](https://docs.appmax.com.br/guides/autenticacao) e [webhooks](https://docs.appmax.com.br/guides/webhooks): fluxo usado pelos adapters HTTP.
