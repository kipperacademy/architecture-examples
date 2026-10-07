package br.com.kipperdev.hexagonal.adapters.out;

import br.com.kipperdev.hexagonal.application.ports.out.EnrollmentRepository;
import br.com.kipperdev.hexagonal.domain.Enrollment;
import java.util.ArrayList;
import java.util.List;

public final class InMemoryEnrollmentRepository implements EnrollmentRepository {
    private final List<Enrollment> enrollments = new ArrayList<>();

    @Override public void save(Enrollment enrollment) { enrollments.add(enrollment); }
    @Override public List<Enrollment> findAll() { return List.copyOf(enrollments); }
}
