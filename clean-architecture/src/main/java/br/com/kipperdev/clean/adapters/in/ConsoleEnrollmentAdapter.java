package br.com.kipperdev.clean.adapters.in;

import br.com.kipperdev.clean.application.EnrollStudent;

/** Adapta a entrada da demo para os dados pedidos pelo caso de uso. */
public final class ConsoleEnrollmentAdapter {
    private final EnrollStudent enrollStudent;

    public ConsoleEnrollmentAdapter(EnrollStudent enrollStudent) { this.enrollStudent = enrollStudent; }

    public void enroll(String id, String student, String course, int cents) {
        var result = enrollStudent.execute(new EnrollStudent.Request(id, student, course, cents));
        System.out.printf("%s | pagamento=%s | matrícula=%s | referência=%s%n",
                student, result.paymentStatus(), result.enrollment().isPresent() ? "liberada" : "não liberada",
                result.paymentReference());
    }
}
