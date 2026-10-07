# Aula 02 — Design Patterns na Prática

**Factory, Singleton, Strategy, Adapter e Dependency Injection · 30 minutos**

**Formato confirmado:** 5 minutos para cada padrão — Factory, Singleton, Strategy e Adapter — e 10 minutos de demonstração integrada. DI aparece na montagem explícita pelo construtor.

**Posição recomendada:** SOLID → Design Patterns → Clean/Hexagonal. A aula funciona sozinha: definir os conceitos e apresentar o contexto antes de usar classes ou regras do exemplo.

**Slides editáveis:** https://app.excalidraw.com/s/5pZP9SZcJC3/9VUYBPV17tF

**Áudio de preparação:** `preparacao-para-gravar.mp3`, 3min49s (228,8065 segundos). Texto ao lado; voz Lucas, Eleven Multilingual v2, conta contato@fernandakipper.com. Duração medida no arquivo exportado.

## Objetivo

Ao final, o aluno deve reconhecer quatro decisões diferentes: **criar um objeto, controlar sua instância, escolher um comportamento e adaptar uma interface**. Deve conseguir montar essas peças por construtor e seguir uma compra do início ao fim.

Não apresentar padrões como coleção de classes obrigatórias. Começar pelo problema que cada um resolve; nomear a estrutura e seu custo. Factory, Singleton, Strategy e Adapter podem colaborar, mas nenhum exige automaticamente os outros.

## Contexto do exemplo — apresentar no slide 04

Uma escola vende um curso por **R$ 100,00**. O checkout calcula o preço e solicita o pagamento. Há duas políticas: preço cheio ou **10% de desconto para Pix**, uma regra fictícia desta escola.

- **Entrada:** preço original, política escolhida e fornecedor escolhido na montagem.
- **Unidade interna:** centavos inteiros. R$ 100 = `10_000`; R$ 90 = `9_000`.
- **Integração legada:** API `charge(String amount, String currency)` espera reais como texto, por exemplo `"90.00"`, e moeda `"BRL"`.
- **Estado compartilhado:** um registro didático conta as compras concluídas nesta execução. Dois checkouts acessam o mesmo contador; ele não é banco de dados nem histórico persistente.
- **Resultado:** valor confirmado pelo colaborador de pagamento, exibido em centavos.
- **Ambiente:** todas as implementações são simulações locais. Não existe transação financeira ou chamada de rede.

Pergunta condutora: **como mudar a política de preço e o fornecedor sem espalhar escolhas de criação e conversões pelo checkout?**

## Plano da aula

| Tempo | Tema | Slides |
|---|---|---|
| 00:00–05:00 | Factory e contextualização da escola | 01–05 |
| 05:00–10:00 | Singleton: identidade, estado compartilhado e limites | 06–09 |
| 10:00–15:00 | Strategy e montagem por Dependency Injection | 10–12 |
| 15:00–20:00 | Adapter e colaboração entre os padrões | 13–16 |
| 20:00–30:00 | Demo Java integrada e fechamento | 17 → IDE/terminal → 18 |

## 00:00–05:00 · Factory

### 00:00–00:20 · Slide 01 — Capa

- Apresentar as quatro decisões: criação, instância, comportamento e integração.
- Explicar que os padrões serão vistos separadamente e depois trabalhando na mesma compra.
- Anunciar 20 minutos de conceitos e 10 de execução. Não presumir conhecimento da aula de SOLID.

### 00:20–00:50 · Slide 02 — O que é um design pattern?

- **Conceito:** solução de design recorrente para um problema em determinado contexto, com consequências e custos.
- Um padrão fornece vocabulário para discutir uma decisão; não é uma biblioteca, código pronto ou uma obrigação.
- A pergunta útil é “qual mudança quero acomodar?”. Nem todo `if` precisa virar padrão.

### 00:50–01:40 · Slide 03 — Factory: separar a criação do uso

- **Conceito:** concentrar a escolha e a construção de um objeto num ponto que fornece esse objeto ao consumidor.
- O consumidor pede um produto por um contrato. A criação conhece as classes concretas e sua montagem.
- O exemplo da aula é uma **Simple Factory**, com decisão em um método. Não chamar o `switch` de Factory Method do GoF: Factory Method usa um ponto de criação especializado por subclasses; Abstract Factory trata famílias de produtos relacionados.
- O `new` continua existindo. A mudança é onde a decisão de criação fica.

### 01:40–02:30 · Slide 04 — Apresentar a escola do zero

- Descrever produto, preço, operação de checkout, desconto Pix e resultado.
- Mostrar `10_000` centavos = R$ 100 e `9_000` = R$ 90.
- Avisar que os fornecedores são simulados. O nome legado representa uma API cujo formato já existe e que a aplicação precisa respeitar.
- Não entrar ainda em conversão: o aluno só precisa saber que haverá escolha de fornecedor e uma diferença de formato.

### 02:30–05:00 · Slide 05 — Factory aplicada ao pagamento

- `PagamentoFactory.criar(Fornecedor.LEGADO)` entrega um objeto do tipo `Pagamento`.
- Abrir mentalmente a caixa de criação: ela monta `new PagamentoLegadoAdapter(new SdkLegado())`. O Adapter será explicado no terceiro bloco; por enquanto, é a implementação entregue.
- `Fornecedor.LOCAL` escolhe `new PagamentoLocal()`.
- Mostrar a montagem no main: o resultado da Factory será passado ao Checkout. O Checkout não consulta a Factory nem decide qual fornecedor usar.
- Custo: a Factory conhece as implementações e precisa mudar ao adicionar uma opção. A vantagem é concentrar essa decisão; não alegar que adicionar fornecedor nunca exige editar código.

## 05:00–10:00 · Singleton

### 05:00–06:00 · Slide 06 — Uma instância, um ponto de acesso

- **Conceito:** a própria classe controla sua instanciação e fornece um ponto global de acesso à mesma instância.
- Uma variável estática sozinha não prova Singleton: observar também quem pode construir objetos.
- O escopo é a classe carregada naquela execução. Não existe unicidade automática entre servidores ou processos.
- No exemplo, `RegistroCompras` mantém um contador local. Queremos observar identidade e estado compartilhado; não é uma recomendação de armazenamento para uma loja real.

### 06:00–07:15 · Slide 07 — O mecanismo no código

- Abrir mentalmente três peças: construtor `private`, campo `private static final INSTANCIA` e `getInstance()` que retorna esse campo.
- O campo cria o objeto durante a inicialização da classe. Chamar `getInstance()` novamente não executa outro `new`.
- `final` impede trocar a referência; não torna o objeto imutável. O contador ainda muda.
- Não entrar em lazy loading, double-checked locking, reflection ou serialização nesta aula.

### 07:15–08:45 · Slide 08 — Duas referências, o mesmo contador

- Ana e Bia recebem `RegistroCompras.getInstance()`. Desenhar duas referências chegando a **um único objeto**, com o campo `quantidade` dentro dele.
- Ana conclui uma compra: 0 → 1. Bia conclui outra: 1 → 2. Ambas as referências leem 2.
- `registroAna == registroBia` compara identidade e resulta em `true`. Não são duas cópias sincronizadas.
- Antecipar a pergunta da demo: “o contador de Bia começa em zero ou já inclui a compra da Ana?”.

### 08:45–10:00 · Slide 09 — Compartilhar exige escolher o escopo

- Singleton não é pré-requisito para compartilhar um objeto: o main poderia criar uma classe comum uma vez e passar a mesma instância para dois consumidores.
- Aqui o main obtém o Singleton e o injeta no Checkout. `Checkout` não chama `getInstance()` escondido em `comprar`.
- O exemplo continua acoplado ao tipo concreto `RegistroCompras`; injetá-lo não elimina esse acoplamento. Um contrato seria uma evolução se fosse necessário substituir o registro.
- Estado mutável compartilhado pode vazar entre fluxos e dificultar isolamento. O contador desta demo é intencionalmente compartilhado.
- A inicialização estática da classe é coordenada pela JVM. Isso não torna `quantidade++` seguro em várias threads. A demo roda em uma única thread.
- Cada novo comando `java` começa outra execução com contador zero. Reiniciar o programa perde os dados; dois servidores teriam contadores separados.

## 10:00–15:00 · Strategy

### 10:00–11:15 · Slide 10 — Trocar um algoritmo por contrato

- **Conceito:** encapsular variações de um comportamento atrás de um contrato e permitir que o contexto use a alternativa recebida.
- Identificar os papéis: contexto que usa, contrato que descreve a operação, estratégias que implementam algoritmos.
- A seleção pode acontecer na montagem; não é obrigatório trocar a Strategy no meio de uma execução.
- Não basta duas classes terem a mesma assinatura: devem preservar o significado da operação e da unidade dos valores.

### 11:15–13:15 · Slide 11 — A política de preço

- `PoliticaPreco.calcular(precoCentavos)` devolve o total em centavos.
- `SemDesconto`: mantém `10_000`. `DescontoPix`: calcula 90% e devolve `9_000`.
- `Checkout` chama `politicaPreco.calcular(...)`; não tem um `if` para cada campanha.
- Mostrar a entrada igual nos dois caminhos e resultados diferentes. A diferença é proposital: mudou a regra de preço, não a integração.
- Custo: objetos e contratos extras. Uma variação simples que nunca muda pode continuar como uma função ou condição; usar Strategy quando separar as alternativas ajuda de fato.

### 13:15–15:00 · Slide 12 — Dependency Injection conecta as peças

- **Conceito:** receber uma dependência de fora, em vez de o consumidor escolher/criar essa dependência internamente.
- Mostrar `new Checkout(politicaPreco, pagamento, registro)` com as três dependências criadas acima. Ler o construtor e os campos.
- Quem instancia: o main, diretamente ou com ajuda da Factory. Quem usa: o Checkout.
- DI pode existir sem framework e sem interface. Aqui os contratos permitem substituir política e pagamento; a injeção entrega os objetos que cumprem esses contratos.
- Não confundir DI com Strategy: DI fornece o colaborador; Strategy organiza alternativas de um comportamento. Não confundir DI com inversão de dependência: receber uma classe concreta ainda pode acoplar a ela.

## 15:00–20:00 · Adapter

### 15:00–16:15 · Slide 13 — Compatibilizar interfaces

- **Conceito:** oferecer a interface esperada pelo consumidor traduzindo para uma interface existente diferente.
- Papéis: cliente, contrato esperado, adaptador e componente adaptado.
- A tradução pode envolver nomes de métodos, unidades, tipos de dados e resultados. O Adapter deve preservar o significado da operação.
- Uma classe que apenas repassa uma chamada idêntica não mostra bem o motivo de usar este padrão; por isso a demo terá uma incompatibilidade observável.

### 16:15–17:30 · Slide 14 — A incompatibilidade real

- Relembrar: aplicação usa centavos; SDK espera reais como texto.
- `9_000` centavos significa R$ 90. Se alguém só fizer `Integer.toString(9000)`, o SDK recebe `"9000"` reais.
- Perguntar quanto o fornecedor vai interpretar: **R$ 9.000**, cem vezes a intenção. Guardar a execução para o bloco prático.
- Não é um erro de compilação: os tipos permitem passar a String errada. A diferença é semântica, a unidade do valor.

### 17:30–19:00 · Slide 15 — O Adapter preserva o significado

- `PagamentoLegadoAdapter` implementa `Pagamento` e recebe `SdkLegado` pelo construtor.
- Entrada: `9000` centavos → `BigDecimal.valueOf(valorCentavos, 2)` → texto `"90.00"`.
- Chamada: `sdk.charge(valorReais, "BRL")`.
- Retorno: reais confirmados → deslocar duas casas → centavos para a aplicação.
- A transformação de ida e volta fica na borda. O Checkout não conhece `charge`, moeda ou representação em String.
- Explicar a causa precisa: o cálculo correto da unidade resolve o erro; o padrão organiza onde essa tradução vive.

### 19:00–20:00 · Slide 16 — Como trabalham juntos

- Factory cria o objeto de pagamento, inclusive sua dependência SDK.
- Strategy calcula o total segundo a política escolhida.
- DI entrega política, pagamento e registro ao Checkout.
- Adapter traduz a solicitação e a resposta do fornecedor.
- Singleton fornece o mesmo registro; após a confirmação, o Checkout incrementa seu contador.
- Separar montagem e execução: primeiro os objetos são construídos; depois `comprar` usa as dependências já recebidas.

## 20:00–30:00 · Demonstração integrada

### 20:00–20:30 · Slide 17 — Previsão

- Curso de R$ 100, Pix com 10% de desconto, fornecedor legado.
- Pedir o valor esperado: R$ 90, que equivale a 9.000 centavos.
- Perguntar o que acontece se o código apenas converter o inteiro em texto e enviar ao SDK.
- Antecipar a segunda previsão: após duas compras no mesmo programa, as referências do registro lerão 1 ou 2? Retomar em `DemoSingleton`.

### 20:30–21:30 · Expor a incompatibilidade

Abrir **somente** `pratica/DemoSemAdapter.java`. Mostrar a simulação do SDK em `SdkLegado.java`: `amount` é interpretado como reais.

```bash
bash executar.sh sem-adapter
```

Saída **esperada pela leitura do código**, ainda não executada nesta preparação:

```text
Intenção: 9000 centavos = R$ 90.00
SDK simulado recebeu: R$ 9000.00
Valor interpretado pelo SDK: R$ 9000
```

O programa aceita os dados, mas o fornecedor interpreta cem vezes o valor pretendido. É um erro intencional e inteiramente local.

### 21:30–23:15 · Montar a compra integrada

Abrir `pratica/DemoCompra.java` e ler de cima para baixo:

```java
int precoCursoCentavos = 10_000;
PoliticaPreco politicaPreco = new DescontoPix();
Pagamento pagamento = PagamentoFactory.criar(Fornecedor.LEGADO);
RegistroCompras registro = RegistroCompras.getInstance();
Checkout checkout = new Checkout(politicaPreco, pagamento, registro);
```

1. Entrada e regra escolhidas explicitamente.
2. Factory cria o pagamento. Abrir `PagamentoFactory.java` e mostrar o `new` real, inclusive o SDK entregue ao Adapter.
3. Voltar ao main: o Checkout recebe as três instâncias pelo construtor. Essa linha é DI.
4. Abrir `Checkout.java`: calcular pela Strategy, solicitar pagamento e registrar a compra após a confirmação.
5. Abrir `PagamentoLegadoAdapter.java`: mostrar conversão e chamada ao SDK. Não explicar toda a API de BigDecimal; focar na unidade do valor.

A Factory só aparece na montagem. A compra não fica buscando dependências globalmente.

### 23:15–24:00 · Executar os quatro padrões juntos — momento WOW

```bash
bash executar.sh compra
```

Saída esperada:

```text
Total calculado: 9000 centavos
SDK simulado recebeu: R$ 90.00
Pagamento confirmado: 9000 centavos
```

- O mesmo SDK agora recebe R$ 90 em vez de R$ 9.000.
- O valor confirmado vem do retorno do colaborador, traduzido pelo Adapter; não é só um placar fixo impresso pelo main.
- Reconstruir a causa: Strategy escolheu o total; Factory forneceu o objeto compatível; DI ligou as peças; Adapter preservou a unidade.

### 24:00–25:00 · Trocar somente a regra de preço

Abrir `DemoSemDesconto.java`. A única linha de comportamento que muda em relação a `DemoCompra` é:

```java
PoliticaPreco politicaPreco = new SemDesconto();
```

```bash
bash executar.sh sem-desconto
```

Esperado: `10000` centavos calculados, SDK recebe `R$ 100.00`, confirmação `10000` centavos.

- O preço original e o fornecedor permanecem os mesmos.
- O Checkout não ganhou outro condicional; recebeu outra estratégia.
- Ambos são válidos: mudamos a política de negócio de forma explícita.

### 25:00–26:00 · Trocar somente o fornecedor

Abrir `DemoOutroFornecedor.java`. Partir da política Pix e mudar a escolha:

```java
Pagamento pagamento = PagamentoFactory.criar(Fornecedor.LOCAL);
```

```bash
bash executar.sh outro-fornecedor
```

Esperado:

```text
Total calculado: 9000 centavos
Pagamento local recebeu: 9000 centavos
Pagamento confirmado: 9000 centavos
```

- Este colaborador já atende ao contrato em centavos e dispensa a tradução legada.
- Abrir a opção LOCAL na Factory. A escolha mudou na montagem; o algoritmo de preço e o Checkout continuam iguais.
- As demos separadas permitem comparar poucas linhas sem menus, argumentos de cenário ou várias versões misturadas na tela.

### 26:00–29:00 · Singleton dentro do mesmo fluxo

Abrir `DemoSingleton.java`. Cada checkout recebe explicitamente sua política, seu pagamento e a referência de registro.

```bash
bash executar.sh singleton
```

Antes de executar, pedir duas previsões: `registroAna == registroBia` e os dois totais ao final.

Saída esperada:

```text
Mesmo objeto? true
Total calculado: 9000 centavos
SDK simulado recebeu: R$ 90.00
Total calculado: 10000 centavos
Pagamento local recebeu: 10000 centavos
Compras vistas por Ana: 2
Compras vistas por Bia: 2
```

- A compra de Ana passa por Factory, Strategy e Adapter. A de Bia usa outra política e outro fornecedor. Ambas incrementam o mesmo Singleton, recebido por DI.
- Abrir `RegistroCompras`: o mesmo campo `quantidade` muda duas vezes. Não existe soma entre cópias.
- Rodar o comando novamente, se houver tempo: o total volta a 2, não cresce para 4, porque começou outra JVM.
- A diferença de valores mostra Strategy; o SDK em reais mostra Adapter; a criação concentrada mostra Factory; a identidade e o contador mostram Singleton. DI conecta tudo.

### 29:00–30:00 · Slide 18 — Recuperação e ponte

- Perguntar: “entrou um fornecedor que pede valor em outra unidade. Que parte muda?” Adapter e criação/montagem da nova opção; não a política de desconto.
- “Mudou a promoção?” Alterar/adicionar Strategy e escolhê-la na montagem.
- “O contador vale para outra JVM?” Não; o estado é local e temporário.
- “Preciso de uma Factory para todo construtor?” Não; justifique a decisão pelo problema de criação.
- Fechar: contratos e montagem explícita serão úteis para entender as fronteiras de Clean e Hexagonal. Essa ponte é opcional para o aluno; o entendimento desta aula é completo por si.

## Preparação da professora

- Abrir a pasta `02-design-patterns`; script funciona também por caminho completo.
- Deixar os cinco mains em abas separadas e mostrar somente o cenário do momento.
- Arquivos principais para explicar: `DemoCompra`, `PagamentoFactory`, `Checkout`, `DescontoPix`, `PagamentoLegadoAdapter`, `SdkLegado`, `RegistroCompras` e `DemoSingleton`.
- Poucos comentários, sem framework, sem Maven ou dependências externas.
- As fontes desta revisão foram preparadas e lidas; não foram compiladas nem executadas. Todos os resultados acima são previsões derivadas do código.

## Limites didáticos

O SDK é fictício, local e sempre confirma o valor recebido. O exemplo não demonstra integração, autorização ou captura financeira reais. O desconto usa divisão inteira e trunca frações de centavo; o preço fixo de R$ 100 evita esse caso no vídeo. Valores negativos, grandes quantias, moedas adicionais, erros do provedor e concorrência ficaram fora do recorte. Não usar este código como motor financeiro de produção.

A Factory mostrada é Simple Factory. Factory Method e Abstract Factory só são diferenciadas verbalmente para evitar confusão de nomes; não são implementadas. Singleton tem bloco próprio e participa da demo integrada. O contador serve para observar estado compartilhado em uma única thread; não é persistente, distribuído ou seguro para incremento concorrente. A construção é controlada para uso normal da classe; não abordamos mecanismos que contornam esse controle.

## Referências

- [Martin Fowler — Inversion of Control Containers and the Dependency Injection pattern](https://martinfowler.com/articles/injection.html): separar configuração e uso; injeção por construtor.
- [Gamma, Helm, Johnson e Vlissides — Adapter, trecho do livro publicado pela InformIT](https://www.informit.com/articles/article.aspx?p=1398600): compatibilização de interfaces.
- [Entrevista com autores de Design Patterns](https://www.informit.com/articles/article.aspx?p=1404056): padrões como vocabulário, discussão de Factory, DI e ressalvas sobre Singleton.
- [Java SE 21 — Comparator](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Comparator.html): referência de API que recebe comportamento de comparação por contrato; analogia de Strategy, não classificação declarada pela documentação.

Diagramas e código são exemplos didáticos próprios, não reproduções dos exemplos das fontes.

- [Java Language Specification 12.4.2](https://docs.oracle.com/javase/specs/jls/se21/html/jls-12.html#jls-12.4.2): inicialização de classes; não confundir publicação da instância com sincronização de seus métodos mutáveis.
