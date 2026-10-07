package br.com.kipperdev.clean.application;

import br.com.kipperdev.clean.domain.Enrollment;
import java.util.List;

public interface EnrollmentRepository {
    void save(Enrollment enrollment);
    List<Enrollment> findAll();
}
