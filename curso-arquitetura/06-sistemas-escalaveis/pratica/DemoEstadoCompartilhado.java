public class DemoEstadoCompartilhado {
    public static void main(String[] args) {
        Sessoes armazenamentoCompartilhado = new Sessoes();
        Replica replicaA = new Replica("A", armazenamentoCompartilhado);
        Replica replicaB = new Replica("B", armazenamentoCompartilhado);
        replicaA.login("sessao-ana", "Ana");
        System.out.println(replicaA.acessar("sessao-ana"));
        System.out.println(replicaB.acessar("sessao-ana"));
    }
}
