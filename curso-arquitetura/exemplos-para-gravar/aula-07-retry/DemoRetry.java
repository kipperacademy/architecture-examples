import java.util.concurrent.TimeoutException;

public class DemoRetry {
    public static void main(String[] args) throws Exception {
        Provedor provedor = new Provedor();
        try {
            provedor.cobrar("pedido-ana", true);
        } catch (TimeoutException erro) {
            System.out.println("Cliente: UNKNOWN. Timeout não prova falha da cobrança.");
        }
        provedor.cobrar("pedido-ana", false);
        System.out.println("Cobranças no provedor: " + provedor.quantidade());
    }
}
