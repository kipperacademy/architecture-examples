# Aula 06 — Como Construir Sistemas Escaláveis

**Título Pora:** Como Construir Sistemas Escaláveis: Cache, CDN, Load Balancing, Rate Limiting e Stateless.
**Prazo editorial:** 29/10/2026. **Duração proposta:** 30 min: 13 de conceitos, 14 de prática, 3 de fechamento.

## Objetivo e contexto

O aluno deve localizar o recurso pressionado antes de escolher uma técnica e prever o custo introduzido por ela. A escola publica um catálogo de cursos e recebe muitas consultas repetidas ao mesmo preço. Uma aluna também navega autenticada entre pedidos. Catálogo público, sessão privada e finalização de compra têm necessidades distintas; não tratar todo dado como igualmente cacheável.

## 00:00–13:00 · Conceitos

1. **Slide 01, 00:00–01:00 — Capa.** Escalar é sustentar mais carga dentro dos objetivos de serviço. Antes de multiplicar instâncias, medir requisições, latência, erros e saturação. Nesta aula contaremos operações, sem inventar benchmark de tempo.
2. **Slide 02, 01:00–02:30 — Localizar o gargalo.** Cinco leituras repetidas chegam ao catálogo. Se o trabalho caro está na origem, mais servidores web podem aumentar a pressão no mesmo lugar. Usar a pergunta “qual recurso esta técnica poupa?”. Escala vertical aumenta recursos de uma instância; horizontal distribui entre instâncias. Há limites e custos em ambas.
3. **Slide 03, 02:30–04:30 — Cache.** Guarda uma cópia reaproveitável. Miss consulta a origem e preenche; hit usa a cópia. Isso reduz consultas, mas pode servir valor antigo. TTL limita o tempo de reutilização segundo uma política; invalidação remove a cópia. A demo usará invalidação explícita, sem TTL. Cache não deve substituir uma verificação autoritativa de preço/estoque na compra quando a regra exige valor atual.
4. **Slide 04, 04:30–06:00 — CDN.** Distribui conteúdo por pontos próximos dos clientes, com cache conforme regras. A imagem pública do curso pode ser servida na borda; isso não remove automaticamente consultas da API de matrícula. Mostrar hit na borda e miss indo à origem. Conteúdo privado exige política apropriada; não cachear resposta personalizada como pública.
5. **Slide 05, 06:00–08:00 — Load balancing.** Distribui requisições entre alvos disponíveis. Mostrar A e B recebendo a mesma rota. Health checks ajudam a selecionar alvos; não garantem que cada operação terá sucesso. Um banco compartilhado pode continuar saturado. Não usar duas chamadas manuais a objetos como prova de um balanceador implantado.
6. **Slide 06, 08:00–10:00 — Stateless.** A réplica não precisa de estado local de sessão de pedidos anteriores para atender ao próximo pedido. O sistema ainda tem estado: sessão pode estar num armazenamento compartilhado ou outra representação apropriada. Sticky sessions podem manter afinidade, mas preservam dependência daquela réplica. Trocar/reiniciar a réplica revela o problema.
7. **Slide 07, 10:00–12:00 — Rate limiting.** Limita admissões por chave e intervalo. Mostrar limite de três por cliente por minuto. Excesso pode retornar HTTP 429 e informação sobre nova tentativa. Isso protege capacidade; não a cria. Limite local de três em cada réplica não é limite global de três. Janela fixa permite rajadas na virada da janela; não apresentá-la como solução universal.
8. **Slide 08, 12:00–13:00 — Previsão.** “Cinco consultas iguais fazem quantas leituras na origem? Depois de mudar o preço, o cache muda sozinho?” Esperar a resposta antes de abrir o terminal.

## 13:00–27:00 · Prática

Todos os comandos partem da **pasta do curso**. Demos independentes, sem rede e sem números aleatórios.

### 13:00–19:00 · Cache e dado antigo

Abrir `Catalogo.java`, `CachePreco.java` e os dois mains. Mostrar que o contador é incrementado dentro da operação da origem, não um número colocado na saída.

```sh
bash 06-sistemas-escalaveis/executar.sh DemoSemCache
bash 06-sistemas-escalaveis/executar.sh DemoCache
```

Resultados conferidos: sem cache, cinco consultas; com cache, uma. Após mudar origem de `10000` para `12000` centavos, a leitura ainda retorna `10000`. Após `invalidar()`, retorna `12000` e a contagem chega a duas. O cache foi mais econômico e ficou temporariamente desatualizado: os dois efeitos vêm do mesmo mecanismo.

### 19:00–23:30 · Estado e réplicas

Abrir um main por vez e destacar somente onde as instâncias de `Sessoes` são criadas.

```sh
bash 06-sistemas-escalaveis/executar.sh DemoEstadoLocal
bash 06-sistemas-escalaveis/executar.sh DemoEstadoCompartilhado
```

Primeiro: `A: Ana`, `B: SEM SESSÃO`. Depois: `A: Ana`, `B: Ana`. O segundo exemplo injeta o mesmo objeto para modelar armazenamento compartilhado. As réplicas são objetos dentro da mesma JVM, **não processos reais ou Redis**. Em produção, o armazenamento precisa funcionar entre processos e tem latência, falhas, expiração e segurança próprias. A demo isola a causa lógica da perda da sessão.

### 23:30–27:00 · Limitar por chave e janela

```sh
bash 06-sistemas-escalaveis/executar.sh DemoLimite
```

Abrir `LimitePorJanela.permitir`: calcular janela, consultar contagem da chave e incrementar se permitido. As primeiras três de Ana passam; quarta e quinta não. Bia tem cota própria; Ana volta a passar em t=60. O relógio lógico chega como argumento para tornar a experiência reproduzível, sem esperar um minuto real.

O método retorna boolean, não uma resposta HTTP. O adaptador HTTP traduziria a negativa para a resposta apropriada. Execução sequencial, sem concorrência; mapa em memória não é limitador distribuído de produção. Se houver duas instâncias deste limitador, haverá duas cotas independentes.

## 27:00–30:00 · Slide 09 — Escolher pela necessidade

Recuperação: “Cache resolve API sem sessão?” Não. “CDN resolve toda escrita lenta?” Não. “Balancear elimina gargalo do banco?” Não. Pedir ao aluno para ligar técnica → recurso protegido → custo novo. Encerrar com uma sequência de decisão: medir → identificar → mudar uma variável → observar efeito e custo.

Exercício: criar dois limitadores de três e alternar seis chamadas. Prever antes o total aceito e explicar por que isso não representa uma cota global.

## Fontes

- [HTTP caching — MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching): mecanismos e restrições de cache HTTP.
- [CloudFront — How delivery works](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/HowCloudFrontWorks.html): borda, cache e origem.
- [AWS Application Load Balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html): alvos, roteamento e health checks.
- [RFC 6585 §4](https://www.rfc-editor.org/rfc/rfc6585.html#section-4): HTTP 429.
