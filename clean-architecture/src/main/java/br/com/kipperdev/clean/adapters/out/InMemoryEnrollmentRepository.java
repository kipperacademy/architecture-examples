package br.com.kipperdev.clean.adapters.out;

import br.com.kipperdev.clean.application.EnrollmentRepository;
import br.com.kipperdev.clean.domain.Enrollment;
import java.util.ArrayList;
import java.util.List;

public final class InMemoryEnrollmentRepository implements EnrollmentRepository {
    private final List<Enrollment> enrollments = new ArrayList<>();

    @Override public void save(Enrollment enrollment) { enrollments.add(enrollment); }
    @Override public List<Enrollment> findAll() { return List.copyOf(enrollments); }
}
