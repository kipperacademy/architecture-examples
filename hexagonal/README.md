# Matrículas — Arquitetura Hexagonal

Versão independente em Java 17+ da arquitetura Ports & Adapters de Alistair Cockburn. O núcleo da aplicação define **ports** conforme as conversas que precisa oferecer ou solicitar. **Primary adapters** acionam a aplicação; **secondary adapters** são acionados por ela para falar com pagamentos ou persistência. A persistência usa JPA com Hibernate e H2 em arquivo, sem Spring. As entidades JPA ficam no lado secondary.

```sh
./executar.sh
```

A execução requer Maven 3.9+ e JDK 17+. O script compila e inicia a aplicação com `mvn compile exec:java`. Por padrão, o banco H2 em arquivo fica em `data/enrollments.mv.db` (relativo a esta pasta). Para escolher outro URL JDBC H2, configure `ENROLLMENT_DB_URL`, por exemplo `ENROLLMENT_DB_URL='jdbc:h2:file:/tmp/turma;DB_CLOSE_ON_EXIT=FALSE' ./executar.sh`.

A demo usa os mesmos pedidos e respostas simuladas da versão Clean: Ana confirmada, Bia pendente e Clara recusada. Só Ana recebe matrícula. Rodar novamente atualiza a matrícula de Ana pela chave estável `enr-ana`; Bia e Clara não são gravadas.

## Ports e adapters: primary e secondary

```text
ConsoleEnrollmentAdapter ──> EnrollStudent (primary port)
                                  │
                    ┌─────────────┴──────────────┐
                    v                            v
        PixPaymentProvider (secondary)   EnrollmentRepository (secondary)
                    ^                            ^
       AppMaxPixPaymentAdapter       JpaEnrollmentRepository
```

`EnrollStudent` é uma primary port: descreve uma capacidade pela qual um ator pode acionar o núcleo. `PixPaymentProvider` e `EnrollmentRepository` são secondary ports: descrevem conversas que a aplicação precisa com atores externos. O console implementa um primary adapter; AppMax e JPA/H2 implementam secondary adapters. `InMemoryEnrollmentRepository` é outro secondary adapter para demonstração, não usado pela composição padrão.

## Pastas

- `domain/`: conceitos e regra de matrícula no interior da aplicação.
- `application/ports/primary/`: conversas primárias pelas quais atores acionam a aplicação.
- `application/ports/secondary/`: conversas secundárias que a aplicação inicia com atores externos.
- `application/usecases/`: execução dos casos de uso no interior da aplicação.
- `adapters/primary/`: adapters que traduzem as entradas de atores para as primary ports.
- `adapters/secondary/`: adapters que traduzem as secondary ports para tecnologias externas.
- `adapters/secondary/persistence/`: entidades JPA, fora do domínio e dos casos de uso.
- `Main.java`: composição explícita dos adapters e do núcleo.
- `src/main/resources/META-INF/persistence.xml`: unidade JPA e entidades persistidas.
- `pom.xml`: Hibernate, H2 e configuração de build/execução.
- `AppMaxPixPaymentAdapter`: adapter HTTP de produção/sandbox, limitado a Pix.

## Persistência e pagamento

`JpaEnrollmentRepository` implementa a secondary port `EnrollmentRepository`; tipos JPA não chegam ao núcleo. O estado do pagamento e a matrícula são confirmados na mesma transação JPA. A configuração H2 usa `hibernate.hbm2ddl.auto=update` para a demo; não é uma estratégia de migração de produção.

### Pix real AppMax

O modo padrão (`./executar.sh` ou `./executar.sh demo`) continua usando o simulador local. O caminho real é explícito e aceita somente Pix; não há campos, endpoints ou tokenização de cartão.

Configure as credenciais **do merchant** (não as credenciais do app) no ambiente, sem gravá-las no projeto:

```sh
export APP_MAX_CLIENT_ID='...'
export APP_MAX_CLIENT_SECRET='...'
# Opcional: o padrão é sandbox; use os dois domínios oficiais de produção juntos ao operar em produção.
export APP_MAX_API_BASE_URL='https://api.sandboxappmax.com.br'
export APP_MAX_AUTH_BASE_URL='https://auth.sandboxappmax.com.br'
./executar.sh pix-create
```

O comando solicita os dados do comprador, os dados do estudante/curso e o preço em centavos. Nome, sobrenome, email, telefone e IP são enviados ao endpoint de cliente; o IP deve ser coletado no checkout/Appmax JS. CPF/CNPJ é enviado no cliente e no pagamento Pix. O adapter cria cliente, pedido digital e pagamento Pix, então salva o pedido AppMax, estado e instruções EMV/QR no H2 como pendente. O exemplo precisa de dados completos do comprador e não persiste email/telefone/documento/IP localmente.

Depois que o Pix for pago, consulte o estado pela API autenticada e promova a matrícula:

```sh
./executar.sh pix-check <id-interno-da-matricula>
```

Cada consulta chama `GET /v1/orders/{order_id}`. O serviço só grava matrícula quando a resposta autenticada retorna `aprovado` ou `integrado` **e** `total_paid` corresponde exatamente ao valor persistido em centavos; status sem valor pago ou com valor divergente não libera acesso. `pendente`, `pendente_integracao` e estados desconhecidos também não liberam acesso. A atualização do pagamento e a criação da matrícula ocorrem na mesma transação JPA; repetir a confirmação não duplica a matrícula.

O projeto não usa webhook para confirmar. A documentação pública descreve os eventos e payloads, mas não documenta assinatura HMAC ou autenticação que prove a origem do POST; portanto, um payload recebido não serve como autoridade para liberar matrícula. Um webhook futuro pode apenas disparar a consulta autenticada do pedido.

## Limite da demo

`AppMaxApiSimulator` não chama a API real. Os rótulos de demonstração `paid`, `pending` e `refused` são inventados para mostrar como o adaptador traduz respostas externas para `CONFIRMED`, `PENDING` e `DECLINED`; eles não pretendem reproduzir os estados oficiais da AppMax. O adapter HTTP Pix usa OAuth merchant e os endpoints reais descritos na documentação oficial. Não envie dados de cartão a esta aplicação.

## Fontes

- Alistair Cockburn, [Hexagonal Architecture / Ports and Adapters](https://alistair.cockburn.us/hexagonal-architecture).
- Martin Fowler e Badri Janakiraman, [Badri on Hexagonal Rails](https://martinfowler.com/articles/badri-hexagonal/).
- Appmax, [autenticação](https://docs.appmax.com.br/guides/autenticacao), [exemplo completo (Pix e GET do pedido)](https://docs.appmax.com.br/guides/exemplo-integracao), [status dos pedidos](https://docs.appmax.com.br/guides/status-pedidos) e [webhooks](https://docs.appmax.com.br/guides/webhooks).
- Aula 03 no repositório do curso: `curso-arquitetura/03-clean-architecture-hexagonal/roteiro.md`.
