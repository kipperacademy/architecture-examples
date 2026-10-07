# Aula 01 — SOLID e acoplamento

**20 minutos: 10 de teoria + 10 de prática.** Roteiro de apoio em tópicos; os tempos são metas de gravação. Código preparado, sem digitar a aplicação inteira ao vivo.

**História:** Ana, Bia e Clara compraram um curso. Pagamento confirmado libera acesso; a notificação comunica essa liberação. Continuidade do exemplo de matrícula e cobrança da introdução.

**Pergunta que conduz a aula:** se o e-mail cair, quem já pagou deve perder o acesso?

## 00:00–10:00 · Teoria no Excalidraw

Abrir `teoria.excalidraw` no Excalidraw Plus e iniciar a apresentação. O arquivo local revisado contém **13 frames: uma capa, dez telas da teoria e duas telas para explicar a execução na prática**, um assunto por tela, na mesma ordem dos blocos abaixo. A configuração nativa online deve ser conferida após importar a revisão; a contagem local não comprova essa configuração. Estilo: fundo branco, títulos manuscritos com marca roxa, explicação curta acima do desenho, caixas coloridas, trechos de código e anotações roxas apontando a causa concreta.

| Slide | Assunto | Tempo |
|---|---|---|
| Capa | Tema, objetivo e tópicos da aula | 00:00–00:30 |
| Nova página, após a capa | O que é SOLID: cinco princípios para responsabilidades e dependências | ~45 s |
| 01 | Regra de matrícula | 00:30–01:00 |
| 02 | Acoplamento: mudar o canal exige editar matrícula | 01:00–02:15 |
| 03 | Coesão: agrupar operações pelo propósito | 02:15–03:15 |
| 04 | S: quem pede a mudança e qual parte muda | 03:15–04:25 |
| 05 | D: tipos citados no código e direção das dependências | 04:25–05:55 |
| 06 | O: regra preservada, implementação nova, montagem alterada | 05:55–07:00 |
| 07 | L: sucesso, falha prevista e promessa quebrada | 07:00–08:15 |
| 08 | I: consultar sem depender de estornar/emitir nota | 08:15–09:15 |
| 09 | Prever o resultado antes da execução | 09:15–10:00 |

Os trechos dos slides são recortes simplificados; os arquivos executáveis preservam o fluxo completo. Formatação de mensagem é uma responsabilidade ilustrativa na teoria; na simulação, o envio imprime uma linha.

### 00:00–00:30 · Apresentar a aula antes do exemplo

- **Visual — capa:** apresentar “SOLID e acoplamento” como parte de arquitetura de código.
- Estabelecer o objetivo: organizar responsabilidades e dependências para reduzir o impacto das mudanças no código.
- Antecipar as três perguntas: o que uma parte conhece da outra; quais responsabilidades ficam juntas; como os cinco princípios SOLID orientam essas decisões.
- Anunciar a divisão: 10 minutos de conceitos e 10 minutos de Java. Transição: usar a matrícula em um curso para acompanhar essas decisões em uma história concreta.

### 00:30–01:00 · Apresentar a regra e o problema

- Retomar a decisão de design de código da introdução: responsabilidades e dependências dentro da aplicação.
- Explicar a regra da escola: pagamento confirmado permite liberar a matrícula; enviar o aviso é um passo de comunicação.
- Percorrer a regra pretendida: pagamento confirmado → acesso liberado → aviso. Introduzir a dúvida: será que o código sempre preserva essa prioridade quando o aviso falha? Guardar a execução para a prática.
- **Visual — slide 01:** sublinhar a condição de acesso e apontar a anotação “E se o e-mail cair?”.

### 01:00–02:15 · Acoplamento

- **Lembrete:** interdependência entre partes. Observar o que uma classe conhece de outra e quais mudanças ou falhas chegam até ela.
- No exemplo, consultar o pagamento é necessário. Instanciar um canal específico dentro da matrícula faz a regra conhecer uma escolha técnica; exigir sucesso do envio antes do acesso também cria uma dependência de execução.
- Relacionar ao exemplo da introdução: mudar endereço de cobrança não deveria exigir mudar a regra de acesso. Aqui, trocar o canal de comunicação também não deveria exigir reescrevê-la.
- **Visual — slide 02:** ler o pedido “agora o aviso deve ir pelo WhatsApp”; apontar `new Email(true)` dentro da matrícula e a anotação de alteração no mesmo arquivo. A conclusão é visível: a regra de acesso não mudou, mas a classe precisou mudar. Pergunta de transição: o que pertence à matrícula e o que pertence ao aviso?

### 02:15–03:15 · Coesão

- **Lembrete:** quanto as responsabilidades reunidas em uma unidade contribuem para um propósito relacionado.
- Matrícula decide acesso e coordena esse caso de uso. Notificação conhece os detalhes do envio. Mudar o texto ou fornecedor da mensagem tem um motivo diferente de mudar o critério de matrícula.
- Uma classe pode ter vários métodos coesos. Dividir cada linha em uma classe também pode dificultar a compreensão.
- **Visual — slide 03:** as duas operações azuis decidem acesso; a operação amarela comunica. Comparar o grupo misturado com os dois grupos de propósito explícito.

### 03:15–04:25 · S — Single Responsibility Principle

- **Responsabilidade única:** reunir o que muda pelo mesmo motivo e separar razões independentes de mudança.
- A operação educacional define acesso; comunicação define como avisar. Mostrar a mudança concreta: trocar a mensagem não deveria alterar a decisão sobre pagamento.
- Coordenar consulta, decisão e aviso faz parte do caso de uso. Implementar SDK, template e regra de acesso no mesmo lugar mistura decisões diferentes.
- **Visual — slide 04:** percorrer cada pedido real de mudança até a parte que deve responder a ele.

### 04:25–05:55 · D — Dependency Inversion Principle

- **Inversão de dependência:** a política de alto nível e os detalhes se apoiam em abstrações; o contrato descreve a necessidade da regra, sem expor particularidades do fornecedor.
- A matrícula precisa consultar uma situação e solicitar um aviso. Mostrar os contratos `ConsultaPagamento` e `Notificador`.
- **Visual — slide 05:** apontar `Notificador canal` dentro da regra e `implements Notificador` no detalhe. As setas representam tipos citados pelo código. As duas classes conhecem o contrato; a regra não referencia `Email`.
- O construtor recebe o colaborador. A escolha concreta fica no `main` de cada demo. Isso demonstra injeção manual; Spring é desnecessário para explicar a ideia.
- **Distinção breve:** receber um objeto concreto pelo construtor já é injeção. A inversão exige também que o contrato proteja a regra dos detalhes que variam.

### 05:55–07:00 · O — Open/Closed Principle

- **Aberto/fechado:** permitir uma extensão identificada preservando a parte que deve permanecer estável.
- O pedido agora é enviar pelo WhatsApp. Acrescentar uma implementação do mesmo contrato e mudar a montagem, preservando `Matriculas`.
- A proteção vale para essa variação: canal de notificação. Uma regra nova de acesso pode exigir mudar a classe. Um `if` no ponto de escolha não invalida automaticamente o princípio.
- **Visual — slide 06:** ler as três partes numeradas: linha da regra preservada, nova implementação e escolha alterada no `main` da demo.

### 07:00–08:15 · L — Liskov Substitution Principle

- **Substituição de Liskov:** uma implementação precisa poder substituir outra preservando as promessas do contrato e as expectativas válidas de quem chama.
- Contrato da demonstração: `enviar` recebe uma aluna válida, tenta entregar o aviso e pode sinalizar falha de entrega com `IOException`. Sucesso não pode significar “não fiz nada”. Não há promessa de entrega sempre bem-sucedida.
- `Email` e `WhatsApp` respeitam a mesma operação. Uma implementação que só aceita algumas alunas sem isso estar no contrato ou lança “operação não suportada” quebra a expectativa.
- Compilar e implementar a interface garante a assinatura; não prova o comportamento.
- **Visual — slide 07:** comparar as três linhas: envio com sucesso, falha prevista e implementação que retorna normalmente sem enviar. A última quebra a promessa do contrato.

### 08:15–09:15 · I — Interface Segregation Principle

- **Segregação de interfaces:** um cliente não deve depender de operações de que não precisa.
- Matrícula consulta pagamento. Um contrato `Financeiro` com consultar, estornar e emitir nota ofereceria responsabilidades alheias a esse consumidor.
- Mostrar a alternativa `ConsultaPagamento.consultar`. O contrato é pequeno porque corresponde à necessidade do consumidor; não há obrigação de toda interface ter um só método.
- **Visual — slide 08:** matrícula usa a consulta; estornar e emitir nota estão acinzentados porque são alheios a essa necessidade. Extrair a consulta para um contrato específico.

### 09:15–10:00 · Retomar o mapa e preparar a previsão

- **Visual — slide 09:** deixar os dois contadores como “? / 3”. Retomar oralmente: coesão pergunta o que fica junto; acoplamento pergunta como as partes se relacionam. SOLID oferece critérios para essas decisões.
- Repetir a situação: três pagamentos confirmados, mesmo curso, e-mail indisponível.
- Pedir uma previsão do número de acessos em cada versão. Ir para a IDE sem revelar o placar no slide.

## 10:00–20:00 · Prática em Java

Cada exemplo tem um `main` independente. Abrir uma demo por vez na IDE; a tela mostra criação dos objetos → pedidos → confirmação → resultado. Os comandos abaixo partem de `curso-arquitetura` e compilam antes de executar.

### 10:00–11:15 · Ler a primeira versão

- Abrir `DemoAcoplamento.java`: três alunas, pagamento confirmado, e-mail indisponível.
- Abrir `MatriculasAcopladas.java`: a classe cria e conhece `Email`; o envio vem antes da inclusão em `acessos`.
- Mostrar que trocar o canal exigiria alterar essa dependência concreta dentro da matrícula.

### 11:15–12:00 · Estabelecer o resultado normal

- Abrir `DemoEmail.java`. Apontar a montagem explícita: `new Matriculas(new PagamentoLocal(), new Email(true))`.
- Percorrer a criação dos pedidos e a chamada `matriculas.confirmar(pedido)`.

```sh
bash 01-solid-acoplamento-coesao/executar.sh DemoEmail
```

- **Resultado esperado:** 3/3 acessos, zero avisos pendentes. `true` simula e-mail disponível.
- A classe `Matriculas` recebe um `Notificador`; `Email` é uma implementação aceita pelo construtor.

### 12:00–13:00 · Momento WOW: quem pagou ficou sem acesso

- Voltar a `DemoAcoplamento.java`. Pedir a previsão: os três pagamentos estão confirmados, mas o e-mail está fora do ar.

```sh
bash 01-solid-acoplamento-coesao/executar.sh DemoAcoplamento
```

- **Resultado esperado:** 0/3. A exceção interrompe cada confirmação antes de registrar acesso.
- Abrir `DemoDesacoplamento.java`: os mesmos pedidos e a mesma indisponibilidade de e-mail.

```sh
bash 01-solid-acoplamento-coesao/executar.sh DemoDesacoplamento
```

- **Resultado esperado:** 3/3, com três avisos pendentes. Comparar os resultados das duas execuções.

### 13:00–15:30 · Mostrar injeção e explicar a causa

- Na demo, apontar as duas linhas:

```java
Notificador notificador = new Email(false);
Matriculas matriculas = new Matriculas(new PagamentoLocal(), notificador);
```

- O objeto concreto é `Email`; a variável e o parâmetro do construtor usam o contrato `Notificador`. Quem escolhe o canal é a demo.
- Abrir `Matriculas.java`: pagamento diferente de `CONFIRMADO` encerra o fluxo. Depois vem a inclusão em `acessos`, seguida da tentativa de envio. A falha esperada vira aviso pendente.
- Mostrar os contratos em `Contratos.java` e os detalhes simulados em `Integracoes.java`.
- Relacionar S à separação de decisões, D ao contrato recebido e I à consulta sem operações financeiras extras.
- **Causalidade:** a ordem e o tratamento da falha explicam a diferença de acessos. Também seria possível corrigir o bloqueio na versão acoplada com tratamento adequado. Interfaces não criam tolerância a falhas automaticamente.

### 15:30–17:30 · Trocar uma linha e manter a regra

- Ainda em `DemoDesacoplamento.java`, trocar apenas:

```java
Notificador notificador = new WhatsApp();
```

- Manter a construção de `Matriculas` e o restante do fluxo. Pedir a previsão e executar a mesma demo novamente.

```sh
bash 01-solid-acoplamento-coesao/executar.sh DemoDesacoplamento
```

- **Resultado esperado após a troca:** avisos de WhatsApp, 3/3 acessos, zero pendências. `Matriculas` não foi editada.
- O: o canal pode variar preservando a regra. L: a nova implementação respeita as expectativas do contrato.
- `DemoWhatsApp.java` oferece a versão já preparada, com `new Matriculas(new PagamentoLocal(), new WhatsApp())`, caso prefira não editar ao vivo:

```sh
bash 01-solid-acoplamento-coesao/executar.sh DemoWhatsApp
```

### 17:30–18:45 · Mudar a condição do negócio

- Abrir `DemoPagamentoPendente.java`: a montagem usa e-mail disponível; os três pedidos têm status `PENDENTE`.
- Pedir a previsão antes de rodar.

```sh
bash 01-solid-acoplamento-coesao/executar.sh DemoPagamentoPendente
```

- **Resultado esperado:** 0/3, zero avisos pendentes. O pagamento impede a matrícula antes do envio.
- Separar o aviso preserva a dependência legítima da confirmação do pagamento.

### 18:45–20:00 · Recapitular sobre o código

- **Acoplamento:** a regra conhece os contratos de que precisa; a escolha do canal fica no `main`.
- **Coesão/S:** regra de matrícula e detalhes do envio têm papéis reconhecíveis.
- **O/L:** outro canal atende ao mesmo contrato e mantém expectativas válidas do consumidor.
- **I/D:** contratos pequenos expressam necessidades da regra; implementações atendem a eles.
- Pedir que o aluno localize uma mudança de integração que hoje obriga a alterar uma regra de negócio.
- Ponte curta para Clean Architecture e Hexagonal na próxima aula.

## Notas breves para a professora

- A falha é determinística e simulada. Não há requisições externas, credenciais, Spring ou banco; o programa não envia mensagens reais.
- Acessos e avisos pendentes ficam em memória. O exemplo não implementa reenvio, persistência, atomicidade nem garantias distribuídas; isso pertence à aula de assincronia.
- São três alunas distintas e um único curso. Nomes identificam as alunas apenas para reduzir o código.
- Usar o padrão observado na aula de tokens: explicar o modelo → pedir previsão → manter a entrada → alterar uma condição → executar → explicar a diferença. Primeiro cair o e-mail; depois trocar o canal; por último mudar o pagamento.

## Guia visual da revisão — 12 telas locais

A duração permanece 20 minutos. As telas 01–10 acompanham a teoria já descrita (capa + slides de conteúdo 01–09); 11–12 entram somente depois das execuções da prática. Não antecipar os resultados quando pedir a previsão. Arquivo portátil: `teoria.excalidraw`; prévias editáveis em SVG: `previas/index.html`. Importação e slides nativos online são etapas separadas.

| Tela | Pergunta para conduzir | Caminho para apontar | Resultado / cuidado |
|---|---|---|---|
| 01 · Capa | Que mudança vamos acomodar? | Pedido de novo canal → regra de acesso → detalhe de envio | Abrir tema antes da escola; acoplamento e coesão são critérios. |
| 02 · Regra | Qual condição realmente permite o acesso? | Ana/Bia/Clara → pagamento confirmado → acesso → aviso posterior | Três pagamentos iguais; aviso comunica a liberação. |
| 03 · Acoplamento | Onde tenho que editar para usar WhatsApp? | Pedido amarelo → `Email` no campo → `new Email` no construtor → chamada | Recortes reais de `MatriculasAcopladas`; regra de pagamento não mudou. |
| 04 · Coesão | Quais operações contribuem para o mesmo propósito? | Consultar/registrar azuis → matrícula; SDK/texto amarelo → comunicação | Separar propósitos sem converter cada método em classe. |
| 05 · S | Quem pede cada mudança? | Pedido Acadêmico → critério; pedido Comunicação → detalhe de envio | Coordenar a operação permanece no caso de uso. |
| 06 · D | Que tipos a regra conhece? | `Matriculas` → `Notificador`; `Email`/`WhatsApp` → contrato | Setas de dependência de código; não sequência de chamadas. |
| 07 · O | Qual linha muda para incluir outro canal? | Montagem com `Email(false)` → `WhatsApp()` → `Matriculas` preservada | Extensão do canal; não promessa de classe imutável para sempre. |
| 08 · L | Falha prevista e sucesso sem envio são equivalentes? | Aluna válida → envio, IOException prevista ou retorno sem efeito | Último caso quebra a promessa; assinatura não basta. |
| 09 · I | A matrícula precisa de estorno e nota? | Consumidor consulta → interface financeira hipotética → recorte `ConsultaPagamento` | Contrato orientado pela necessidade desse cliente. |
| 10 · Previsão | Quantos acessos nas duas versões? | Mesmas entradas → dois contadores interrogados | Esperar a previsão; resultados só no terminal. |
| 11 · Ordem acoplada | Qual linha não executou? | Confirmado → envio lança → `acessos.add` bloqueado | Depois de `DemoAcoplamento`: 0/3; apontar a ordem real. |
| 12 · Ordem tratada | Por que o acesso continua e o aviso fica pendente? | Acesso registrado → tentativa → `catch IOException` → pendência | Depois de `DemoDesacoplamento`: 3/3 e três pendências. Código com reticências é recorte simplificado; interface não causa resiliência sozinha. |
