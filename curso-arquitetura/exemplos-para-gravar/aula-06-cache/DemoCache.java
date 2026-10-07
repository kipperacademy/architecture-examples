public class DemoCache {
    public static void main(String[] args) {
        Catalogo catalogo = new Catalogo();
        CachePreco cache = new CachePreco(catalogo);
        for (int pedido = 1; pedido <= 5; pedido++) {
            System.out.println("Preço: " + cache.consultar());
        }
        System.out.println("Consultas à origem: " + catalogo.consultas());
        catalogo.alterarPreco(12000);
        System.out.println("Preço no cache após alteração: " + cache.consultar());
        cache.invalidar();
        System.out.println("Preço após invalidar: " + cache.consultar());
        System.out.println("Consultas à origem: " + catalogo.consultas());
    }
}
