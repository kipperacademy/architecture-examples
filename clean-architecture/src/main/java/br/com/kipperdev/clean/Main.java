package br.com.kipperdev.clean;

import br.com.kipperdev.clean.adapters.in.ConsoleEnrollmentAdapter;
import br.com.kipperdev.clean.adapters.out.AppMaxApiSimulator;
import br.com.kipperdev.clean.adapters.out.AppMaxPaymentAdapter;
import br.com.kipperdev.clean.adapters.out.InMemoryEnrollmentRepository;
import br.com.kipperdev.clean.application.EnrollStudent;

/** Composition root: escolhe as implementações concretas e injeta os contratos. */
public final class Main {
    public static void main(String[] args) {
        var repository = new InMemoryEnrollmentRepository();
        var simulatedAppMax = new AppMaxApiSimulator(java.util.Map.of(
                "enr-ana", "paid", "enr-bia", "pending", "enr-clara", "refused"));
        var payment = new AppMaxPaymentAdapter(simulatedAppMax);
        var useCase = new EnrollStudent(payment, repository);
        var console = new ConsoleEnrollmentAdapter(useCase);

        console.enroll("enr-ana", "Ana", "Arquitetura", 10_000);
        console.enroll("enr-bia", "Bia", "Arquitetura", 10_000);
        console.enroll("enr-clara", "Clara", "Arquitetura", 10_000);
        System.out.println("Matrículas persistidas: " + repository.findAll().stream().map(e -> e.student()).toList());
    }
}
