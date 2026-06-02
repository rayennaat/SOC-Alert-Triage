package com.secuiq.backend.dto.alerts;

import com.secuiq.backend.domain.AlertSeverity;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Schema(description = "Single alert returned in list")
public class AlertResponse {

    @NotBlank
    @Schema(example = "753e1f4b-1a2b-4c3d-8e5f-6a7b8c9d0e1f")
    private String alertId;

    @NotBlank
    @Schema(example = "USA")
    private String source;

    @NotBlank
    @Schema(example = "2024-06-15T14:30:00Z")
    private String timestamp;

    @NotBlank
    @Schema(example = "HIGH")
    private AlertSeverity severity;

    @NotBlank
    @Schema(example = "Suspicious login attempt detected from IP")
    private String description;

    @NotBlank
    @Schema(example = "189.50.1.5")
    private String srcIp;

    @NotBlank
    @Schema(example = "10.80.20.8")
    private String dstIp;

    @NotBlank
    @Schema(example = "john_doe")
    private String username;

    @NotBlank
    @Schema(example = "LOGIN_ATTEMPT")
    private String eventType;

    @NotBlank
    @Schema(example = "0.85")
    private Double score;

    @NotBlank
    @Schema(example = "v1.2.3")
    private String modelVersion;
}