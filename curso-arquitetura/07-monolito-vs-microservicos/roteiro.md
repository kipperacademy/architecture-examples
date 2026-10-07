# Aula 07 — Monólito vs Microserviços

**Título Pora:** Monólito vs Microserviços: Quando Usar, Comunicação entre Serviços e Dados Distribuídos.
**Prazo editorial:** 05/11/2026 — esta aula está em novembro, não em outubro.
**Duração proposta:** 25 min: 12 de conceitos, 10 de prática, 3 de fechamento.

## Objetivo e contexto

Comparar a fronteira de implantação com a fronteira do negócio e explicar falhas parciais. A escola vende um curso de R$ 100. O checkout pede uma cobrança e aguarda uma confirmação antes de liberar a matrícula. O provedor pode processar a cobrança e perder a resposta. Essa falha também existe num monólito que chama um provedor externo: ela vem da fronteira remota, não do nome da arquitetura.

Pergunta condutora: **o benefício de separar esta parte em outro serviço compensa perder a simplicidade de uma chamada local?**

## 00:00–12:00 · Teoria e diagramas

1. **Slide 01, 00:00–01:00 — Contexto.** A escola vende por R$ 100; o checkout precisa falar com o provedor e confirmar a compra. Apresentar a fronteira como escolha e perguntar qual benefício justificaria separá-la.
2. **Slide 02, 01:00–02:30 — O que é implantado junto?** Comparar módulos locais no artefato `escola.jar` com dois processos e contratos entre serviços. Réplicas não alteram a unidade de deploy.
3. **Slide 03, 02:30–04:30 — A ida e volta remota.** Seguir `pedido-ana` com 10000 centavos: o provedor registra a cobrança #1, o checkout aguarda resposta e ela se perde. Resultado no cliente: `UNKNOWN`, não “recusado”. O timeout é a incerteza da demo, sem duração afirmada.
4. **Slide 04, 04:30–06:30 — A identidade do retry.** Comparar o mesmo cenário: sem guardar chave, duas cobranças; com `pedido-ana` e o mesmo valor, uma cobrança e resposta recuperada. ID novo pode representar outra operação; mesmo ID com outro valor deve conflitar.
5. **Slide 05, 06:30–08:00 — Dois bancos, dois commits.** Financeiro confirma sua escrita; Acadêmico rejeita a vaga já ocupada e faz rollback local. O primeiro commit permanece. Uma compensação seria uma nova operação.
6. **Slide 06, 08:00–09:30 — Benefício com cenário concreto.** Equipe pequena que muda matrícula e cobrança juntas tende a ganhar simplicidade com um deploy. Transcodificação de vídeo que cresce 10× pode justificar escala e deploy isolados, desde que autonomia pague operação, contratos, traces, plantão e falhas parciais.
7. **Slide 07, 09:30–11:00 — Diagnóstico distribuído.** Correlacionar `pedido-ana`, timeout, retry e consulta do resultado. Contratos e observabilidade são parte da fronteira, não detalhes posteriores.
8. **Slide 08, 11:00–12:00 — Decisão.** Comparar os dois cenários e ligar necessidade, fronteira e custo. Não fornecer uma resposta universal.

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

## 22:00–25:00 · Fechar a decisão

Retomar o slide 08 e pedir uma decisão para os dois cenários: equipe pequena que muda matrícula e cobrança juntas; processamento de vídeos que precisa escalar e evoluir independentemente. Não fornecer resposta universal: o aluno deve ligar necessidade, fronteira e custo. Encerrar com “qual falha parcial esta divisão passa a permitir?”.

Ponte para assíncrono: liberar trabalho posterior da espera direta pode ajudar; fila também exige lidar com publicação, repetição e estado. Não prometer que eventos eliminam acoplamento ou erros distribuídos.

## Guia visual para a gravação

- **Slide 01 — Pergunta:** qual parte da compra atravessa uma fronteira? **Aponte:** `pedido-ana` e `10000 centavos`, depois a escolha central. **Resultado:** a decisão exige benefício concreto.
- **Slide 02 — Pergunta:** o que muda entre um e dois deploys? **Aponte:** `escola.jar`, chamada local, os dois serviços e `contrato v1`. **Resultado:** aumenta a autonomia e surge uma fronteira de rede.
- **Slide 03 — Pergunta:** o timeout prova que a cobrança falhou? **Aponte:** POST, estado do provedor, resposta perdida e estado do checkout. **Resultado:** provedor tem cobrança #1; cliente fica `UNKNOWN`.
- **Slide 04 — Pergunta:** quantas cobranças ficam após a repetição? **Aponte:** primeiro a coluna sem chave, depois chave/valor e a resposta reutilizada. **Resultado:** 2 sem identidade protegida; 1 com mesma chave e valor.
- **Slide 05 — Pergunta:** qual commit o rollback desfaz? **Aponte:** banco A, pedido entre serviços, conflito e rollback no banco B. **Resultado:** recebimento de A continua confirmado.
- **Slide 06 — Pergunta:** qual carga ou mudança está crescendo de forma diferente? **Aponte:** os dois cenários e o respectivo deploy. **Resultado:** autonomia pode compensar custos operacionais quando há evidência.
- **Slide 07 — Pergunta:** como localizar o pedido incerto? **Aponte:** span remoto, correlation ID e estados ligados a `pedido-ana`. **Resultado:** observabilidade permite reconciliar a chamada distribuída.
- **Slide 08 — Pergunta:** qual cenário paga o custo da fronteira? **Aponte:** equipe e mudanças conjuntas, depois vídeo e escala 10×. **Resultado:** justificar uma escolha e nomear a falha parcial criada.

## Fontes

- [Lewis e Fowler — Microservices](https://martinfowler.com/articles/microservices.html): implantação independente e consequências da distribuição.
- [AWS Builders' Library — Making retries safe](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/): identidade da intenção e tratamento de repetição.
- [Transactional outbox](https://microservices.io/patterns/data/transactional-outbox.html): fronteira entre gravação e publicação, aprofundada na aula seguinte.
