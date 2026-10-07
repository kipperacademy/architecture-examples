# Aula 4 — Monólito modular

A aula mostra módulos de matrícula e cobranças no mesmo aplicativo. Cada módulo guarda seus dados e expõe um contrato para os outros; a comunicação é local e o sistema continua gerando um único artefato e um único deploy.

## Conceitos apresentados

### Monólito modular

Um único processo e deploy podem conter módulos separados por responsabilidade.

~~~mermaid
flowchart LR
  subgraph App[Uma aplicação e um deploy]
    Academico[Módulo acadêmico]
    Financeiro[Módulo financeiro]
  end
~~~

### Fronteira e contrato entre módulos

Matrículas consulta o contrato público de cobranças. Ela não abre a entidade interna nem altera diretamente o banco do módulo financeiro.

~~~mermaid
flowchart LR
  Matriculas[Módulo acadêmico] -->|pedido id| Contrato[Contrato: está confirmado?]
  Contrato --> Cobrancas[Módulo financeiro]
  Cobrancas --> Banco[(Dados de cobranças: dono financeiro)]
~~~

### Regra de matrícula

O resultado da consulta define se a aluna entra na lista de matriculadas; pagamentos pendentes não liberam acesso.

~~~mermaid
flowchart TD
  Pedido --> Consulta[Consultar status da cobrança]
  Consulta -->|confirmado| Matricula[Liberar matrícula]
  Consulta -->|pendente| Fim[Não matricular]
~~~

## Exemplo e transcrição

Java 21+. Partindo desta pasta, execute bash executar.sh modulos. A demo usa os pedidos de Ana e Bia e mostra a dependência entre os contratos dos módulos.

Leia a transcrição com timestamps em transcricao.md. Ela foi gerada automaticamente em português pelo ElevenLabs Scribe a partir da gravação FHD no Drive; não foi revisada palavra a palavra.
