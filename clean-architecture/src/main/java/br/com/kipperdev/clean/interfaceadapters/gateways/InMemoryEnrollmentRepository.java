package br.com.kipperdev.clean.interfaceadapters.gateways;

import br.com.kipperdev.clean.usecases.EnrollmentRepository;
import br.com.kipperdev.clean.entities.Enrollment;
import java.util.ArrayList;
import java.util.List;

public final class InMemoryEnrollmentRepository implements EnrollmentRepository {
    private final List<Enrollment> enrollments = new ArrayList<>();

    @Override public void save(Enrollment enrollment) { enrollments.add(enrollment); }
    @Override public List<Enrollment> findAll() { return List.copyOf(enrollments); }
}
