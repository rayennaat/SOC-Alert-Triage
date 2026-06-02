package com.secuiq.backend.dto.predict;

import com.secuiq.backend.domain.AlertSeverity;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;

@SuppressWarnings("java:S107")
@Schema(description = "Request for ML-based severity prediction")
public class PredictRequest {

    @NotBlank
    @Schema(example = "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8")
    private String alertId;

    @NotBlank
    @Schema(example = "Tunis")
    private String source;

    @NotBlank
    @Schema(example = "HIGH")
    private AlertSeverity severity;

    @NotBlank
    @Schema(example = "2023-10-05T14:48:00Z")
    private String timestamp;

    @NotBlank
    @Schema(example = "185.53.177.10")
    private String srcIp;

    @NotBlank
    @Schema(example = "10.2.10.10")
    private String dstIp;

    @NotBlank
    @Schema(example = "user")
    private String username;

    @NotBlank
    @Schema(example = "bruteforce")
    private String eventType;

    @NotBlank
    @Schema(example = "Multiple failed logins from same IP in 2 minutes")
    private String description;

    public PredictRequest(String alertId, String source, AlertSeverity severity, String timestamp, String srcIp,
            String dstIp,
            String username, String eventType, String description) {
        this.alertId = alertId;
        this.source = source;
        this.severity = severity;
        this.timestamp = timestamp;
        this.srcIp = srcIp;
        this.dstIp = dstIp;
        this.username = username;
        this.eventType = eventType;
        this.description = description;
    }

    public String getAlertId() {
        return alertId;
    }

    public void setAlertId(String alertId) {
        this.alertId = alertId;
    }

    public String getSource() {
        return source;
    }

    public void setSource(String source) {
        this.source = source;
    }

    public AlertSeverity getSeverity() {
        return severity;
    }

    public void setSeverity(AlertSeverity severity) {
        this.severity = severity;
    }

    public String getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }

    public String getSrcIp() {
        return srcIp;
    }

    public void setSrcIp(String srcIp) {
        this.srcIp = srcIp;
    }

    public String getDstIp() {
        return dstIp;
    }

    public void setDstIp(String dstIp) {
        this.dstIp = dstIp;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getEventType() {
        return eventType;
    }

    public void setEventType(String eventType) {
        this.eventType = eventType;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }
}
