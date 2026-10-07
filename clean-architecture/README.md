# Matrículas — Clean Architecture

Aplicação Java 17+ com JPA/Hibernate e H2 em arquivo, organizada pelas quatro áreas nomeadas por Robert C. Martin: **Entities**, **Use Cases**, **Interface Adapters** e **Frameworks & Drivers**. Requer Maven 3.9+.

## Demonstração local

```sh
./executar.sh
```

Por padrão, a execução usa o simulador AppMax e grava em `./data/enrollments.mv.db` (H2). Ana é matriculada; Bia (pendente) e Clara (recusada) não são. A simulação é repetível e não acessa serviços externos.

Configure outro arquivo H2 com `DATABASE_URL='jdbc:h2:file:/caminho/enrollments;DB_CLOSE_ON_EXIT=FALSE'`. O Hibernate aplica o schema a partir das entidades JPA (`hibernate.hbm2ddl.auto=update`); não há scripts SQL de schema.

## AppMax HTTP com PIX

O modo HTTP é explícito e usa merchant credentials obtidas no processo de instalação do app. Credenciais do aplicativo não servem para criar clientes/pedidos/pagamentos. Nenhuma credencial fica no código.

Defina no ambiente:

```sh
APPMAX_MODE=http
APPMAX_ENV=sandbox                         # sandbox ou production
APPMAX_MERCHANT_CLIENT_ID=...
APPMAX_MERCHANT_CLIENT_SECRET=...
APPMAX_CUSTOMER_FIRST_NAME=...
APPMAX_CUSTOMER_LAST_NAME=...
APPMAX_CUSTOMER_EMAIL=...
APPMAX_CUSTOMER_PHONE=...
APPMAX_CUSTOMER_IP=...                    # valor obtido do Appmax JS no checkout
APPMAX_CUSTOMER_DOCUMENT_NUMBER=...       # CPF/CNPJ necessário para PIX
APPMAX_ENROLLMENT_ID=...
APPMAX_ENROLLMENT_STUDENT=...
APPMAX_ENROLLMENT_COURSE=...
APPMAX_ENROLLMENT_AMOUNT_CENTS=10000
APPMAX_WEBHOOK_PORT=8080
```

Também é possível definir `APPMAX_AUTH_BASE_URL` e `APPMAX_API_BASE_URL`; ambas precisam ser origens HTTPS. Sem override, sandbox seleciona `auth.sandboxappmax.com.br` e `api.sandboxappmax.com.br`; produção seleciona os domínios `auth.appmax.com.br` e `api.appmax.com.br`. Depois de configurar essas variáveis, execute `./executar.sh`. A aplicação solicita OAuth client credentials, cria cliente e pedido digital, gera PIX, persiste pedido pendente e imprime o EMV copia-e-cola, QR PNG em base64 e expiração.

O campo de IP deve vir do callback do Appmax JS no checkout web. Este exemplo Java de console recebe esse dado por variável de ambiente para mostrar a fronteira; não implementa o checkout de navegador que coleta o IP. Não envie PAN ou CVV a este backend: o fluxo implementado só cria PIX. O parser trata os campos PIX tanto sob `data.payment.pix_*` quanto sob `data.pix` (`emv_code`, `qr_code`, `expires_at`), que aparecem em páginas diferentes da documentação atual.

### Confirmação assíncrona

O modo HTTP inicia `POST /webhooks/appmax` e mantém um worker lendo a inbox persistente. O webhook aceita somente `order_approved`, `order_paid_by_pix` e `order_integrated` do tipo `order`; ele salva o payload e responde rapidamente. São aceitos os formatos `data.order.id` e `data.order_id` documentados nos exemplos/referência da AppMax. O worker consulta `GET /v1/orders/{order_id}` autenticado com Bearer e só libera matrícula se o pedido retornado tiver o mesmo ID, status `aprovado` ou `integrado` e `total_paid` igual ao valor esperado em centavos. `pendente`, `autorizado`, valor divergente e outros estados não liberam acesso. A inbox é deduplicada por evento+pedido, tem retry com intervalo e a confirmação/persistência é transacional no H2 via JPA.

A AppMax documenta que não envia assinatura HMAC nem token nos webhooks. Portanto o endpoint não inventa nem valida uma assinatura inexistente; o payload é somente um gatilho não confiável, e o status consultado pela API é a fonte de verdade. Publique-o somente atrás de HTTPS, configure a URL pública no app AppMax e habilite permissões dos eventos. O exemplo não implementa allowlist oficial de IP porque a documentação não fornece uma lista estável. Proteja a URL na borda de rede e monitore retries/falhas.

## Círculos da Clean Architecture

- `entities/`: entidades e regras gerais da matrícula, sem depender de UI, persistência ou AppMax.
- `usecases/`: regras específicas da aplicação. `PaymentProvider`, `EnrollmentRepository` e `PendingPaymentRepository` são abstrações internas que o caso de uso chama; as implementações concretas ficam no círculo externo.
- `interfaceadapters/controllers/`: controllers de console e webhook; convertem entradas externas para chamadas de caso de uso.
- `interfaceadapters/gateways/`: adapters que traduzem AppMax e persistência JPA/Hibernate para os contratos usados pelos casos de uso.
- `interfaceadapters/gateways/persistence/`: entidades ORM e mapeamento para matrícula, pagamento pendente, inbox de webhook e confirmação.
- `frameworksdrivers/`: `Main`, ponto de composição e configuração concreta de frameworks e ferramentas.
- `src/main/resources/META-INF/persistence.xml`: configuração do provedor JPA.

## Regra de dependência

O código fonte depende somente para dentro: Entities não conhece Use Cases; Use Cases depende de suas abstrações internas; Interface Adapters implementam essas abstrações e conhecem os detalhes externos; Frameworks & Drivers monta os componentes concretos. O sentido do fluxo em execução pode atravessar os círculos para fora, mas as dependências de código continuam apontando para as políticas internas. Esta é a regra que define a arquitetura; os nomes dos pacotes apenas espelham os círculos originais.

O simulador continua como padrão. H2 em arquivo mantém a demonstração independente e adequada a desenvolvimento; avalie banco gerenciado para produção. Para operação real, a AppMax exige merchant instalar/autorizar o app, configurar URL de webhook e conceder as permissões de evento. Valide sandbox e as credenciais/conta do merchant antes de usar produção. Não há cobrança AppMax real verificada neste exemplo.

## Build

```sh
mvn clean package
mvn exec:java
```

O projeto usa Hibernate ORM `7.4.12.Final`, H2 e Jackson como dependências Maven. A série Hibernate 7.4 declara suporte a Java 17 e Jakarta Persistence 3.2.

## Referências

- AppMax [Quickstart](https://docs.appmax.com.br/quickstart), [PIX](https://docs.appmax.com.br/api-reference/payments/pix), [Consultar pedido](https://docs.appmax.com.br/api-reference/orders/consultar-pedido), [Webhooks](https://docs.appmax.com.br/guides/webhooks), [Exemplo completo](https://docs.appmax.com.br/guides/exemplo-integracao), [Ambientes](https://docs.appmax.com.br/guides/ambientes), [Autenticação](https://docs.appmax.com.br/guides/autenticacao) e [Appmax JS](https://docs.appmax.com.br/guides/appmax-js).
- Robert C. Martin, [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html).
