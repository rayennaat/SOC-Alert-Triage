package com.secuiq.backend.dto.alerts.upload;

import com.secuiq.backend.domain.AlertSeverity;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
@SuppressWarnings("java:S107")
@Schema(description = "Request to upload a single alert (JSON/CSV body)")
public class AlertUploadRequest {
    @NotBlank
    @Schema(example = "Suricata", requiredMode = Schema.RequiredMode.REQUIRED)
    private String source;

    @NotBlank
    @Schema(example = "2025-12-05T14:30:00Z", requiredMode = Schema.RequiredMode.REQUIRED)
    private String timestamp;

    @NotNull
    @Schema(example = "HIGH", requiredMode = Schema.RequiredMode.REQUIRED)
    private AlertSeverity severity;

    @NotBlank
    @Schema(example = "Multiple failed SSH logins", requiredMode = Schema.RequiredMode.REQUIRED)
    private String description;

    @NotBlank
    @Schema(example = "192.168.1.100", requiredMode = Schema.RequiredMode.REQUIRED)
    private String srcIp;

    @NotBlank
    @Schema(example = "10.0.0.50", requiredMode = Schema.RequiredMode.REQUIRED)
    private String dstIp;

    @Schema(example = "admin", nullable = true)
    private String username;

    @NotBlank
    @Schema(example = "bruteforce", requiredMode = Schema.RequiredMode.REQUIRED)
    private String eventType;

    @Schema(description = "Any extra raw data (JSON object)", nullable = true)
    private Object rawData;
}
