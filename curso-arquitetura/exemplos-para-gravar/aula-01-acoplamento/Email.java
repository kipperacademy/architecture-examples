import java.io.IOException;

record Email(boolean disponivel) implements Notificador {
    public void enviar(String aluna) throws IOException {
        if (!disponivel) throw new IOException("E-mail fora do ar");
        System.out.println("  E-mail enviado para " + aluna);
    }
}
