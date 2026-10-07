public class DemoEventoPerdido {
    public static void main(String[] args) {
        Escola escola = new Escola();
        Fila fila = new Fila();
        escola.matricularSemOutbox("Ana");
        System.out.println("Falha entre salvar matrícula e publicar: publicação não executada.");
        System.out.println("Matrículas: " + escola.estado().matriculas());
        System.out.println("Eventos na fila: " + fila.tamanho());
    }
}
