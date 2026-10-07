import java.util.LinkedHashMap;
import java.util.Map;
import java.util.concurrent.TimeoutException;

public class ProvedorIdempotente {
    private final Map<String, Integer> cobrancas = new LinkedHashMap<>();

    public String cobrar(String chave, int centavos, boolean perderResposta) throws TimeoutException {
        Integer anterior = cobrancas.get(chave);
        if (anterior != null && anterior != centavos) {
            throw new IllegalArgumentException("Mesma chave com outro valor");
        }
        cobrancas.putIfAbsent(chave, centavos);
        if (perderResposta) throw new TimeoutException("Resposta perdida após cobrar");
        return "CONFIRMADO";
    }

    public int quantidade() { return cobrancas.size(); }
}
