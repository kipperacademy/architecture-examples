# Aula 04 — Monólito Modular

**Título Pora:** Monólito Modular: Como Organizar Domínios, Módulos, Banco de Dados e Transações.
**Prazo editorial:** 20/10/2026. **Duração proposta:** 25 min: 10 de conceitos, 12 de prática, 3 de fechamento. Não é uma duração já aprovada.

## Objetivo e contexto

O aluno deve conseguir separar capacidades de negócio dentro de uma aplicação implantada como uma unidade, identificar quem pode acessar cada dado e explicar o limite de uma transação local. Apresentar a escola do zero: vende cursos, registra recebimentos e libera matrícula. Financeiro conhece a confirmação do pedido; Acadêmico decide a matrícula. O exemplo não faz cobrança externa.

Pergunta condutora: **como separar responsabilidades sem criar serviços de rede — e sem perder a consistência entre duas escritas?**

## 00:00–10:00 · Conceitos e diagramas

1. **00:00–01:00 · Slide 01 — Capa e objetivo.** Apresentar fronteiras, dados e transações. Explicar que a decisão de modularizar é diferente da decisão de distribuir processos. Não pressupor as aulas anteriores.
2. **01:00–02:00 · Slide 02 — Uma unidade de deploy.** Monólito: a aplicação é construída e implantada como uma unidade. Pode ter vários módulos, várias réplicas e um banco externo. Modular: capacidades têm interfaces e responsabilidades explícitas. Isso exige regras no código; nomes de pastas sozinhos não impedem dependências indevidas.
3. **02:00–03:30 · Slide 03 — Fronteira por capacidade.** Apresentar a escola. Financeiro confirma pedidos; Acadêmico registra acesso. Ambos podem conter regras e persistência próprias. Não confundir módulo com camada controller/service/repository. Uma camada técnica pode existir dentro de cada módulo.
4. **03:30–05:00 · Slide 04 — Dependência permitida.** Apontar `Matriculas → Cobrancas.estaConfirmado(pedido)`. O contrato retorna uma informação necessária, não o mapa mutável inteiro. Mostrar o `private` em `confirmadas`. O acoplamento ao contrato existe e é escolhido. Pacotes Java não protegem automaticamente todos os subpacotes; usar visibilidade, módulos JPMS ou verificações de arquitetura conforme a necessidade.
5. **05:00–06:30 · Slide 05 — Dono dos dados.** Um banco físico pode ter tabelas com donos distintos. O código de Acadêmico não escreve diretamente nos recebimentos. Prefixos das tabelas desta demo documentam os donos; não implementam isolamento por permissões. Um schema por módulo também não equivale a um banco por serviço. Evitar joins operacionais indiscriminados que tornem o layout interno um contrato público; relatórios podem precisar de uma solução explícita.
6. **06:30–08:30 · Slide 06 — Transação local.** Duas alterações relacionadas precisam confirmar juntas. Mostrar BEGIN → recebimento → matrícula → COMMIT; falha antes do commit → ROLLBACK. Na demo, uma conexão e um banco participam da transação. Estar no mesmo processo não cria atomicidade automaticamente. O caso de uso de aplicação define a unidade de trabalho e coordena os módulos participantes.
7. **08:30–10:00 · Slide 07 — Faça a previsão.** Uma única vaga, já ocupada por Ana. Tentar registrar recebimento de Bia e matriculá-la na vaga 1. O banco rejeita a segunda escrita por uma restrição UNIQUE. Perguntar: **o recebimento de Bia continua salvo?** Separar as duas execuções, com a mesma entrada e a mesma falha.

## 10:00–22:00 · Prática

### 10:00–14:00 · Seguir a fronteira em Java

Abrir `pratica/DemoModulos.java`, `pratica/academico/Matriculas.java` e `pratica/financeiro/Cobrancas.java`. Instanciar Financeiro, injetar no Acadêmico, confirmar somente o pedido de Ana, pedir as duas matrículas e ler o estado. Executar da **pasta do curso**:

```sh
bash 04-monolito-modular/executar.sh modulos
```

Resultado conferido: `Matrículas: [Ana]`. A demo é de fronteira e visibilidade, com coleções em memória. Não representa uma implementação completa de DDD, proteção automatizada contra ciclos ou banco transacional.

Perguntar o que aconteceria se Acadêmico recebesse a coleção mutável de recebimentos. Ele poderia alterar dados que Financeiro deveria controlar. Na demo, o campo é privado e a saída das matrículas é uma cópia imutável. A garantia apresentada é essa, sem alegar isolamento completo de todos os módulos.

### 14:00–20:30 · Observar uma transação real

Abrir `sql/estrutura.sql`: explicar a vaga única e as duas tabelas. Depois abrir `transacao.py` só na região `BEGIN → INSERT → INSERT → COMMIT/ROLLBACK`.

**Por que este trecho usa Python?** É apenas o driver de SQLite da biblioteca padrão, para rodar uma transação real sem baixar JDBC ou subir serviços. A primeira demo permanece Java. Os arquivos SQL servem de apoio visual; o runner executa as mesmas operações, tratando a exceção explicitamente. Não apresentar Python como requisito arquitetural.

```sh
bash 04-monolito-modular/executar.sh sem-transacao
bash 04-monolito-modular/executar.sh com-transacao
```

Resultados conferidos:

| Cenário | Recebimentos | Matrículas |
|---|---|---|
| Autocommit; falha na segunda escrita | pedido-ana, pedido-bia | Ana |
| Transação; rollback após a mesma falha | pedido-ana | Ana |

Cada comando cria um banco SQLite novo em memória; não reaproveita estado anterior. O banco é real, embora efêmero. A primeira escrita fica confirmada no autocommit. No segundo cenário, a exceção leva ao rollback da unidade de trabalho. A mudança é o limite da transação, não uma nova regra de vaga.

**Limite importante:** o registro de recebimento é uma linha local fictícia. Rollback de SQL não estorna uma cobrança feita por HTTP num provedor. Essa distinção prepara a aula de distribuição. A demo mostra atomicidade; não mede durabilidade em disco nem testa isolamento concorrente.

### 20:30–22:00 · Slide 08 — Onde a garantia termina

Desenhar a fronteira do banco ao redor das duas tabelas. Colocar um provedor de pagamento fora dela. Traçar uma chamada que atravessa essa fronteira. Uma transação local não alcança automaticamente essa operação externa. Se houver necessidade de consistência entre participantes independentes, será preciso outra coordenação.

## 22:00–25:00 · Slide 09 — Recuperação e decisão

- “Trocar tudo para HTTP melhora a organização?” Só se houver um problema que justifique a fronteira de processo e seus custos.
- “Posso ter dez módulos e um deploy?” Sim. A divisão lógica e a unidade de implantação são decisões diferentes.
- “Dois INSERT no mesmo método são atômicos?” Não necessariamente; localizar BEGIN/COMMIT e a conexão participante.
- Exercício: acrescentar módulo Comunicação que recebe uma solicitação de aviso, sem obter acesso direto às tabelas de matrícula. Primeiro desenhar a dependência; depois justificar a interface.

## Preparação

Abrir os três arquivos Java e o bloco SQL antes de gravar. Não percorrer árvore de arquivos durante a explicação. Executar as três demos a partir da pasta do curso. A transação só cobre a segunda metade; não alegar que o Java anterior já usa SQLite.

## Fontes

- [Spring Modulith — Fundamentals](https://docs.spring.io/spring-modulith/reference/fundamentals.html): interfaces, implementação interna e dependências de módulos; não é dependência da demo.
- [JDBC Connection](https://docs.oracle.com/en/java/javase/21/docs/api/java.sql/java/sql/Connection.html): contraparte Java para autocommit, commit e rollback.
- [SQLite — Transactions](https://www.sqlite.org/lang_transaction.html): transação executada pelo runner.
