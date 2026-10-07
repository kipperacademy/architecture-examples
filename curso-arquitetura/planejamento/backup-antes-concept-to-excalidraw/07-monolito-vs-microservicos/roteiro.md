# Aula 07 — Monólito vs Microserviços

**Título Pora:** Monólito vs Microserviços: Quando Usar, Comunicação entre Serviços e Dados Distribuídos.
**Prazo editorial:** 05/11/2026 — esta aula está em novembro, não em outubro.
**Duração proposta:** 25 min: 12 de conceitos, 10 de prática, 3 de fechamento.

## Objetivo e contexto

Comparar a fronteira de implantação com a fronteira do negócio e explicar falhas parciais. A escola vende um curso de R$ 100. O checkout pede uma cobrança e aguarda uma confirmação antes de liberar a matrícula. O provedor pode processar a cobrança e perder a resposta. Essa falha também existe num monólito que chama um provedor externo: ela vem da fronteira remota, não do nome da arquitetura.

Pergunta condutora: **o benefício de separar esta parte em outro serviço compensa perder a simplicidade de uma chamada local?**

## 00:00–12:00 · Teoria e diagramas

1. **Slide 01, 00:00–01:00 — Capa.** Decisão de arquitetura orientada por autonomia, limites de escala e custos operacionais. Não apresentar microserviços como etapa obrigatória de amadurecimento.
2. **Slide 02, 01:00–02:30 — Unidade de deploy.** Monólito: componentes da aplicação implantados em conjunto. Microserviços: capacidades com possibilidade de evolução e implantação independente, respeitando contratos. Ambos podem ter boas ou más fronteiras internas. Réplicas do mesmo monólito não se tornam microserviços.
3. **Slide 03, 02:30–04:30 — O que a chamada remota acrescenta.** Mostrar requisição atravessando rede, processamento e resposta de volta. Cada trecho pode atrasar ou falhar. Precisamos de timeout, correlação, observabilidade e uma política de repetição. Contrato inclui semântica e evolução dos dados, não apenas URL ou JSON.
4. **Slide 04, 04:30–06:30 — Timeout não é negação.** A cobrança foi registrada; a resposta se perdeu. O checkout sabe que não recebeu confirmação dentro do limite, mas não sabe se houve efeito. Marcar `UNKNOWN` no cliente e `CONFIRMADO` no provedor. Não converter automaticamente a exceção em “pagamento recusado”. Reconciliação pode consultar a operação pela mesma identidade.
5. **Slide 05, 06:30–08:00 — Retry e idempotência.** Repetir a mesma operação precisa preservar sua identidade. Uma chave nova representa outra intenção. Reutilizar a chave com parâmetros incompatíveis deve ser rejeitado. Em produção, chave, resultado e efeito exigem armazenamento e coordenação corretos; um mapa local não resolve reinícios ou corridas entre réplicas.
6. **Slide 06, 08:00–09:30 — Dados sob donos diferentes.** Escrever diretamente na tabela de outro serviço acopla consumidores ao seu modelo interno. Uma transação local no banco de Matrículas não desfaz o commit no banco de Cobranças. Comunicar por contrato/evento e explicitar qual estado intermediário o negócio admite. Evitar a promessa de transação global automática.
7. **Slide 07, 09:30–11:00 — Quando compensa.** Necessidade concreta de implantação independente, capacidade isolada ou responsabilidade de equipes pode justificar extração. Exigir evidência: qual componente muda/escalona em ritmo distinto? Custos: operação, dados distribuídos, diagnóstico, compatibilidade e falhas parciais. Um monólito modular costuma ser uma opção válida quando esses custos não se pagam.
8. **Slide 08, 11:00–12:00 — Previsão.** Mesma compra, resposta perdida depois da cobrança, uma repetição. “Quantas cobranças ficam no provedor?” Fazer a pergunta para as duas estratégias sem revelar ainda a saída.

## 12:00–22:00 · Prática Java

As demos **simulam** o resultado de uma falha remota de forma determinística. Não executam HTTP, serviços independentes ou espera real de timeout. O objetivo é enxergar a ordem “efeito confirmado → resposta perdida” sem depender de rede aleatória.

### 12:00–16:00 · Retry duplica o efeito

Abrir `Provedor.java`: `cobrancas.add(pedido)` ocorre antes da exceção controlada. Abrir `DemoRetry.java`: instanciar provedor, tentar compra, capturar timeout, repetir exatamente o mesmo pedido e exibir o tamanho da coleção.

Na **pasta do curso**:

```sh
bash 07-monolito-vs-microservicos/executar.sh DemoRetry
```

Resultado conferido: cliente fica `UNKNOWN` na primeira chamada; no final o provedor tem **2 cobranças**. O contador é derivado das gravações na lista. A mensagem da exceção é conhecimento do experimento; o cliente real não poderia concluir que o provedor cobrou apenas olhando um timeout.

### 16:00–20:00 · Mesma chave preserva a intenção

Abrir `ProvedorIdempotente.java` e `DemoIdempotencia.java`. O main deixa `pedido-ana` explícito nas duas tentativas. O provedor guarda chave e valor e recusa a mesma chave com valor diferente.

```sh
bash 07-monolito-vs-microservicos/executar.sh DemoIdempotencia
```

Resultado conferido: primeira resposta desconhecida, segunda confirmada; **1 cobrança** registrada. A diferença vem do registro da identidade e da decisão de não reaplicar o efeito. Não vem de uma interface ou do uso de `try/catch`.

### 20:00–22:00 · Limites e extensão

O `Map` é local, efêmero e usado por uma thread. Não fornece idempotência financeira de produção. O desenho real deve coordenar unicidade, payload, efeito e resultado de forma atômica, prever retenção e preservar a chave entre tentativas/reinícios do cliente. Se o efeito está num provedor externo, usar a garantia oferecida por ele e reconciliar estados incertos.

Perguntar o que ocorre ao repetir com `pedido-ana-2`: será outra operação e poderá cobrar novamente. Exercício alternativo: manter chave e mudar o valor para 12000; prever a rejeição por conflito. Não executar esses desvios antes de consolidar o contraste principal.

## 22:00–25:00 · Slide 09 — Tomar a decisão

Pedir uma decisão para dois cenários: equipe pequena que muda matrícula e cobrança juntas; processamento de vídeos que precisa escalar e evoluir independentemente. Não fornecer resposta universal: o aluno deve ligar necessidade, fronteira e custo. Encerrar com “qual falha parcial esta divisão passa a permitir?”.

Ponte para assíncrono: liberar trabalho posterior da espera direta pode ajudar; fila também exige lidar com publicação, repetição e estado. Não prometer que eventos eliminam acoplamento ou erros distribuídos.

## Fontes

- [Lewis e Fowler — Microservices](https://martinfowler.com/articles/microservices.html): implantação independente e consequências da distribuição.
- [AWS Builders' Library — Making retries safe](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/): identidade da intenção e tratamento de repetição.
- [Transactional outbox](https://microservices.io/patterns/data/transactional-outbox.html): fronteira entre gravação e publicação, aprofundada na aula seguinte.
