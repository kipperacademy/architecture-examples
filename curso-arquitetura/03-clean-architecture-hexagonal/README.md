# Aula 3 — Clean Architecture e arquitetura hexagonal

A gravação compara duas formas de manter as regras da aplicação independentes de detalhes externos. O exemplo é um fluxo de matrículas com entradas por CSV ou terminal e repositórios em memória ou arquivo.

## Conceitos apresentados

### Clean Architecture

Entidades e casos de uso concentram regras. Frameworks, entrada, armazenamento e serviços externos ficam nas bordas; dependências apontam para o núcleo.

~~~mermaid
flowchart LR
  Externo[Entrada e armazenamento] -->|implementa contratos| Casos[Casos de uso]
  Casos --> Entidades[Entidades e regras]
~~~

### Entidade e caso de uso

A entidade guarda os dados do pedido. MatricularAluno coordena a ação de matrícula usando a porta de repositório, sem decidir se os dados irão para arquivo ou memória.

~~~mermaid
flowchart LR
  Caso[MatricularAluno: executar] --> Entidade[Pedido e status]
  Caso --> Repositorio[Contrato RepositorioMatriculas]
~~~

### Arquitetura hexagonal: portas e adaptadores

Portas descrevem as ações que o núcleo oferece ou necessita. Adaptadores traduzem CSV, terminal, arquivo e memória para esses contratos.

~~~mermaid
flowchart LR
  CSV[Entrada CSV] --> PortaEntrada[Porta de entrada]
  Terminal[Entrada terminal] --> PortaEntrada
  PortaEntrada --> Aplicacao[Matricular]
  Aplicacao --> PortaSaida[Porta RepositorioMatriculas]
  PortaSaida --> Memoria[Adaptador em memória]
  PortaSaida --> Arquivo[Adaptador em arquivo]
~~~

### Troca de adaptador

O main escolhe a implementação e conecta as peças; a regra de matrícula permanece igual quando muda a entrada ou o armazenamento.

~~~mermaid
flowchart LR
  Main --> Aplicacao[MatricularAluno]
  Main --> Entrada[CSV ou terminal]
  Main --> Saida[Memória ou arquivo]
  Entrada --> Aplicacao
  Aplicacao --> Saida
~~~

## Exemplos e transcrição

Java 21+. Partindo desta pasta, execute bash executar.sh clean-memoria, bash executar.sh clean-arquivo, bash executar.sh hex-terminal Ana CONFIRMADO ou bash executar.sh hex-csv. O CSV de entrada está em dados/pedidos.csv; a demo de arquivo grava em dados/matriculas.txt.

Leia a transcrição com timestamps em transcricao.md. Ela foi gerada automaticamente em português pelo ElevenLabs Scribe a partir da gravação FHD no Drive; não foi revisada palavra a palavra.
