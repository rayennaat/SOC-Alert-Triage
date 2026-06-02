package com.secuiq.backend.repositories;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.secuiq.backend.domain.AlertFeatures;

public interface AlertFeaturesRepository extends JpaRepository<AlertFeatures, Long> {
    boolean existsByAlertId(String alertId);

    Optional<AlertFeatures> findByAlertId(String alertId);
}
