package br.com.kipperdev.hexagonal.application.ports.secondary;

import br.com.kipperdev.hexagonal.domain.Enrollment;
import br.com.kipperdev.hexagonal.domain.PendingPixPayment;
import java.util.List;

public interface EnrollmentRepository {
    void save(Enrollment enrollment);
    List<Enrollment> findAll();
    void savePendingPix(PendingPixPayment payment);
    java.util.Optional<PendingPixPayment> findPendingPix(String enrollmentId);
    void updatePendingPixStatus(String enrollmentId, String providerStatus);
    void confirmPixEnrollment(String enrollmentId, String providerStatus);
}
