package br.com.kipperdev.hexagonal;

import br.com.kipperdev.hexagonal.adapters.in.ConsoleEnrollmentAdapter;
import br.com.kipperdev.hexagonal.adapters.out.AppMaxApiSimulator;
import br.com.kipperdev.hexagonal.adapters.out.AppMaxPaymentAdapter;
import br.com.kipperdev.hexagonal.adapters.out.InMemoryEnrollmentRepository;
import br.com.kipperdev.hexagonal.application.service.EnrollStudentService;

/** Composition root: conecta os adaptadores às portas do núcleo. */
public final class Main {
    public static void main(String[] args) {
        var repository = new InMemoryEnrollmentRepository();
        var appMaxSimulator = new AppMaxApiSimulator(java.util.Map.of(
                "enr-ana", "paid", "enr-bia", "pending", "enr-clara", "refused"));
        var paymentAdapter = new AppMaxPaymentAdapter(appMaxSimulator);
        var enrollStudent = new EnrollStudentService(paymentAdapter, repository);
        var consoleAdapter = new ConsoleEnrollmentAdapter(enrollStudent);

        consoleAdapter.enroll("enr-ana", "Ana", "Arquitetura", 10_000);
        consoleAdapter.enroll("enr-bia", "Bia", "Arquitetura", 10_000);
        consoleAdapter.enroll("enr-clara", "Clara", "Arquitetura", 10_000);
        System.out.println("Matrículas persistidas: " + repository.findAll().stream().map(e -> e.student()).toList());
    }
}
