package demos;

import adapters.entrada.EntradaCsv;
import adapters.saida.RepositorioEmMemoria;
import aplicacao.Matricular;
import aplicacao.MatricularAluno;
import aplicacao.RepositorioMatriculas;
import java.io.IOException;
import java.nio.file.Path;

public class DemoHexagonalCsv {
    public static void main(String[] args) throws IOException {
        RepositorioMatriculas repositorio = new RepositorioEmMemoria();
        Matricular matricular = new MatricularAluno(repositorio);
        EntradaTerminal csv = new EntradaTerminal(matricular);

        csv.importar(Path.of("dados", "pedidos.csv"));
        System.out.println("Matrículas salvas: " + repositorio.listar());
    }
}
