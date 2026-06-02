
package com.secuiq.backend.repositories;

import org.springframework.stereotype.Repository;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.domain.Page;

import com.secuiq.backend.domain.Alert;
import com.secuiq.backend.domain.AlertSeverity;

// What is the purpose of this file ?
@Repository
public interface AlertRepository extends JpaRepository<Alert, String> {

    Page<Alert> findBySeverity(AlertSeverity severity, Pageable pageable);

    Page<Alert> findBySource(String source, Pageable pageable);

    Page<Alert> findByEventType(String eventType, Pageable pageable);
}
