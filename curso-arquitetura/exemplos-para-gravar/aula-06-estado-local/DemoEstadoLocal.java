public class DemoEstadoLocal {
    public static void main(String[] args) {
        Replica replicaA = new Replica("A", new Sessoes());
        Replica replicaB = new Replica("B", new Sessoes());
        replicaA.login("sessao-ana", "Ana");
        System.out.println(replicaA.acessar("sessao-ana"));
        System.out.println(replicaB.acessar("sessao-ana"));
    }
}
