package br.com.kipperdev.hexagonal.application.ports.out;

import br.com.kipperdev.hexagonal.domain.Enrollment;
import java.util.List;

public interface EnrollmentRepository {
    void save(Enrollment enrollment);
    List<Enrollment> findAll();
}
