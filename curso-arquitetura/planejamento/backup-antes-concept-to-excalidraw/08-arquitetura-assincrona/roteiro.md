# Aula 08 — Arquitetura Assíncrona

**Título Pora:** Arquitetura Assíncrona: Filas, Eventos, Workers, Outbox, Idempotência e Sagas.
**Prazo editorial:** 12/11/2026 — continuação de novembro.
**Duração proposta:** 35 min: 15 de conceitos, 15 de prática, 5 de recuperação. O título reúne muitos conceitos; esta é uma proposta de duração, não uma confirmação da professora.

## Objetivo e contexto

O aluno deve seguir uma operação entre gravação, publicação, consumo e confirmação, localizando onde um evento pode se perder ou repetir. A escola confirma matrícula de Ana. Um worker registra o aviso correspondente depois. A aluna pode ter acesso antes de o aviso ser processado; essa escolha é aceitável no exemplo e precisa ser explicada.

Um segundo cenário, apresentado somente ao discutir Saga, reserva vaga e tenta cobrar. Se a cobrança for recusada, a reserva é liberada por uma ação de compensação. Não confundir isso com a matrícula já paga do primeiro cenário.

## 00:00–15:00 · Conceitos

1. **Slide 01, 00:00–01:00 — Capa.** Trabalho posterior e garantias entre etapas. Assíncrono desacopla o momento de execução; não significa “tudo mais rápido” nem ausência de contrato.
2. **Slide 02, 01:00–02:30 — Fila e worker.** Produtor publica trabalho; fila o mantém disponível segundo suas garantias; worker processa; confirmação informa que pode ser retirado. Se entrada supera processamento, backlog cresce. Mais workers só ajudam enquanto não pressionam um recurso comum ainda mais.
3. **Slide 03, 02:30–04:00 — Comando e evento.** `EnviarAviso` pede uma ação. `MatriculaConfirmada` informa algo ocorrido. Nomear intenção/fato e IDs. Uma fila com consumidores concorrentes normalmente distribui trabalho; broadcast para consumidores independentes exige topologia apropriada, não simplesmente acrescentar consumidores à mesma fila.
4. **Slide 04, 04:00–06:00 — Janela de perda.** Salvar matrícula e depois publicar em outro sistema são dois efeitos. Se o processo falha entre eles, a matrícula fica sem evento. Publicar primeiro também cria um problema: o consumidor pode agir antes de a matrícula existir. Só inverter a ordem não resolve o dual write.
5. **Slide 05, 06:00–08:00 — Outbox.** Salvar alteração de negócio e registro de evento na mesma transação local. Um relay/publicador lê pendências e envia ao broker. A transação protege a intenção local de publicar; o envio continua separado. Se relay falhar após publicar e antes de marcar como enviado, pode reenviar. Isso exige consumidores preparados para duplicidade.
6. **Slide 06, 08:00–10:00 — ACK e repetição.** Worker registra efeito e cai antes de ACK; o broker pode redeliver. ACK antes do efeito arrisca perda. Publisher confirm trata produtor→broker; consumer ACK trata broker→consumidor. Não misturar os dois nem prometer exactly-once de ponta a ponta.
7. **Slide 07, 10:00–12:00 — Idempotência.** Usar ID estável e registrar processamento junto do efeito numa mesma transação, quando ambos cabem no banco local. UNIQUE no ID ajuda a coordenar concorrência; um `if` seguido de gravação não é proteção suficiente. Para e-mail/efeito externo, “marcar como processado” e chamar a API continuam separados: usar idempotência do destino ou outra coordenação, conforme contrato. A demo só registra um aviso local, não envia e-mail real.
8. **Slide 08, 12:00–13:30 — Retry e DLQ.** Falha transitória pode merecer novas tentativas com atraso e limite. Mensagem inválida não melhora com repetição infinita. Ao exceder política, encaminhar para tratamento/DLQ, observar e corrigir antes de reprocessar. Guardar ID, motivo e tentativas. DLQ não é solução automática nem descarte silencioso. Ordenação pode mudar com retries e múltiplos workers.
9. **Slide 09, 13:30–15:00 — Saga.** Sequência de transações locais com ações compensatórias para falhas de negócio. Reserva confirmada → cobrança recusada → liberar reserva. Compensar é outra ação observável, não voltar o tempo. Pode falhar e precisar de retry/intervenção. Orquestração coordena por um participante; coreografia reage a eventos. Explicar a escolha sem implementar ambos nesta aula.

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

## 30:00–35:00 · Slide 10 — Reconstruir as falhas

- Commit feito, publicação não feita: buscar pendência na outbox.
- Publicação feita, marcação não feita: possível envio duplicado.
- Efeito local feito, ACK perdido: consumidor reconhece evento já processado e confirma sem repetir o efeito.
- Mensagem inválida: aplicar política de tratamento; tentar para sempre só cresce o problema.
- Cobrança recusada após reserva: compensar reserva; o histórico da tentativa permanece.

Exercício: desenhar onde guardar ID e efeito para dois workers pegando o mesmo evento. Esperar a resposta antes de revelar a combinação “restrição de unicidade + mesma transação local”. Pergunta final: **qual etapa meu ACK realmente confirma?**

## Fontes

- [Transactional outbox — Chris Richardson](https://microservices.io/patterns/data/transactional-outbox.html).
- [Saga — Chris Richardson](https://microservices.io/patterns/data/saga.html).
- [RabbitMQ — Acknowledgements and confirms](https://www.rabbitmq.com/docs/confirms).
- [RabbitMQ — Dead letter exchanges](https://www.rabbitmq.com/docs/dlx).
