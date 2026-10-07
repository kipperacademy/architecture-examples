package br.com.kipperdev.clean.adapters.out;

import br.com.kipperdev.clean.application.PaymentProvider;
import br.com.kipperdev.clean.domain.PaymentStatus;

/** Traduz a conversa interna para o formato externo e normaliza a resposta do provedor. */
public final class AppMaxPaymentAdapter implements PaymentProvider {
    private final AppMaxApiSimulator appMax;

    public AppMaxPaymentAdapter(AppMaxApiSimulator appMax) {
        this.appMax = appMax;
    }

    @Override
    public PaymentResult charge(PaymentCommand command) {
        var external = appMax.createCharge(new AppMaxApiSimulator.Request(
                command.enrollmentId(), command.student(), command.course(), command.amountInCents()));
        return new PaymentResult(toInternalStatus(external.status()), external.paymentId());
    }

    private PaymentStatus toInternalStatus(String providerStatus) {
        return switch (providerStatus.toLowerCase()) {
            case "paid" -> PaymentStatus.CONFIRMED;
            case "pending" -> PaymentStatus.PENDING;
            case "refused" -> PaymentStatus.DECLINED;
            default -> PaymentStatus.UNKNOWN;
        };
    }
}
