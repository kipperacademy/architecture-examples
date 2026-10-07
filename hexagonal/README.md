# Matrículas — Arquitetura Hexagonal

Versão independente, Java puro. Requer JDK 17+. O núcleo conversa com o exterior por portas; adaptadores de entrada e saída convertem entre essas conversas e cada tecnologia.

```sh
./executar.sh
```

A demo usa os mesmos pedidos e respostas simuladas da versão Clean: Ana confirmada, Bia pendente e Clara recusada. Só Ana recebe matrícula.

## Portas e adaptadores

```text
ConsoleEnrollmentAdapter ──> EnrollStudent (porta de entrada)
                                  │
                    ┌─────────────┴──────────────┐
                    v                            v
           PaymentProvider              EnrollmentRepository
                    ^                            ^
          AppMaxPaymentAdapter     InMemoryEnrollmentRepository
```

`EnrollStudent` implementa a porta de entrada, chamada pelo adaptador de console. As portas de saída descrevem o que o núcleo precisa. AppMax e armazenamento implementam essas conversas; a composição fica no `Main`.

## Pastas

- `domain/`: conceitos e regra de matrícula.
- `application/ports/in/`: capacidade que a aplicação oferece.
- `application/ports/out/`: necessidades que a aplicação solicita ao exterior.
- `application/service/`: implementação do caso de uso.
- `adapters/in/` e `adapters/out/`: tradução de/para o exterior.
- `Main.java`: composição explícita dos adaptadores e serviços.

## Limite da demo

`AppMaxApiSimulator` não chama a API real. Os rótulos de demonstração `paid`, `pending` e `refused` são inventados para mostrar como o adaptador traduz respostas externas para `CONFIRMED`, `PENDING` e `DECLINED`; eles não pretendem reproduzir os estados oficiais da AppMax. A API real tem fluxo de autenticação, cliente, pedido e pagamento; detalhes de tokenização e meios de pagamento não cabem neste exemplo. Não envie dados de cartão a esta aplicação.

## Fontes

- Alistair Cockburn, [Hexagonal Architecture / Ports and Adapters](https://alistair.cockburn.us/hexagonal-architecture).
- Martin Fowler e Badri Janakiraman, [Badri on Hexagonal Rails](https://martinfowler.com/articles/badri-hexagonal/).
- Aula 03 no repositório do curso: `curso-arquitetura/03-clean-architecture-hexagonal/roteiro.md`.
