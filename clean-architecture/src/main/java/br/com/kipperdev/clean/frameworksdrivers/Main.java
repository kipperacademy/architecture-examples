package br.com.kipperdev.clean.frameworksdrivers;

import br.com.kipperdev.clean.interfaceadapters.controllers.ConsoleEnrollmentController;
import br.com.kipperdev.clean.interfaceadapters.controllers.AppMaxWebhookController;
import br.com.kipperdev.clean.interfaceadapters.gateways.AppMaxApiSimulator;
import br.com.kipperdev.clean.interfaceadapters.gateways.AppMaxConfiguration;
import br.com.kipperdev.clean.interfaceadapters.gateways.AppMaxHttpPaymentAdapter;
import br.com.kipperdev.clean.interfaceadapters.gateways.AppMaxPaymentAdapter;
import br.com.kipperdev.clean.interfaceadapters.gateways.JpaEnrollmentRepository;
import br.com.kipperdev.clean.usecases.ConfirmEnrollmentPayment;
import br.com.kipperdev.clean.usecases.EnrollStudent;
import java.io.IOException;

/** Composition root: escolhe as implementações concretas e injeta os contratos. */
public final class Main {
    public static void main(String[] args) {
        var jdbcUrl = System.getenv().getOrDefault("DATABASE_URL",
                "jdbc:h2:file:./data/enrollments;DB_CLOSE_ON_EXIT=FALSE");
        if (!jdbcUrl.startsWith("jdbc:h2:file:"))
            throw new IllegalArgumentException("DATABASE_URL must point to a file-backed H2 database");
        var databasePath = jdbcUrl.substring("jdbc:h2:file:".length()).split(";", 2)[0];
        var databaseFile = java.nio.file.Path.of(databasePath);
        if (databaseFile.getParent() != null) {
            try {
                java.nio.file.Files.createDirectories(databaseFile.getParent());
            } catch (java.io.IOException e) {
                throw new IllegalStateException("Could not create database directory", e);
            }
        }
        try (var repository = new JpaEnrollmentRepository(jdbcUrl)) {
            var env = System.getenv();
            var mode = env.getOrDefault("APPMAX_MODE", "simulation");
            if ("http".equalsIgnoreCase(mode)) {
                var config = AppMaxConfiguration.from(env);
                var customer = config.customerProfile(env);
                var payment = new AppMaxHttpPaymentAdapter(config);
                var useCase = new EnrollStudent(payment, repository, repository);
                var confirmation = new ConfirmEnrollmentPayment(payment, repository);
                var webhookPort = Integer.parseInt(env.getOrDefault("APPMAX_WEBHOOK_PORT", "8080"));
                try (var webhook = new AppMaxWebhookController(webhookPort, repository, confirmation)) {
                    webhook.start();
                    var console = new ConsoleEnrollmentController(useCase);
                    var enrollmentId = env.getOrDefault("APPMAX_ENROLLMENT_ID", "enr-" + java.util.UUID.randomUUID());
                    var student = env.getOrDefault("APPMAX_ENROLLMENT_STUDENT", customer.firstName() + " " + customer.lastName());
                    var course = env.getOrDefault("APPMAX_ENROLLMENT_COURSE", "Arquitetura");
                    var amount = Integer.parseInt(env.getOrDefault("APPMAX_ENROLLMENT_AMOUNT_CENTS", "10000"));
                    console.enroll(enrollmentId, student, course, amount, customer);
                    System.out.println("Webhook AppMax aguardando em :" + webhookPort + "/webhooks/appmax");
                    new java.util.concurrent.CountDownLatch(1).await();
                } catch (IOException e) {
                    throw new IllegalStateException("Could not start AppMax webhook receiver", e);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            } else if ("simulation".equalsIgnoreCase(mode)) {
                var simulatedAppMax = new AppMaxApiSimulator(java.util.Map.of(
                        "enr-ana", "paid", "enr-bia", "pending", "enr-clara", "refused"));
                var payment = new AppMaxPaymentAdapter(simulatedAppMax);
                var useCase = new EnrollStudent(payment, repository, repository);
                var console = new ConsoleEnrollmentController(useCase);
                console.enroll("enr-ana", "Ana", "Arquitetura", 10_000);
                console.enroll("enr-bia", "Bia", "Arquitetura", 10_000);
                console.enroll("enr-clara", "Clara", "Arquitetura", 10_000);
            } else {
                throw new IllegalArgumentException("APPMAX_MODE must be simulation or http");
            }
            System.out.println("Matrículas no H2/JPA (" + jdbcUrl + "): " +
                    repository.findAll().stream().map(e -> e.student()).toList());
        }
    }
}
