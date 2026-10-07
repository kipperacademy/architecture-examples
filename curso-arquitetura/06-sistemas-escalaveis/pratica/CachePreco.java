public class CachePreco {
    private final Catalogo origem;
    private Integer preco;

    public CachePreco(Catalogo origem) { this.origem = origem; }

    public int consultar() {
        if (preco == null) preco = origem.consultarPreco();
        return preco;
    }

    public void invalidar() { preco = null; }
}
