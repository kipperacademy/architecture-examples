import com.sun.net.httpserver.HttpServer;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.atomic.AtomicInteger;

public class Servidor {
    public static void main(String[] args) throws Exception {
        String host = System.getenv().getOrDefault("HOST", "127.0.0.1");
        int porta = Integer.parseInt(System.getenv().getOrDefault("PORT", "8080"));
        String instancia = System.getenv().getOrDefault("INSTANCE", "local");
        AtomicInteger visitas = new AtomicInteger();
        HttpServer servidor = HttpServer.create(new InetSocketAddress(host, porta), 0);

        servidor.createContext("/curso", request -> {
            String texto = "Curso Arquitetura | instancia=" + instancia
                + " | visitas=" + visitas.incrementAndGet() + "\n";
            byte[] corpo = texto.getBytes(StandardCharsets.UTF_8);
            request.getResponseHeaders().set("Content-Type", "text/plain; charset=utf-8");
            request.sendResponseHeaders(200, corpo.length);
            request.getResponseBody().write(corpo);
            request.close();
        });
        servidor.createContext("/health", request -> {
            byte[] corpo = "ok\n".getBytes(StandardCharsets.UTF_8);
            request.sendResponseHeaders(200, corpo.length);
            request.getResponseBody().write(corpo);
            request.close();
        });
        Runtime.getRuntime().addShutdownHook(new Thread(() -> servidor.stop(0)));
        servidor.start();
        System.out.println("HTTP em " + host + ":" + servidor.getAddress().getPort());
    }
}
