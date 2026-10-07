# Decisões didáticas a partir da aula ao vivo

Fonte: transcrição verbatim do Granola, encontro “Encontro ao Vivo 🎧” de 29/09/2026: https://notes.granola.ai/d/0ca4eb81-036d-463c-8247-3f2c7a89ddac. O retorno MCP não contém timestamps; os trechos abaixo preservam a formulação transcrita e a atribuição de voz “Microphone”.

## O que foi prometido e ensinado

- “Mas a gente vai ter uma aula que vai ser específica disso, de Clean Arch e arquitetura hexagonal. E eu vou trazer muito código sem usar o Spring, fazendo na mão mesmo”. Isso orienta projetos Java sem framework e com composição explícita.
- “Então eu vou trazer exemplo da CleanArc e da arquitetura hexagonal para deixar muito claro como é. Vou trazer o código do MPEG-8 para a gente destrinchar”. A transcrição reconhece literalmente “MPEG-8”; não há contexto suficiente para corrigir essa sigla com segurança. A promessa verificável é trazer código para explicar as duas arquiteturas.
- “Então eu posso ter aqui lá no meu servidor uma única interface que eu vou chamar de PaymentProvider. [...] PaymentProvider vai ter um método chamado charge.” Uma implementação do fornecedor deve respeitar esse contrato; o fluxo externo usa a abstração sem conhecer os detalhes daquela implementação.
- “Então aqui o meu acoplamento de matrícula para cobrança deveria ser somente com o status da cobrança. [...] Cobrança confirmada, matrícula libera. Cobrança pendente, matrícula bloqueada.” O núcleo traduz estados externos para estados internos e não acessa campos da entidade/SDK de pagamento.
- AppMax não é nomeada na transcrição. O pedido escolheu AppMax como exemplo: há um simulador local para a aula e adapters HTTP Pix baseados na API oficial, configuráveis com credenciais do merchant no ambiente. Não foi feita chamada real sem credenciais.

## Como isso aparece nos projetos

| Evidência da aula/material | Decisão nesta pasta |
|---|---|
| Sem Spring; código “na mão” | Java puro, interfaces, construtores e `main` como ponto de composição |
| `PaymentProvider.charge` como contrato da aplicação | Mesma porta interna nas duas versões |
| Matrícula depende somente do status | Apenas `CONFIRMED` permite persistir a matrícula |
| Provider concreto isolado atrás de contrato | Adapters simulados e HTTP AppMax traduzem status externo para `PaymentStatus` interno |
| Aula 03: Ana e Clara confirmadas; Bia pendente; armazenamento intercambiável | JPA/Hibernate com H2 em arquivo persiste matrículas e tentativas Pix; os casos confirmados/pending preservam a mesma regra |
| Aula 02: Adapter traduz centavos e formato externo | Montagem demonstra adapter sem trazer SDK, segredo ou dados de cartão |

## Por que há dois desenhos

Os conceitos se sobrepõem, mas os exemplos agora usam os nomes próprios das fontes originais. Em `clean-architecture/`, os diretórios são `entities/`, `usecases/`, `interfaceadapters/` e `frameworksdrivers/`; a regra de dependência aponta para dentro. Em `hexagonal/`, o núcleo define primary/secondary ports e os adapters correspondentes são primary/secondary (driving/driven), seguindo Cockburn.

Esses exemplos continuam pequenos para fins de aula. O fluxo Pix real guarda a tentativa pendente e só matricula após consulta autenticada do pedido AppMax. A versão Clean usa webhooks como gatilhos e confirma estado pela API; a Hexagonal usa polling explícito. A confirmação e a matrícula são transacionais dentro do banco H2 por meio de JPA, mas a cobrança externa não participa dessa transação. Webhooks AppMax não têm HMAC ou token documentados, então o corpo recebido não é prova de pagamento.
