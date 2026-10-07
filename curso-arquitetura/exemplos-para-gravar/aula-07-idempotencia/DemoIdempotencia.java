import java.util.concurrent.TimeoutException;

public class DemoIdempotencia {
    public static void main(String[] args) throws Exception {
        ProvedorIdempotente provedor = new ProvedorIdempotente();
        try {
            provedor.cobrar("pedido-ana", 10000, true);
        } catch (TimeoutException erro) {
            System.out.println("Cliente: UNKNOWN. Repetir com a MESMA chave.");
        }
        String resultado = provedor.cobrar("pedido-ana", 10000, false);
        System.out.println("Cliente: " + resultado);
        System.out.println("Cobranças no provedor: " + provedor.quantidade());
    }
}
