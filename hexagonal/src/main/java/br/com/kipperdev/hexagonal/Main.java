package br.com.kipperdev.hexagonal;

import br.com.kipperdev.hexagonal.adapters.primary.ConsoleEnrollmentAdapter;
import br.com.kipperdev.hexagonal.adapters.primary.EnrollmentHttpAdapter;
import br.com.kipperdev.hexagonal.adapters.secondary.AppMaxApiSimulator;
import br.com.kipperdev.hexagonal.adapters.secondary.AppMaxPaymentAdapter;
import br.com.kipperdev.hexagonal.adapters.secondary.AppMaxPixPaymentAdapter;
import br.com.kipperdev.hexagonal.adapters.secondary.JpaEnrollmentRepository;
import br.com.kipperdev.hexagonal.application.usecases.CheckPixEnrollmentService;
import br.com.kipperdev.hexagonal.application.usecases.CreatePixEnrollmentService;
import br.com.kipperdev.hexagonal.application.usecases.EnrollStudentService;
import br.com.kipperdev.hexagonal.application.usecases.ManageEnrollmentsService;

import java.util.Scanner;
import java.util.concurrent.CountDownLatch;

/** Composition root and small CLI adapter. Simulated payment remains the default mode. */
public final class Main {
    private Main() {}

    public static void main(String[] args) throws Exception {
        var databaseUrl = System.getenv().getOrDefault("ENROLLMENT_DB_URL",
                "jdbc:h2:file:./data/enrollments;DB_CLOSE_ON_EXIT=FALSE");
        try (var repository = new JpaEnrollmentRepository(databaseUrl)) {
            var mode = args.length == 0 ? "api" : args[0];
            switch (mode) {
                case "api" -> runApi(repository);
                case "demo" -> runDemo(repository);
                case "pix-create" -> createPix(repository);
                case "pix-check" -> {
                    if (args.length != 2) usage();
                    var provider = AppMaxPixPaymentAdapter.fromEnvironment();
                    var service = new CheckPixEnrollmentService(provider, repository);
                    var result = service.check(args[1]);
                    System.out.printf("AppMax order status=%s | total_paid=%s | payment=%s | enrollment=%s%n", result.providerStatus(),
                            result.totalPaidInCents() == null ? "missing" : result.totalPaidInCents(), result.paymentStatus(),
                            result.enrollment().isPresent() ? "confirmed" : "pending/not confirmed");
                }
                default -> usage();
            }
        }
    }

    private static void runApi(JpaEnrollmentRepository repository) throws Exception {
        var simulator = new AppMaxApiSimulator(java.util.Map.of(
                "enr-bia", "pending", "enr-clara", "refused"));
        var payment = new AppMaxPaymentAdapter(simulator);
        var enroll = new EnrollStudentService(payment, repository);
        var manage = new ManageEnrollmentsService(repository);
        var port = Integer.parseInt(System.getenv().getOrDefault("API_PORT", "8080"));
        try (var api = new EnrollmentHttpAdapter(port, enroll, manage)) {
            api.start();
            System.out.println("Enrollment API listening at http://127.0.0.1:" + api.port() + "/api/enrollments");
            new CountDownLatch(1).await();
        }
    }

    private static void runDemo(JpaEnrollmentRepository repository) {
        var appMaxSimulator = new AppMaxApiSimulator(java.util.Map.of(
                "enr-ana", "paid", "enr-bia", "pending", "enr-clara", "refused"));
        var paymentAdapter = new AppMaxPaymentAdapter(appMaxSimulator);
        var useCase = new EnrollStudentService(paymentAdapter, repository);
        var console = new ConsoleEnrollmentAdapter(useCase);
        console.enroll("enr-ana", "Ana", "Arquitetura", 10_000);
        console.enroll("enr-bia", "Bia", "Arquitetura", 10_000);
        console.enroll("enr-clara", "Clara", "Arquitetura", 10_000);
        System.out.println("Matrículas no H2: " + repository.findAll().stream().map(e -> e.student()).toList());
    }

    private static void createPix(JpaEnrollmentRepository repository) {
        var input = new Scanner(System.in);
        System.out.println("Criação de Pix AppMax. Dados de contato/IP devem vir do checkout e ser tratados conforme sua política de privacidade.");
        var enrollmentId = ask(input, "ID interno da matrícula");
        var firstName = ask(input, "Nome");
        var lastName = ask(input, "Sobrenome");
        var email = ask(input, "Email");
        var phone = ask(input, "Telefone");
        var ip = ask(input, "IP coletado pelo checkout/Appmax JS");
        var documentNumber = ask(input, "CPF/CNPJ do pagador");
        var student = ask(input, "Nome do estudante");
        var course = ask(input, "Curso");
        int cents;
        try { cents = Integer.parseInt(ask(input, "Valor em centavos")); }
        catch (NumberFormatException e) { throw new IllegalArgumentException("Amount must be an integer number of cents"); }

        var provider = AppMaxPixPaymentAdapter.fromEnvironment();
        var service = new CreatePixEnrollmentService(provider, repository);
        var pending = service.create(new br.com.kipperdev.hexagonal.application.ports.primary.CreatePixEnrollment.Command(
                enrollmentId, firstName, lastName, email, phone, ip, documentNumber, student, course, cents));
        System.out.printf("Pix criado e salvo como pendente. matrícula=%s | AppMax order=%s | status=%s | expira=%s%n",
                pending.enrollmentId(), pending.appMaxOrderId(), pending.providerStatus(), pending.expiresAt());
        System.out.println("EMV para pagamento: " + pending.emvCode());
        System.out.println("QR code retornado: " + pending.qrCode());
        System.out.println("Após pagar, verifique com: ./executar.sh pix-check " + pending.enrollmentId());
        System.out.println("Matrícula não será liberada enquanto a consulta autenticada não retornar aprovado/integrado.");
    }

    private static String ask(Scanner input, String prompt) {
        System.out.print(prompt + ": ");
        var value = input.nextLine().trim();
        if (value.isEmpty()) throw new IllegalArgumentException(prompt + " is required");
        return value;
    }

    private static void usage() {
        System.out.println("Usage: ./executar.sh [api | demo | pix-create | pix-check <enrollment-id>]");
        System.out.println("Real Pix mode requires APP_MAX_CLIENT_ID and APP_MAX_CLIENT_SECRET; sandbox API is the default.");
        System.exit(2);
    }
}
