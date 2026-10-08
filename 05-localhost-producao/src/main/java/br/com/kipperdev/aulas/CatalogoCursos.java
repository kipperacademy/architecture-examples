package br.com.kipperdev.aulas;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;

public final class CatalogoCursos {
    private static final String CURSOS_JSON = """
            [
              {"id": 1, "nome": "Java do zero", "nivel": "iniciante"},
              {"id": 2, "nome": "APIs com Java", "nivel": "intermediario"},
              {"id": 3, "nome": "Deploy na VPS", "nivel": "intermediario"}
            ]
            """;

    private CatalogoCursos() {}

    public static void main(String[] args) throws IOException {
        int port = Integer.parseInt(System.getenv().getOrDefault("PORT", "8080"));
        String bindAddress = System.getenv().getOrDefault("APP_BIND_ADDRESS", "127.0.0.1");

        HttpServer server = HttpServer.create(new InetSocketAddress(bindAddress, port), 0);
        server.createContext("/", CatalogoCursos::handle);
        server.start();

        System.out.printf("Catálogo ouvindo em http://%s:%d/cursos%n", bindAddress, port);
    }

    private static void handle(HttpExchange exchange) throws IOException {
        try (exchange) {
            String path = exchange.getRequestURI().getPath();
            String method = exchange.getRequestMethod();

            if (!"/cursos".equals(path)) {
                respond(exchange, 404, "text/plain; charset=utf-8", "Rota não encontrada\n");
                return;
            }

            if (!"GET".equals(method)) {
                exchange.getResponseHeaders().set("Allow", "GET");
                respond(exchange, 405, "text/plain; charset=utf-8", "Método não permitido\n");
                return;
            }

            respond(exchange, 200, "application/json; charset=utf-8", CURSOS_JSON);
        }
    }

    private static void respond(HttpExchange exchange, int status, String contentType, String body) throws IOException {
        byte[] bytes = body.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().set("Content-Type", contentType);
        exchange.getResponseHeaders().set("Cache-Control", "no-store");
        exchange.sendResponseHeaders(status, bytes.length);
        exchange.getResponseBody().write(bytes);
    }
}
