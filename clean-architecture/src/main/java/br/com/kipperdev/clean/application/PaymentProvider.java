package br.com.kipperdev.clean.application;

import br.com.kipperdev.clean.domain.PaymentStatus;

/** Port defined in the application's language; adapters translate provider protocols to it. */
public interface PaymentProvider {
    PaymentResult charge(PaymentCommand command);

    record PaymentCommand(String enrollmentId, String student, String course, int amountInCents) {}
    record PaymentResult(PaymentStatus status, String reference) {}
}
