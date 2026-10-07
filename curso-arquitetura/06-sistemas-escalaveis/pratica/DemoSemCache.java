public class DemoSemCache {
    public static void main(String[] args) {
        Catalogo catalogo = new Catalogo();
        for (int pedido = 1; pedido <= 5; pedido++) {
            System.out.println("Preço: " + catalogo.consultarPreco());
        }
        System.out.println("Consultas à origem: " + catalogo.consultas());
    }
}
