import java.util.HashMap;
import java.util.Map;

public class LimitePorJanela {
    private final int limite;
    private long janela = -1;
    private final Map<String, Integer> contagens = new HashMap<>();

    public LimitePorJanela(int limite) { this.limite = limite; }

    public boolean permitir(String cliente, long segundo) {
        long atual = segundo / 60;
        if (atual != janela) {
            contagens.clear();
            janela = atual;
        }
        int usadas = contagens.getOrDefault(cliente, 0);
        if (usadas >= limite) return false;
        contagens.put(cliente, usadas + 1);
        return true;
    }
}
