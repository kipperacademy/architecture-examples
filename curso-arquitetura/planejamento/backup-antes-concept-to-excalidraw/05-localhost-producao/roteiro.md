# Aula 05 — Do localhost à produção

**Título Pora:** Do localhost à produção: servidores, máquinas virtuais, containers e deploy.
**Prazo editorial:** 22/10/2026. **Duração proposta:** 25 min: 10 de teoria, 12 de prática, 3 de fechamento.

## Objetivo e contexto

O aluno deve acompanhar o caminho navegador → endereço/porta → processo, distinguir máquina, VM, imagem e container, e explicar o que um deploy precisa além de executar o código. A escola disponibiliza a página de um curso. Cada acesso retorna o nome da instância e um contador local de visitas. Não há login, banco ou transação financeira nesta demo.

Pergunta condutora: **o que muda quando o código precisa continuar respondendo fora do meu terminal?**

## 00:00–10:00 · Teoria

1. **Slide 01, 00:00–01:00 — Capa.** Código, processo, ambiente e implantação. Começar pela definição: disponibilizar e operar uma versão da aplicação num ambiente onde os usuários conseguem acessá-la.
2. **Slide 02, 01:00–02:30 — Localhost.** É a própria máquina ou contexto de rede de quem faz a chamada. `localhost` no computador de uma aluna não aponta para o computador da professora. Uma porta identifica o destino do serviço naquele endereço. O processo precisa estar rodando e escutando no endereço correto.
3. **Slide 03, 02:30–04:00 — Servidor e VM.** Servidor pode designar a máquina ou o processo que atende. VM possui sistema operacional convidado sobre virtualização; a aplicação roda sobre seu runtime. Explicar responsabilidade operacional: atualizar ambiente, iniciar processo, observar falhas. Não comparar custo ou desempenho com números inventados.
4. **Slide 04, 04:00–05:30 — Container.** Processo isolado com filesystem/configuração próprios, compartilhando o kernel do host Linux. Imagem é o pacote usado para iniciar; container é a execução. No macOS, Docker Desktop usa ambiente Linux virtualizado: não dizer que o container Linux compartilha diretamente o kernel Darwin. VM e container podem ser combinados.
5. **Slide 05, 05:30–07:00 — Caminho da porta.** Dentro do container, a aplicação escuta em `0.0.0.0:8080`. A publicação `127.0.0.1:8081:8080` liga a porta local 8081 à interna 8080. `EXPOSE` documenta; não publica sozinho. Mostrar duas portas com cores equivalentes aos terminais.
6. **Slide 06, 07:00–08:30 — Configuração.** O mesmo código pode receber `PORT` e `INSTANCE` diferentes. Configuração altera o ambiente da execução; não exige editar a regra. Segredos reais exigem um mecanismo adequado, não devem ser incluídos na imagem. A demo usa apenas valores fictícios.
7. **Slide 07, 08:30–10:00 — Estado e reinício.** O contador vive na memória do processo. Parar e iniciar cria outro contador. Empacotar numa imagem não torna dados duráveis. Um volume também não vira um banco automaticamente. Perguntar: **o contador continua em 3 depois do restart?**

## 10:00–22:00 · Prática

### 10:00–13:30 · Um servidor de verdade

Abrir `pratica/Servidor.java`: criação do servidor, handler `/curso`, contador e resposta. Usar `HttpServer` do JDK para o aluno enxergar HTTP sem configuração de framework. Os dois handlers são pequenos; detalhes de bytes são tradução para o protocolo.

Na **pasta do curso**, terminal A:

```sh
INSTANCE=A PORT=8080 bash 05-localhost-producao/executar.sh
```

Terminal B:

```sh
curl http://127.0.0.1:8080/curso
curl http://127.0.0.1:8080/curso
curl http://127.0.0.1:8080/health
```

Saídas esperadas: `instancia=A | visitas=1`, depois `visitas=2`; health retorna `ok`. `HOST` padrão é `127.0.0.1`, restrito à máquina local.

### 13:30–16:00 · Momento WOW: outra execução, outro estado

Parar apenas o processo da demo com Ctrl+C e iniciá-lo novamente. O próximo `/curso` volta a `visitas=1`. Pedir a previsão antes de reiniciar. O retorno a 1 vem da nova instância de `AtomicInteger`, não de cache do navegador.

Abrir outro terminal com `INSTANCE=B PORT=8081 bash 05-localhost-producao/executar.sh`. Consultar 8080 e 8081. O mesmo código atende com nomes e contadores independentes. Não chamar isso de balanceamento: o cliente escolheu a porta manualmente. Parar B antes do bloco Docker, que usa 8081.

### 16:00–20:30 · Empacotar e mapear a porta

Abrir `Dockerfile`: primeiro estágio compila; segundo recebe classes e runtime. `USER` evita executar a aplicação como root. `HOST=0.0.0.0` permite alcançar a interface de rede do container; o publish permanece local ao computador.

```sh
docker build -t curso-arquitetura:aula05 05-localhost-producao
docker run --rm --name curso-arquitetura-aula05 \
  -p 127.0.0.1:8081:8080 -e INSTANCE=container curso-arquitetura:aula05
curl http://127.0.0.1:8081/curso
```

Os dois primeiros comandos ocupam seus respectivos terminais; fazer o curl em outro. Parar com Ctrl+C no terminal do container. O `--rm` remove somente esse container efêmero ao terminar.

**Estado de preparação:** Dockerfile e comandos preparados; o daemon Docker estava desligado em 06/10, portanto build/run em container ainda precisam de ensaio. A primeira construção também depende de baixar a imagem oficial. O bloco HTTP local é independente do Docker. Não fingir a saída do container na gravação.

### 20:30–22:00 · Slide 08 — O que falta para produção

Mostrar o caminho DNS → HTTPS/proxy → aplicação saudável. Esclarecer que esta sessão não publicou um serviço na internet. Para uma implantação real: selecionar ambiente, entregar artefato, configurar rede/TLS e segredos, iniciar processo, observar logs/health, testar a versão e ter estratégia de retorno. `/health` aqui só prova que o handler responde; não verifica dependências.

## 22:00–25:00 · Slide 09 — Recapitulação

“Por que a aluna não abre meu localhost?” O endereço resolve no ambiente dela. “Por que EXPOSE não basta?” Falta publicação/roteamento. “Por que perdi visitas?” O estado era do processo. Exercício: mudar somente `INSTANCE` e `PORT`, observar a resposta e explicar por que o código não mudou.

Evitar abrir contas de cloud ou executar deploy real durante esta aula curta. O foco é o modelo operacional e um pacote reproduzível, preparando a próxima aula sobre réplicas. Apresentar explicitamente a diferença entre demonstração local e operação pública.

## Fontes

- [Docker — Containers](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/).
- [Docker — Publishing ports](https://docs.docker.com/get-started/docker-concepts/running-containers/publishing-ports/).
- [JDK HttpServer](https://docs.oracle.com/en/java/javase/21/docs/api/jdk.httpserver/com/sun/net/httpserver/HttpServer.html).
