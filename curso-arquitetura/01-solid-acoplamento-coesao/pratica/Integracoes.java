import java.io.IOException;

final class PagamentoLocal implements Pagamento {
    public int cobrar(int valor) {
        System.out.println("cobrando no novo");
        return valor + 1;
    }
}

record Email(boolean disponivel) implements Notificador {
    public void enviar(String aluna) throws IOException {
        if (!disponivel) throw new IOException("E-mail fora do ar");
        System.out.println("  E-mail enviado para " + aluna);
    }
}

final class WhatsApp implements Notificador {
    public void enviar(String aluna) {
        System.out.println("  WhatsApp enviado para " + aluna);
    }
}
