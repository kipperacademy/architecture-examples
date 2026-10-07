public class DemoLimite {
    public static void main(String[] args) {
        LimitePorJanela limite = new LimitePorJanela(3);
        for (int pedido = 1; pedido <= 5; pedido++) {
            System.out.println("Ana t=0 pedido " + pedido + ": " + limite.permitir("Ana", 0));
        }
        System.out.println("Bia t=0: " + limite.permitir("Bia", 0));
        System.out.println("Ana t=60: " + limite.permitir("Ana", 60));
    }
}
