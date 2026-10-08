# Roteiro — Do localhost à produção

**Duração sugerida:** 30 minutos. **Exemplo único:** API Java com uma rota `GET /cursos` em `8080`; a mesma aplicação roda local e numa VPS Hostinger. **Pergunta guia:** o que precisa mudar para uma pessoa fora do meu computador chegar ao mesmo processo?

## 1. Abertura e previsões (2 min)

Mostre `http://localhost:8080/cursos` no próprio computador e pergunte: “Se eu mandar este endereço para vocês, em que máquina ele vai tentar conectar?” Colete previsões antes da definição.

## 2. IP e localhost (5 min)

- IP é um endereço usado para encaminhar pacotes a uma interface de rede. IPv4 e IPv6 são formatos; não é nome de domínio nem porta.
- `localhost` é o nome convencional para o loopback do ambiente que está fazendo a chamada: em geral `127.0.0.1` em IPv4 e `::1` em IPv6. A mesma URL, em dois computadores, chega a computadores diferentes.
- `8080` é a porta do processo que espera a conexão naquela máquina. Um endereço sem uma aplicação escutando não produz a resposta.
- Pergunte: “O que muda se eu trocar `localhost` por `127.0.0.1`? E se eu copiar a URL para outro computador?”

## 3. Domínio e DNS (4 min)

Desenhe `api.exemplo.com → DNS → IP público da VPS`. O domínio é um nome mais fácil de lembrar. O registro DNS aponta o nome para endereço(s); DNS não move o processo e não libera portas. O cliente ainda precisa alcançar um serviço que esteja ouvindo e que os firewalls permitam.

Faça previsão: “Se o domínio já resolve para o IP, por que ainda pode aparecer timeout?” Revele as dependências: rota de rede, firewall, proxy, processo e porta.

## 4. A rota em Java (6 min)

Abra `src/main/java/br/com/kipperdev/aulas/CatalogoCursos.java`. Use o `HttpServer` do JDK, sem framework, para a regra ficar visível. A API só oferece `GET /cursos` e devolve JSON estático com três cursos fictícios. Demais métodos recebem `405`; caminhos diferentes recebem `404`.

```sh
mvn -q package
java -jar target/catalogo-cursos-1.0.0.jar
```

Em outro terminal, mostre o cliente separado do processo servidor:

```sh
curl -i http://localhost:8080/cursos
```

Pergunte o que o navegador/curl local consulta: o loopback da própria máquina, porta `8080`, caminho `/cursos`.

## 5. Do nome público ao processo (5 min)

Percorra a requisição em sequência, usando o mesmo endpoint:

```text
api.exemplo.com → DNS → IP público:443 → firewall → Nginx → 127.0.0.1:8080 → GET /cursos
```

Na VPS, o Nginx termina HTTPS e encaminha ao Java pelo loopback. O app continua ouvindo `8080`, mas a internet recebe `443`. DNS, proxy e aplicação são peças diferentes; nenhuma isolada faz deploy completo.

## 6. Implantação didática na Hostinger (6 min)

1. Gerar o JAR com Maven e enviar via SSH/SCP para a VPS.
2. Na VPS Ubuntu, instalar o runtime Java e Nginx; executar o JAR como usuário de serviço não-root via `systemd`.
3. Confirmar com `curl http://127.0.0.1:8080/cursos` dentro da própria VPS.
4. Criar registro `A` para o subdomínio apontando ao IPv4 público da VPS.
5. Configurar o Nginx para encaminhar a rota a `127.0.0.1:8080` e habilitar HTTPS.
6. Permitir `80/tcp` e `443/tcp` nos firewalls Hostinger e Ubuntu; manter `8080/tcp` privado. Testar `https://api.exemplo.com/cursos` de fora.

Use os arquivos em `deploy/` como ponto de partida. Substitua o domínio fictício antes de instalar o Nginx. `roteiro.md` não afirma que o serviço já foi publicado.

## 7. Checagem final (2 min)

Pergunte à turma:

1. Por que `localhost` de uma aluna não chega à VPS da professora?
2. O que o registro `A` muda, e o que ele não muda?
3. Por que a aplicação fica em `127.0.0.1:8080` enquanto usuários acessam `https://api.exemplo.com/cursos`?

Feche com a cadeia: nome → endereço → porta pública → proxy → processo → rota.

## Notas de precisão

- Um servidor pode significar a máquina ou o programa que atende a requisições; deixar explícito pelo contexto.
- Um IP público pode identificar uma interface da VPS; DNS pode ter registros A (IPv4) e AAAA (IPv6). O domínio não é “o IP com nome” em sentido literal: é um nome resolvido para registros.
- `localhost` é relativo à máquina/contexto de rede de quem faz a chamada, não de quem compartilhou a URL.
- `systemd` mantém o processo; Nginx recebe as conexões públicas e faz o proxy reverso. Um JAR existir no disco não prova que a aplicação está rodando.
- Não expor a porta Java `8080` na internet nesta configuração. Abrir `80/443` e manter SSH acessível para administração.
