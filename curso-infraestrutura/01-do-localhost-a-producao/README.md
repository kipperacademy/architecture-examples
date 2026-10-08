# API de cursos em Node.js — localhost à produção

API pequena para a aula **Do localhost à produção**. Usa apenas o módulo HTTP nativo do Node.js, sem framework, banco de dados ou dependências externas.

- Rota: `GET /cursos`
- Porta padrão: `8080`
- Resposta: lista JSON com cursos fictícios
- Outros caminhos retornam `404`; métodos diferentes de `GET` retornam `405`

## Rodar com Node.js

Requer Node.js 22 ou superior.

```sh
npm start
```

Em outro terminal:

```sh
curl -i http://localhost:8080/cursos
```

## Rodar com Docker localmente

Construa a imagem e inicie o container com a porta `8080` publicada no computador:

```sh
docker build -t catalogo-cursos-node .
docker run --rm -p 8080:8080 catalogo-cursos-node
```

Ou use a configuração Compose local:

```sh
docker compose -f docker-compose.local.yml up --build -d
curl -i http://localhost:8080/cursos
docker compose -f docker-compose.local.yml down
```

O mapeamento `8080:8080` encaminha a porta 8080 da máquina para a porta 8080 do container. A aplicação escuta em `0.0.0.0` dentro do container para aceitar conexões encaminhadas pelo Docker.

## Publicar na VPS Hostinger

O Dockerfile mantém a aplicação independente do domínio e escuta na porta `8080`. O `docker-compose.yml` conecta o container à rede externa `traefik-proxy` e configura o Traefik do Docker Manager para encaminhar `api.srv1460423.hstgr.cloud` para essa porta, com HTTPS.

O DNS `A` e `AAAA` de `api.srv1460423.hstgr.cloud` deve apontar para esta VPS. Na verificação atual, ambos resolvem para os endereços da VPS. Mantenha as portas `80` e `443` acessíveis no firewall. Com o projeto implantado no Docker Manager:

```sh
docker compose up --build -d
curl https://api.srv1460423.hstgr.cloud/cursos
```

O Traefik já precisa estar em execução, e o projeto deve compartilhar a rede `traefik-proxy`.

`PORT` e `HOST` podem ser substituídos por variáveis de ambiente. Os padrões são `8080` e `0.0.0.0`.
