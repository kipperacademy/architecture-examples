package adapters.entrada;

import aplicacao.Matricular;
import dominio.StatusPagamento;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

public class EntradaCsv {
    private final Matricular matricular;

    public EntradaCsv(Matricular matricular) {
        this.matricular = matricular;
    }

    public void importar(Path arquivo) throws IOException {
        for (String linha : Files.readAllLines(arquivo, StandardCharsets.UTF_8)) {
            String[] campos = linha.split(";", -1);
            if (campos.length != 2) {
                throw new IllegalArgumentException("Linha inválida: " + linha);
            }
            String aluna = campos[0].trim();
            StatusPagamento pagamento = StatusPagamento.valueOf(campos[1].trim());
            boolean liberada = matricular.executar(aluna, pagamento);
            System.out.println(aluna + " | matrícula liberada: " + liberada);
        }
    }
}
