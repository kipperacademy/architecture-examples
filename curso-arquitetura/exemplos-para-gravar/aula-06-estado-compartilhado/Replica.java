public class Replica {
    private final String nome;
    private final Sessoes sessoes;

    public Replica(String nome, Sessoes sessoes) {
        this.nome = nome;
        this.sessoes = sessoes;
    }

    public void login(String sessao, String aluna) { sessoes.salvar(sessao, aluna); }
    public String acessar(String sessao) { return nome + ": " + sessoes.consultar(sessao); }
}
