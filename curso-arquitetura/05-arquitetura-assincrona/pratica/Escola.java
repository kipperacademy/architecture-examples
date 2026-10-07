import java.util.ArrayList;
import java.util.List;

public class Escola {
    private Estado estado = new Estado(List.of(), List.of());

    public void matricularSemOutbox(String aluna) {
        estado = new Estado(List.of(aluna), List.of());
    }

    public void matricularComOutbox(String aluna, String eventoId) {
        List<String> matriculas = new ArrayList<>(estado.matriculas());
        List<Evento> eventos = new ArrayList<>(estado.outbox());
        matriculas.add(aluna);
        eventos.add(new Evento(eventoId, aluna));
        estado = new Estado(matriculas, eventos);
    }

    public Estado estado() { return estado; }
}
