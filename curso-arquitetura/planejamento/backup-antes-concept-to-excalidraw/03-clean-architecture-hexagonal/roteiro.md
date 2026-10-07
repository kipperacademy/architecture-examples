# Aula 03 — Clean Architecture e Arquitetura Hexagonal

**Ports, Adapters e Inversão de Dependência · 20 minutos · revisão 2**

Roteiro de apoio: conceitos, ordem e indicações de tela. A aula deve funcionar para quem chegou diretamente a este vídeo. Não pressupor contato com aulas anteriores, nem apresentar matrícula ou nomes das classes antes de contextualizar a escola.

## Objetivo

Compreender os dois modelos arquiteturais antes de aplicá-los. Clean organiza políticas e detalhes em níveis de responsabilidade; Hexagonal organiza as conversas entre o núcleo e o exterior. São leituras compatíveis da mesma aplicação.

**Slides editáveis:** https://app.excalidraw.com/s/5pZP9SZcJC3/9nu1j8fbpQ3

**Áudio existente:** `preparacao-para-gravar.mp3` (3min42s) corresponde à versão 1. Ainda pressupõe continuidade da escola e não acompanha a nova introdução conceitual. Esta revisão solicitada altera slides e sincroniza o roteiro; o áudio não foi regenerado.

## Plano de tela

| Tempo | Bloco | Slides / código |
|---|---|---|
| 00:00–05:00 | Fundamentos de Clean + contextualização do exemplo | Slides 01–09 |
| 05:00–10:00 | Prática de Clean | Slide 10 → IDE → terminal |
| 10:00–15:00 | Fundamentos de Hexagonal + aplicação ao exemplo | Slides 11–15 |
| 15:00–20:00 | Prática de Hexagonal e fechamento | Slide 16 → IDE → terminal → slide 17 |

## 00:00–05:00 · Clean Architecture

### 00:00–00:15 · Slide 01 — Apresentar o tema

- Promessa: entender onde colocar responsabilidades e quem pode conhecer quem no código.
- Anunciar os quatro blocos de cinco minutos. Primeiro o modelo mental; depois a aplicação em Java.

### 00:15–00:45 · Slide 02 — O modelo geral

- **Clean Architecture:** organizar a aplicação para preservar políticas de negócio quando mudam mecanismos externos.
- Política descreve o que o negócio faz ou permite. Mecanismo descreve como uma tecnologia executa uma tarefa.
- Percorrer o mapa de fora para dentro: frameworks/drivers, adaptadores, casos de uso e entidades. Os retângulos aninhados representam as mesmas fronteiras frequentemente desenhadas como círculos.
- Esse mapa é uma divisão de responsabilidades; não determina um número obrigatório de pastas ou processos.

### 00:45–01:15 · Slide 03 — Entidades

- Conceitos do domínio que reúnem estado e comportamento relevante ao negócio.
- Regras e condições válidas permanecem compreensíveis sem conhecer o banco ou a interface.
- Explicar estado versus comportamento apontando o desenho. Uma entidade pode ter várias operações coesas.
- “Entidade” neste modelo não significa necessariamente uma tabela ou classe anotada por um ORM.

### 01:15–01:50 · Slide 04 — Casos de uso

- Representam intenções que a aplicação realiza. Coordenam entidades e colaboradores para atingir um resultado.
- Percorrer o fluxo: receber intenção/dados, aplicar regras do domínio, solicitar operações externas quando necessário.
- Distinguir regra de domínio de coordenação de uma operação específica da aplicação. Nenhuma das duas precisa implementar protocolo HTTP ou acesso SQL.

### 01:50–02:15 · Slide 05 — Adaptadores de interface

- Traduzem entre o formato externo e os dados necessários pela aplicação.
- Um controller interpreta um request e chama um caso de uso. Um presenter pode adaptar o resultado para a exibição.
- A tradução também pode existir na persistência. Não transformar request, resposta de SDK ou linha de banco no modelo interno por conveniência.

### 02:15–02:35 · Slide 06 — Frameworks e drivers

- Mecanismos na borda: servidor web, interface gráfica, driver de banco, sistema de arquivos e SDKs.
- Os adaptadores usam essas tecnologias para atender às necessidades internas.
- A arquitetura limita o impacto da substituição; não elimina o trabalho de implementar e integrar um mecanismo novo.

### 02:35–03:20 · Slide 07 — Regra de dependência

- As dependências de código apontam para dentro: detalhes externos conhecem abstrações/políticas internas; o núcleo não cita detalhes externos.
- Setas representam conhecimento de tipos/imports. Não são uma sequência obrigatória de chamadas em execução.
- Apontar o import de persistência dentro da regra e explicar a consequência: mudar a biblioteca passa a exigir alterações naquela regra.
- Apenas mover esse arquivo para uma pasta chamada domínio não muda sua dependência.

### 03:20–04:00 · Slide 08 — Inversão e injeção

- Para solicitar algo externo, o caso de uso conhece um contrato definido pelas necessidades da aplicação. O adaptador externo implementa esse contrato.
- Mostrar o contraste: em execução, a solicitação chega ao banco; no código, a implementação depende da abstração interna.
- Injeção significa entregar o colaborador pelo construtor. Inversão significa orientar as dependências pelo contrato da política. Uma pode existir sem a outra.

### 04:00–05:00 · Slide 09 — Contextualizar a escola do zero

- **Sistema:** uma escola vende acesso a um curso e recebe pedidos de matrícula.
- **Entrada:** nome da aluna e situação do pagamento. Neste exemplo, o status já chega conhecido; não há integração real com cobrança.
- **Regra:** só registrar matrícula com pagamento confirmado.
- **Dados:** Ana confirmada, Bia pendente, Clara confirmada.
- **Resultado esperado:** Ana e Clara registradas; Bia ainda não pode entrar.
- **Desafio:** trocar o armazenamento sem reescrever a decisão sobre pagamento. Só agora apresentar os nomes `Pedido`, `MatricularAluno` e repositório, na transição para a IDE.

## 05:00–10:00 · Prática de Clean Architecture

### 05:00–05:30 · Slide 10 — Fazer a previsão

- Mesmos três pedidos, duas formas de salvar.
- Perguntar: “depois de criar outra instância do repositório, quais nomes ela vai encontrar?”
- Esperar a previsão antes de mostrar o terminal.

### 05:30–06:30 · IDE — Localizar a regra

Abrir, nessa ordem:

1. `pratica/dominio/Pedido.java`: uma condição; pagamento confirmado.
2. `pratica/aplicacao/MatricularAluno.java`: retorno antecipado do pendente; chamada `repositorio.salvar(aluna)`.
3. `pratica/aplicacao/RepositorioMatriculas.java`: contrato de salvar e listar. `listar` permite observar o estado nesta demo.

Não percorrer todos os arquivos na árvore. Mostrar que os imports do caso de uso não incluem `Path`, `Files` ou uma classe de armazenamento.

### 06:30–07:30 · DemoCleanMemoria

- Abrir `pratica/demos/DemoCleanMemoria.java` inteiro.
- Ler a montagem: instanciar `RepositorioEmMemoria`; passar essa instância a `new MatricularAluno(repositorio)`.
- Mostrar as três chamadas explícitas. As entradas já chegam convertidas em tipos da aplicação nesta primeira demonstração.
- Executar, a partir da pasta da aula:

```bash
bash executar.sh clean-memoria
```

Saída **esperada**, não registrada como execução desta revisão:

```text
Matrículas salvas: [Ana, Clara]
Nova instância: []
```

A coleção pertence à instância em memória. Outra instância tem outra coleção; Bia nem chegou ao repositório.

### 07:30–09:15 · DemoCleanArquivo — Momento WOW

- Abrir `pratica/demos/DemoCleanArquivo.java` ao lado da anterior.
- Destacar a troca para `new RepositorioEmArquivo(arquivo)` e a informação de caminho que só a borda precisa conhecer.
- Mostrar que os mesmos três pedidos chegam ao mesmo `MatricularAluno`.
- Executar:

```bash
bash executar.sh clean-arquivo
```

Saída esperada em um arquivo inicialmente ausente:

```text
Matrículas salvas: [Ana, Clara]
Nova instância: [Ana, Clara]
Arquivo real: .../dados/matriculas.txt
```

- Abrir **o arquivo real** `dados/matriculas.txt` na IDE. Duas linhas: Ana e Clara.
- **Surpresa:** o novo objeto recupera as matrículas anteriores, sem mudar a decisão de negócio. A persistência vem da implementação com `Files`, não da existência da interface.
- Apontar só `salvar` e `listar` do adaptador; não explicar cada linha de I/O durante a aula.

### 09:15–10:00 · Explicar a causa e fazer a ponte

- A mudança ficou na implementação e na montagem externa. Domínio e caso de uso permaneceram iguais.
- As demos usam código compartilhado de verdade, não duas cópias equivalentes da regra.
- Ponte: “agora trocamos onde guardamos. E se a escola quiser receber centenas de pedidos por uma planilha?”

## 10:00–15:00 · Arquitetura Hexagonal

### 10:00–10:50 · Slide 11 — O modelo geral

- **Hexagonal, ou Ports and Adapters:** organizar uma fronteira explícita entre o núcleo da aplicação e os agentes/tecnologias externos.
- No interior ficam casos de uso e regras. Portas definem as conversas na fronteira; adaptadores traduzem as tecnologias que participam delas.
- Percorrer quem pode acionar o núcleo e o que o núcleo pode solicitar. O desenho é conceitual, sem depender da escola.
- Os seis lados são um recurso visual; não exigem seis portas, microsserviços ou uma topologia de deploy.

### 10:50–11:40 · Slide 12 — Porta de entrada

- Define uma capacidade que a aplicação oferece ao exterior, com uma operação e seus dados.
- Um agente externo inicia a interação; o caso de uso realiza a operação. A porta não exige HTTP, nem é uma porta TCP.
- Uma interface Java é uma forma de expressá-la, não a definição inteira do conceito. A conversa também inclui o significado dos dados e resultados.
- Quem chama pode receber uma resposta: entrada/saída descreve quem inicia, não o sentido único dos dados.

### 11:40–12:30 · Slide 13 — Porta de saída

- Contrato que expressa uma necessidade da aplicação perante um colaborador externo, por exemplo salvar ou consultar dados.
- O núcleo inicia essa conversa; um adaptador atende ao contrato usando uma tecnologia.
- A operação deve expressar a necessidade do negócio/aplicação sem obrigar o núcleo a conhecer um fornecedor.
- Uma consulta retorna dados e ainda assim pode ser uma porta de saída.

### 12:30–13:35 · Slide 14 — Adaptadores

- Traduzem protocolos e formatos para uma conversa definida pela porta.
- Comparar HTTP/request e CSV/linhas: adaptadores diferentes acionam a mesma operação interna.
- O que varia é a tradução; a decisão de negócio permanece no núcleo. Assim o comportamento da aplicação pode ser acionado sem depender de uma única interface de usuário.
- Também existem adaptadores nas portas de saída; a lógica de acesso ao arquivo ou banco pertence a eles.

### 13:35–15:00 · Slide 15 — Aplicar à escola

- Relembrar o contexto em uma frase antes dos nomes: a escola recebe nome + pagamento e só registra os confirmados.
- Entrada: `Matricular.executar(nome, pagamento)`, implementada por `MatricularAluno`; terminal e CSV chamam essa porta.
- Saída: `RepositorioMatriculas`, implementada pelos repositórios em memória e arquivo.
- `Pedido` guarda o critério de elegibilidade; o caso de uso coordena a decisão e a persistência.
- Previsão para a prática: mudar de terminal para CSV não deveria permitir que Bia, pendente, escape da regra.
- O main montará os objetos e passará cada colaborador ao construtor. Não é preciso framework para estabelecer essas fronteiras.

## 15:00–20:00 · Prática de Hexagonal

### 15:00–15:30 · Slide 16 — Previsão

- Perguntar: “se Bia chegar pelo CSV, ela vai conseguir escapar da regra do pagamento?”
- Mostrar `dados/pedidos.csv` com os mesmos três pedidos, antes da execução.

### 15:30–16:45 · DemoHexagonalTerminal

- Abrir `pratica/demos/DemoHexagonalTerminal.java`. Ler as três instanciações; o tipo da variável do caso de uso é `Matricular`.
- Mostrar `EntradaTerminal.receber`: converte argumentos, chama porta e apresenta o retorno.
- Executar as mesmas pessoas, uma por invocação:

```bash
bash executar.sh hex-terminal Ana CONFIRMADO
bash executar.sh hex-terminal Bia PENDENTE
bash executar.sh hex-terminal Clara CONFIRMADO
```

Resultados esperados: Ana `true` e `[Ana]`; Bia `false` e `[]`; Clara `true` e `[Clara]`. Cada comando cria um processo com memória nova, portanto as listas **não são acumuladas**.

### 16:45–18:15 · DemoHexagonalCsv — Momento WOW

- Abrir `pratica/demos/DemoHexagonalCsv.java`.
- Destacar o mesmo `new MatricularAluno(repositorio)` sendo recebido por `new EntradaCsv(matricular)`.
- Mostrar a transformação em `EntradaCsv.importar`: linha → campos → enum → chamada. Não existe uma segunda condição de pagamento nesse adaptador.
- Executar o lote inteiro:

```bash
bash executar.sh hex-csv
```

Saída esperada:

```text
Ana | matrícula liberada: true
Bia | matrícula liberada: false
Clara | matrícula liberada: true
Matrículas salvas: [Ana, Clara]
```

- **Surpresa:** o sistema ganhou entrada em lote e manteve a mesma decisão sobre cada pedido. A regra não foi copiada para o importador.
- Voltar por um instante ao `MatricularAluno`: é exatamente o mesmo arquivo da primeira metade.

### 18:15–19:15 · Reconstruir o caminho de Bia

- A linha do CSV é válida. O adaptador a converte e chama a porta normalmente.
- `Pedido.permiteMatricula()` devolve falso. O caso de uso retorna antes de salvar.
- Não confundir rejeição de negócio com erro de leitura do arquivo. Uma falha de I/O é outro problema; interfaces não a eliminam.
- Explicar a independência das duas trocas: entrada de lote pode ser combinada com o repositório de arquivo usando o mesmo construtor; guardar essa combinação como exercício, sem uma quinta demo escondendo o foco.

### 19:15–20:00 · Slide 17 — Fechamento

- Clean: as políticas não conhecem os detalhes externos.
- Hexagonal: portas nomeiam conversas; adaptadores traduzem o mundo externo.
- Injeção monta os objetos; inversão orienta quem depende de quem.
- Pergunta de recuperação: “para adicionar uma entrada HTTP, onde ficariam a conversão do request e a regra do pagamento?” Resposta esperada: conversão no adaptador; decisão no domínio acionado pelo caso de uso.
- Exercício opcional: combinar CSV e arquivo modificando somente a montagem, e explicar por que `MatricularAluno` não precisa mudar.

## Preparação da gravação

- Abrir a pasta desta aula, não a raiz do curso. O script também funciona por caminho completo e localiza sua própria pasta.
- Java 21+; abrir os quatro mains em abas separadas, com fonte suficiente para caberem na tela.
- Conferir os três pedidos originais em `dados/pedidos.csv`; se quiser começar do zero, apagar somente a saída `dados/matriculas.txt` de uma execução anterior.
- Cada demo mostra uma situação. Não juntar as quatro em um menu dentro de `Demo.java`.
- Os resultados acima foram deduzidos da leitura dos fontes; os novos exemplos não foram compilados nem executados nesta preparação.

## Limites do exemplo — lembretes para a professora

Pagamento é uma entrada local já conhecida, não uma consulta a um provedor real. Nome identifica aluna apenas para simplificar a demo. Arquivo é uma implementação didática, sem transação, controle de concorrência ou persistência de produção. O CSV tem duas colunas separadas por ponto e vírgula, sem cabeçalho ou campos entre aspas; não é um importador CSV genérico. Erro de formato interrompe o lote, que é sequencial e não atômico. Esses detalhes não devem virar novas digressões dentro dos cinco minutos.

## Referências

- [Robert C. Martin — The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html): regra de dependência, políticas, casos de uso e fronteiras.
- [Alistair Cockburn — Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture): dentro/fora, portas, adaptadores e entrada em lote.
- [Fernanda — Arquitetura Hexagonal com Java](https://www.youtube.com/watch?v=UKSj5VJEzps): continuidade didática com diagrama antes da IDE e separação dos detalhes de persistência.

O código e os diagramas desta aula são um exemplo didático próprio, inspirado nesses princípios; não uma reprodução literal dos exemplos das fontes.
