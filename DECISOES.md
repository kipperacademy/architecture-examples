# Decisões didáticas a partir da aula ao vivo

Fonte: transcrição verbatim do Granola, encontro “Encontro ao Vivo 🎧” de 29/09/2026: https://notes.granola.ai/d/0ca4eb81-036d-463c-8247-3f2c7a89ddac. O retorno MCP não contém timestamps; os trechos abaixo preservam a formulação transcrita e a atribuição de voz “Microphone”.

## O que foi prometido e ensinado

- “Mas a gente vai ter uma aula que vai ser específica disso, de Clean Arch e arquitetura hexagonal. E eu vou trazer muito código sem usar o Spring, fazendo na mão mesmo”. Isso orienta projetos Java sem framework e com composição explícita.
- “Então eu vou trazer exemplo da CleanArc e da arquitetura hexagonal para deixar muito claro como é. Vou trazer o código do MPEG-8 para a gente destrinchar”. A transcrição reconhece literalmente “MPEG-8”; não há contexto suficiente para corrigir essa sigla com segurança. A promessa verificável é trazer código para explicar as duas arquiteturas.
- “Então eu posso ter aqui lá no meu servidor uma única interface que eu vou chamar de PaymentProvider. [...] PaymentProvider vai ter um método chamado charge.” Uma implementação do fornecedor deve respeitar esse contrato; o fluxo externo usa a abstração sem conhecer os detalhes daquela implementação.
- “Então aqui o meu acoplamento de matrícula para cobrança deveria ser somente com o status da cobrança. [...] Cobrança confirmada, matrícula libera. Cobrança pendente, matrícula bloqueada.” O núcleo traduz estados externos para estados internos e não acessa campos da entidade/SDK de pagamento.
- AppMax não é nomeada na transcrição. O pedido atual escolhe AppMax como exemplo; por isso, o código implementa um adaptador local simulado e não afirma integração real.

## Como isso aparece nos projetos

| Evidência da aula/material | Decisão nesta pasta |
|---|---|
| Sem Spring; código “na mão” | Java puro, interfaces, construtores e `main` como ponto de composição |
| `PaymentProvider.charge` como contrato da aplicação | Mesma porta interna nas duas versões |
| Matrícula depende somente do status | Apenas `CONFIRMED` permite persistir a matrícula |
| Provider concreto isolado atrás de contrato | `AppMaxPaymentAdapter` traduz rótulos simulados para `PaymentStatus` interno |
| Aula 03: Ana e Clara confirmadas; Bia pendente; armazenamento intercambiável | Mesmos estudantes/regra para facilitar comparação; repositório em memória simples para manter o foco em arquitetura |
| Aula 02: Adapter traduz centavos e formato externo | Montagem demonstra adapter sem trazer SDK, segredo ou dados de cartão |

## Por que há dois desenhos

Os limites se sobrepõem, mas a ênfase muda. Em `clean-architecture/`, o foco é a política/caso de uso e a direção das dependências para o núcleo. Em `hexagonal/`, o foco é dar nome às conversas: uma porta de entrada para matrícula, portas de saída para pagamento e persistência, e adaptadores para os agentes externos.

Esses exemplos são intencionalmente pequenos para fins de aula. Não modelam transação distribuída entre cobrança e matrícula, idempotência, consulta/reconciliação, webhook, credenciais ou falhas de rede. Um pagamento real confirmado seguido de falha de persistência exige decisões adicionais; a transcrição da aula de 29/09 discute falhas parciais em outros contextos e este exercício não deve sugerir atomicidade entre AppMax e o armazenamento local.
