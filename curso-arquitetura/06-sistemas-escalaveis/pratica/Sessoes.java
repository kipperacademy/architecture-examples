import java.util.HashMap;
import java.util.Map;

public class Sessoes {
    private final Map<String, String> alunas = new HashMap<>();
    public void salvar(String sessao, String aluna) { alunas.put(sessao, aluna); }
    public String consultar(String sessao) { return alunas.getOrDefault(sessao, "SEM SESSÃO"); }
}
