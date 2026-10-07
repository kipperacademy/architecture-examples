# Aula 08 — Arquitetura Assíncrona

**Título Pora:** Arquitetura Assíncrona: Filas, Eventos, Workers, Outbox, Idempotência e Sagas.
**Prazo editorial:** 12/11/2026 — continuação de novembro.
**Duração proposta:** 35 min: 15 de conceitos, 15 de prática, 5 de recuperação. O título reúne muitos conceitos; esta é uma proposta de duração, não uma confirmação da professora.

## Objetivo e contexto

O aluno deve seguir uma operação entre gravação, publicação, consumo e confirmação, localizando onde um evento pode se perder ou repetir. A escola confirma matrícula de Ana. Um worker registra o aviso correspondente depois. A aluna pode ter acesso antes de o aviso ser processado; essa escolha é aceitável no exemplo e precisa ser explicada.

Um segundo cenário, apresentado somente ao discutir Saga, reserva vaga e tenta cobrar. Se a cobrança for recusada, a reserva é liberada por uma ação de compensação. Não confundir isso com a matrícula já paga do primeiro cenário.

## 00:00–15:00 · Conceitos

1. **Slide 01, 00:00–01:00 — Contexto.** A matrícula de Ana foi confirmada; um worker aplicará o aviso depois. O ID `evento-1` acompanha o caminho.
2. **Slide 02, 01:00–02:30 — Fila e ACK.** A fila tem três IDs; o worker processa `evento-1`; o ACK o retira e restam dois. Com entrada de 3/s e saída de 1/s, o backlog cresce 2/s.
3. **Slide 03, 02:30–04:00 — Comando e evento.** Mostrar dois fluxos independentes: o comando `EnviarAviso` chega ao worker, que envia o aviso; o evento `MatriculaConfirmada` chega ao consumidor, que também pode decidir enviar o aviso. O comando não se transforma no evento.
4. **Slide 04, 04:00–06:00 — Dual write.** Banco confirma a matrícula, processo cai antes de publicar e a fila fica vazia. Inverter a ordem pode entregar evento antes do commit, então não basta trocar a sequência.
5. **Slide 05, 06:00–08:00 — Outbox.** Matrícula e `evento-1` pendente entram na mesma transação local. Relay lê a pendência, publica no broker e marca envio depois.
6. **Slide 06, 08:00–09:00 — Janela de duplicidade do relay.** Se publicar e cair antes de marcar, ao retomar publica o mesmo `evento-1` outra vez. O ID estável facilita a deduplicação; não promete exactly-once.
7. **Slide 07, 09:00–10:30 — Efeito e ID, antes do ACK.** Consumidor grava ID e aviso no mesmo commit local. Worker cai antes de enviar ACK; conexão fecha, broker reentrega; o ID existente impede outro aviso e o worker confirma a entrega.
8. **Slide 08, 10:30–11:30 — Comparar o efeito repetido.** Duas entregas de `evento-1`: sem dedupe, avisos `[Ana, Ana]`; com dedupe, `[Ana]`. Conferir contra `DemoEntregaDuplicada` e `DemoConsumidorIdempotente`.
9. **Slide 09, 11:30–13:30 — Retry e DLQ.** Repetir a mesma mensagem após 0, 1 e 5 segundos; após a terceira tentativa, encaminhar para DLQ e corrigir antes do replay. Dado inválido não melhora com retry infinito.
10. **Slide 10, 13:30–15:00 — Saga.** Em outro cenário, reservar vaga, receber recusa de cobrança e liberar a reserva por nova ação compensatória. A compensação pode falhar e precisa de recuperação.

## 15:00–30:00 · Prática Java

**Limite declarado antes de executar:** modelos locais em memória, uma thread, sem broker e sem persistência em disco. As “paradas” interrompem etapas do fluxo didático, não matam o processo JVM. Esses exemplos mostram causa e consequência; não demonstram recuperação durável após crash. Nenhum e-mail é enviado.

### 15:00–21:00 · Perder o evento e guardar a intenção

Abrir `DemoEventoPerdido.java`: a matrícula é salva, a publicação é deliberadamente omitida para modelar a interrupção. Na **pasta do curso**:

```sh
bash 08-arquitetura-assincrona/executar.sh DemoEventoPerdido
```

Conferido: matrículas `[Ana]`, fila com **0** eventos. O programa não inventa esse total: ele vem da fila que não recebeu a publicação.

Abrir `Estado.java` e `Escola.matricularComOutbox`: construir novo estado contendo matrícula e evento; trocar a referência uma vez. Esse recurso modela a gravação conjunta na execução sequencial; **não é uma transação de banco nem garantia durável**.

```sh
bash 08-arquitetura-assincrona/executar.sh DemoOutbox
```

Conferido: uma pendência enquanto o publicador está parado; ao retomá-lo, **1** evento na fila. Nesta demo a pendência não é marcada como enviada. Reexecutar o loop publicaria novamente, mostrando por que o consumidor precisa suportar repetição. Em produção haveria tabela durável e rastreamento do envio, sem eliminar a janela de duplicidade.

### 21:00–27:00 · Efeito repetido antes do ACK

Abrir `Fila.java`: `proximo()` não remove; `confirmar()` remove. São operações separadas para tornar o intervalo visível. Perguntar: **se o worker já registrou o aviso e ainda não confirmou, quantos registros surgem ao tentar de novo?**

```sh
bash 08-arquitetura-assincrona/executar.sh DemoEntregaDuplicada
bash 08-arquitetura-assincrona/executar.sh DemoConsumidorIdempotente
```

Conferido: `[Ana, Ana]` no primeiro; `[Ana]` no segundo. O mesmo evento `evento-1` é obtido novamente porque continua na fila. O segundo consumidor consulta o ID processado antes de adicionar o aviso.

### 27:00–30:00 · Transferir o mecanismo para produção

Abrir `sql/contratos.sql` como modelo de persistência, não um serviço já implementado. Explicar duas transações locais diferentes: produtor grava matrícula + outbox; consumidor grava ID processado + aviso. Uma restrição única disputa a posse do evento no consumidor. Confirmar ao broker só após o commit local.

O Java não é concorrente; o `HashSet` não é atômico junto da lista e desaparece ao reiniciar. As tabelas descrevem a garantia necessária, não justificam dizer que as demos já a implementam. Para sair deste material e entregar um sistema, faltam driver/repositórios, relay, broker, contratos de redelivery e testes de crash/concorrência. Não esconder essa fronteira de escopo.

## 30:00–35:00 · Reconstruir as falhas

- Commit feito, publicação não feita: buscar pendência na outbox.
- Publicação feita, marcação não feita: possível envio duplicado.
- Efeito local feito, ACK perdido: consumidor reconhece evento já processado e confirma sem repetir o efeito.
- Mensagem inválida: aplicar política de tratamento; tentar para sempre só cresce o problema.
- Cobrança recusada após reserva: compensar reserva; o histórico da tentativa permanece.

Usar novamente os slides 04–10 para reconstruir cada caso. Exercício: desenhar onde guardar ID e efeito para dois workers pegando o mesmo evento. Esperar a resposta antes de revelar a combinação “restrição de unicidade + mesma transação local”. Pergunta final: **qual etapa meu ACK realmente confirma?**

## Guia visual para a gravação

- **Slide 01 — Pergunta:** que trabalho pode continuar depois de confirmar matrícula? **Aponte:** Ana, publicação de `evento-1`, fila e aviso. **Resultado:** o acesso pode vir antes do processamento posterior.
- **Slide 02 — Pergunta:** o que muda quando o worker confirma? **Aponte:** fila de 3, processamento do primeiro ID e fila de 2. **Resultado:** ACK retira uma mensagem; diferença 3/s − 1/s faz backlog crescer.
- **Slide 03 — Pergunta:** quem iniciou cada aviso? **Aponte:** os dois fluxos separados: comando ao worker e evento ao consumidor. **Resultado:** comando e evento têm contratos distintos; não há conversão causal entre eles.
- **Slide 04 — Pergunta:** em qual intervalo a publicação se perde? **Aponte:** commit da matrícula, queda e fila com zero mensagens. **Resultado:** estado do negócio existe sem evento.
- **Slide 05 — Pergunta:** que registros compartilham a transação? **Aponte:** matrícula e outbox, depois relay e broker. **Resultado:** intenção persiste localmente; relay lê, publica e marca depois.
- **Slide 06 — Pergunta:** quando o mesmo evento pode aparecer outra vez? **Aponte:** publish, queda antes da marca e retomada do relay. **Resultado:** broker recebe duas entregas com ID `evento-1`.
- **Slide 07 — Pergunta:** o que acontece se o worker cai antes do ACK? **Aponte:** commit local, conexão encerrada, redelivery, ID já existente e ACK. **Resultado:** reentrega sem repetir o aviso.
- **Slide 08 — Pergunta:** qual é o efeito de duas entregas com o mesmo ID? **Aponte:** entrada `evento-1` duas vezes e listas de avisos. **Resultado:** sem dedupe `[Ana, Ana]`; com dedupe `[Ana]`.
- **Slide 09 — Pergunta:** quantas tentativas antes de tratar à parte? **Aponte:** relógio, mesmo ID e terceira falha até a DLQ. **Resultado:** limite evita repetição infinita; correção antecede replay.
- **Slide 10 — Pergunta:** como liberar vaga depois de recusar cobrança? **Aponte:** reserva confirmada, recusa e nova ação de liberação. **Resultado:** compensação é outro evento e também pode falhar.

## Fontes

- [Transactional outbox — Chris Richardson](https://microservices.io/patterns/data/transactional-outbox.html).
- [Saga — Chris Richardson](https://microservices.io/patterns/data/saga.html).
- [RabbitMQ — Acknowledgements and confirms](https://www.rabbitmq.com/docs/confirms).
- [RabbitMQ — Dead letter exchanges](https://www.rabbitmq.com/docs/dlx).
