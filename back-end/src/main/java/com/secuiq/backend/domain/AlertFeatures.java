package com.secuiq.backend.domain;

import java.time.Instant;

import org.hibernate.annotations.CreationTimestamp;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name = "alerts_features")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@SuppressWarnings("java:S1659")
public class AlertFeatures {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "alert_id", nullable = false, unique = true)
    private String alertId;

    // Time features
    private int hourOfDay;
    private int dayOfWeek;
    private boolean isWeekend;

    // Original one-hot (keep for future)
    private boolean severityLow, severityMedium, severityHigh, severityCritical;
    private boolean eventBruteforce, eventMalware, eventDdos, eventPhishing, eventScan, eventOther;
    private Double srcIpEntropy;
    private int descriptionLength;

    // NEW: EXACTLY what your Python model needs
    private String eventType;
    @Builder.Default
    private String userRole = "user";
    @Builder.Default
    private int loginAttempts = 1;
    @Builder.Default
    private int uniqueDstPorts = 1;
    @Builder.Default
    private long bytesSent = 500;

    @CreationTimestamp
    private Instant createdAt;
}