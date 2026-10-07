package br.com.kipperdev.clean.application;

import br.com.kipperdev.clean.domain.Enrollment;
import br.com.kipperdev.clean.domain.PaymentStatus;
import java.util.Optional;

/** Orquestra cobrança e matrícula; só a situação CONFIRMED libera acesso. */
public final class EnrollStudent {
    private final PaymentProvider paymentProvider;
    private final EnrollmentRepository enrollmentRepository;

    public EnrollStudent(PaymentProvider paymentProvider, EnrollmentRepository enrollmentRepository) {
        this.paymentProvider = paymentProvider;
        this.enrollmentRepository = enrollmentRepository;
    }

    public Result execute(Request request) {
        var payment = paymentProvider.charge(new PaymentProvider.PaymentCommand(
                request.id(), request.student(), request.course(), request.amountInCents()));
        if (payment.status() != PaymentStatus.CONFIRMED) {
            return new Result(payment.status(), payment.reference(), Optional.empty());
        }

        var enrollment = new Enrollment(request.id(), request.student(), request.course(), request.amountInCents());
        enrollmentRepository.save(enrollment);
        return new Result(payment.status(), payment.reference(), Optional.of(enrollment));
    }

    public record Request(String id, String student, String course, int amountInCents) {}
    public record Result(PaymentStatus paymentStatus, String paymentReference, Optional<Enrollment> enrollment) {}
}
