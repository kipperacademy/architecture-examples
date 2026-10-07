public class DemoOutbox {
    public static void main(String[] args) {
        Escola escola = new Escola();
        Fila fila = new Fila();
        escola.matricularComOutbox("Ana", "evento-1");
        System.out.println("Publicador parado; pendências: " + escola.estado().outbox().size());
        for (Evento evento : escola.estado().outbox()) fila.publicar(evento);
        System.out.println("Matrículas: " + escola.estado().matriculas());
        System.out.println("Após retomar publicador, eventos na fila: " + fila.tamanho());
    }
}
