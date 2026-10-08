# Exemplos: do localhost à produção

Este diretório contém duas implementações da mesma API didática: Java e Node.js. Ambas expõem somente `GET /cursos`, retornam cursos fictícios e usam a porta `8080`.

## Java

Requer JDK 21 e Maven.

```sh
mvn -q package
java -jar target/catalogo-cursos-1.0.0.jar
```

Em outro terminal:

```sh
curl -i http://localhost:8080/cursos
```

## Node.js e Docker

Consulte [`nodejs/README.md`](nodejs/README.md) para rodar a API com Node.js ou Docker Compose.

## Configurações de deploy

- `deploy/catalogo-cursos.service`: execução do exemplo Java pelo `systemd`.
- `deploy/nginx-catalogo-cursos.conf`: proxy reverso do Nginx para a API Java.
