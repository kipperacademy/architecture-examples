# Aula 08 — Arquitetura assíncrona: aplicações que conversam em momentos diferentes

Revisão de 7/10/2026. Seis slides para quem acabou de aprender microsserviços. Os desenhos são cenários conceituais; não representam integrações de produção executadas neste projeto.

## 1. Duas aplicações: quem espera por quem?

Comece lembrando que separar a aplicação em serviços cria a necessidade de comunicação. Uma API expõe um contrato de operações e dados. No desenho, a Loja pede uma reserva ao Estoque e espera o resultado para continuar aquele fluxo. Essa espera é a dependência síncrona relevante para a arquitetura. Não confundir com bloquear uma thread: mesmo um cliente HTTP com I/O não bloqueante pode depender do resultado para concluir o pedido.

**Frase para lembrar:** assíncrono separa a solicitação da conclusão do trabalho. Pode coexistir com comunicação síncrona no mesmo sistema.

**Apontar:** ida da solicitação, processamento no Estoque, retorno e só então continuação. **Perguntar:** se o Estoque demorar, qual etapa da Loja também espera?

## 2. Aceitar agora, concluir depois

A Loja chama POST /reservas. A API registra uma tarefa com ID 42 e estado PENDENTE, responde 202 e um worker processa a reserva depois. Worker significa processo que executa trabalho em segundo plano. A tarefa precisa existir em um mecanismo acessível ao worker; o desenho omite sua implementação para primeiro explicar o tempo. A próxima página introduz um broker como uma opção para entregar trabalho.

202 indica aceitação, não sucesso final. O contrato desta API fornece ID e consulta GET /tarefas/42. A tela pode mostrar “processando”, continuar outras ações e consultar o resultado. Também deve tratar falha, expiração e estado ainda pendente. Callback/webhook ou evento são alternativas à consulta periódica; não são garantias automáticas de HTTP.

**Apontar:** resposta 202 antes da execução do worker; depois outra chamada obtém o resultado. **Perguntar:** “aceito” permite dizer ao usuário “reserva concluída”?

## 3. Produtor, broker, fila e consumidor

Produtor é o papel de quem publica uma mensagem. Consumidor é quem a recebe e realiza o trabalho. Message broker é o intermediário que recebe, roteia e entrega mensagens conforme sua configuração. Uma aplicação pode exercer os dois papéis em fluxos diferentes. Uma mensagem contém dados, identidade e um contrato de significado; não é uma chamada de método que atravessa processos.

Neste exemplo, Pedidos publica tarefas de aviso. A fila acumula trabalho enquanto os workers de Avisos processam. Os dois workers competem pela mesma fila: m1 vai para A, m2 para B. Isso distribui carga, não envia automaticamente cada mensagem para todos. A fila armazena mensagens pendentes ou ainda não confirmadas conforme o broker. Retenção, persistência, limites e comportamento na falha precisam ser configurados; desenhar uma fila não torna os dados duráveis.

**Apontar:** mensagens individuais e seus destinos. **Perguntar:** se os dois workers saírem do ar, onde o trabalho aguarda? Diferenciar confirmação de publicação do produtor de ACK após consumo.

## 4. Tópico e assinaturas independentes

Um tópico organiza publicações por assunto. Aqui usamos o modelo conceitual pub/sub: o evento PedidoConfirmado, ID e42, interessa a Email e Notas. Cada interesse tem uma assinatura e sua própria fila. Assim, o mesmo fato gera duas entregas independentes. Se Email estiver lento, Notas pode continuar; cada assinatura mantém seu próprio progresso.

Evento descreve um fato ocorrido; comando pede uma ação. PedidoConfirmado é evento, EnviarAviso seria comando. Produtos têm modelos diferentes: tópico, exchange, assinatura e grupo de consumidores não são termos universalmente equivalentes. Em RabbitMQ, o exemplo pode ser implementado com exchange, bindings e filas; em sistemas de log, grupos acompanham posições. A figura explica o comportamento desejado, sem prometer broadcast para qualquer configuração.

**Apontar:** o mesmo ID nas duas filas. **Perguntar:** colocar Email e Notas na mesma fila competitiva garantiria os dois efeitos? Não.

## 5. ACK, reentrega e idempotência

ACK é a confirmação que o consumidor envia ao broker. Confirmar antes do efeito pode perder trabalho se o processo cair em seguida. Confirmar depois é necessário neste fluxo, mas existe outra janela: o efeito foi gravado e o consumidor caiu antes de enviar ACK. O broker pode entregar novamente o mesmo ID.

Idempotência significa que repetir a operação não repete indevidamente seu efeito. A figura registra o aviso e o ID processado na mesma transação local, com proteção de unicidade; na reentrega, encontra e42 e confirma sem registrar outro aviso. Uma consulta de ID solta antes de gravar não protege contra concorrência ou falha entre passos. Enviar email ou chamar outra API é um efeito externo e não participa automaticamente dessa transação: requer estratégia própria, como uma chave de idempotência aceita pelo destino. Não prometer exactly-once de ponta a ponta.

**Apontar:** efeito salvo → queda sem ACK → mesmo ID → apenas um efeito. **Perguntar:** duas entregas precisam virar dois avisos?

## 6. Falhas, estado e acompanhamento

- **Retry:** repetir quando há chance de uma falha transitória desaparecer, como indisponibilidade temporária. Mensagem inválida pode exigir correção em vez de repetição.
- **Backoff:** aumentar o intervalo entre tentativas para não sobrecarregar uma dependência em falha; jitter espalha os horários. +1 s e +5 s são uma política ilustrativa, não padrão obrigatório.
- **DLQ (dead-letter queue):** destino separado para mensagens que não puderam ser tratadas segundo a política. Guardar motivo, tentativas e identidade; alertar, investigar e só então reprocessar. DLQ não corrige dados sozinha.
- **Consistência eventual:** serviços podem refletir um fato em momentos diferentes. Pedido confirmado e nota ainda pendente são estados intermediários que a experiência precisa explicar. Convergência depende de processamento e recuperação funcionando; não há prazo garantido apenas por usar eventos.
- **Ordem:** paralelismo e retries podem mudar a ordem de conclusão. Definir onde a ordem importa, por exemplo por pedido, e escolher serialização/particionamento e validação de versões adequadas. Uma chave sozinha não implementa a garantia.
- **Observabilidade:** acompanhar eventId, pedidoId/correlação, tentativas, erros, idade da mensagem, backlog e estado final. Um POST aceito não demonstra que a tarefa terminou.
- **Capacidade/backpressure:** se o produtor envia mais do que os consumidores conseguem processar, a fila cresce. Limitar entrada ou concorrência, escalar com atenção à dependência final e investigar o gargalo.

**Pergunta final:** como descobrir e recuperar uma mensagem aceita que ainda não virou um resultado?

## Código e aprofundamento

As demos existentes de matrícula continuam disponíveis como exercícios complementares de duplicação e idempotência. Outbox e Saga da versão anterior foram retirados da sequência principal para respeitar seis slides e a progressão de iniciantes; materiais anteriores estão no backup. As demos Java são simulações em memória, não a implementação de um broker de produção.

## Fontes para a professora

- HTTP 202: https://www.rfc-editor.org/rfc/rfc9110.html#section-15.3.3
- Filas e confirmações: https://www.rabbitmq.com/tutorials/tutorial-two-java
- Publicação e assinaturas: https://www.rabbitmq.com/tutorials/tutorial-three-java
- Confiabilidade: https://www.rabbitmq.com/docs/reliability

As frases dos slides são paráfrases didáticas, não citações literais.
