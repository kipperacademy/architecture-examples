# API de cursos com Node.js e Docker

Uma API pequena para acompanhar a aula **Do localhost à produção**. Ela usa apenas o módulo HTTP nativo do Node.js: sem framework, banco de dados ou dependências externas.

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

## Rodar com Docker

Na pasta `nodejs/`, construa a imagem e inicie o container:

```sh
docker build -t catalogo-cursos-node .
docker run --rm -p 8080:8080 catalogo-cursos-node
```

Ou use Docker Compose:

```sh
docker compose up --build -d
curl -i http://localhost:8080/cursos
docker compose down
```

O mapeamento `8080:8080` encaminha a porta 8080 da máquina para a porta 8080 do container. A aplicação escuta em `0.0.0.0` dentro do container para aceitar conexões encaminhadas pelo Docker.

## Publicar na VPS

Envie esta pasta para a VPS e execute `docker compose up --build -d`, ou conecte o repositório a um painel como Coolify. No Coolify, configure a porta interna `8080` e associe o domínio; o proxy do painel encaminha as requisições para o container. Para acessar diretamente pelo IP da VPS na porta `8080`, mapeie essa porta no Compose e permita `8080/tcp` nos firewalls da Hostinger e do Ubuntu.

`PORT` e `HOST` podem ser substituídos por variáveis de ambiente. Os padrões são `8080` e `0.0.0.0`.
