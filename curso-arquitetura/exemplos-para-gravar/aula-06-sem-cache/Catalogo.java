public class Catalogo {
    private int preco = 10000;
    private int consultas;

    public int consultarPreco() {
        consultas++;
        return preco;
    }

    public void alterarPreco(int preco) { this.preco = preco; }
    public int consultas() { return consultas; }
}
