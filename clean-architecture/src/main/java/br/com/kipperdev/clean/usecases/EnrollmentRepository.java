package br.com.kipperdev.clean.usecases;

import br.com.kipperdev.clean.entities.Enrollment;
import java.util.List;

public interface EnrollmentRepository {
    void save(Enrollment enrollment);
    List<Enrollment> findAll();
}
