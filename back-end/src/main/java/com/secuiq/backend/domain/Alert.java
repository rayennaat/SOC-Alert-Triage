package com.secuiq.backend.domain;

import java.time.Instant;

import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.UuidGenerator;
import org.hibernate.type.SqlTypes;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "alerts", indexes = {
        @Index(name = "idx_alert_severity", columnList = "severity"),
        @Index(name = "idx_alert_timestamp", columnList = "timestamp"),
        @Index(name = "idx_alert_source", columnList = "source")
})
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Alert {

    @Id
    @UuidGenerator
    @Column(columnDefinition = "varchar(36)", updatable = false, nullable = false)
    private String alertId;

    @Column(nullable = false)
    private String source;

    @Column(nullable = false)
    private Instant timestamp;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private AlertSeverity severity;

    @Column(nullable = false, length = 2000)
    private String description;

    @Column(nullable = false)
    private String srcIp;

    @Column(nullable = false)
    private String destIp;

    private String username;

    @Column(nullable = false)
    private String eventType;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "jsonb")
    @Builder.Default
    private String rawData = "{}";

    private Double score;

    private String modelVersion;

    @CreationTimestamp
    @Column(updatable = false)
    private Instant createdAt;
}
