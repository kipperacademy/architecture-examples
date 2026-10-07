import java.util.List;

public record Estado(List<String> matriculas, List<Evento> outbox) {
    public Estado {
        matriculas = List.copyOf(matriculas);
        outbox = List.copyOf(outbox);
    }
}
