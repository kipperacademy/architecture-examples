import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeoutException;

public class Provedor {
    private final List<String> cobrancas = new ArrayList<>();

    public void cobrar(String pedido, boolean perderResposta) throws TimeoutException {
        cobrancas.add(pedido);
        if (perderResposta) throw new TimeoutException("Resposta perdida após cobrar");
    }

    public int quantidade() { return cobrancas.size(); }
}
