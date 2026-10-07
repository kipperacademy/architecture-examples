# Matrículas — Clean Architecture

Versão independente, Java puro. Requer JDK 17+. Clean Architecture aqui organiza políticas de negócio e detalhes em círculos/camadas conceituais; as dependências de código apontam para dentro.

```sh
./executar.sh
```

O cenário executa três tentativas de pagamento pelo adaptador AppMax simulado: Ana é confirmada e matriculada; Bia fica pendente; Clara é recusada. Só a primeira matrícula é persistida.

## Caminho da dependência

```text
Main (montagem) → EnrollStudent → contratos internos
                         ↑               ↑
                  domínio      AppMaxAdapter / InMemoryEnrollmentRepository
```

O caso de uso define o que precisa de pagamento e persistência. O adaptador conhece o protocolo fictício da AppMax e traduz seus estados. O domínio não importa classes de pagamento externo.

## Pastas

- `domain/`: estado e regra da matrícula.
- `application/`: caso de uso e contratos internos que ele necessita.
- `adapters/`: detalhes de AppMax simulado, repositório em memória e entrada de console.
- `bootstrap/`: composição explícita das implementações.

## Limite da demo

`AppMaxApiSimulator` não chama a API real. Os rótulos de demonstração `paid`, `pending` e `refused` são inventados para tornar visível a tradução; eles não pretendem reproduzir os estados oficiais da AppMax. A integração real requer fluxo de credenciais/merchant, criação de cliente e pedido, escolha do meio de pagamento, tokenização quando aplicável e tratamento de respostas/webhooks conforme a API e a configuração da conta. Não envie dados de cartão a esta aplicação.

## Fontes

- Robert C. Martin, [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html).
- Aula 03 no repositório do curso: `curso-arquitetura/03-clean-architecture-hexagonal/roteiro.md`.
- Appmax, [Quickstart](https://docs.appmax.com.br/quickstart) e [referência da API](https://docs.appmax.com.br/).
