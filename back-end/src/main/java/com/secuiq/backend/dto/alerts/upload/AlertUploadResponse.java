package com.secuiq.backend.dto.alerts.upload;

import java.util.List;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Schema(description = "Response after uploading one or many alerts")
public class AlertUploadResponse {
    @Schema(example = "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8")
    private String alertId;

    @Schema(example = "SUCCESS")
    private String status;

    @Schema(nullable = true)
    private List<String> errors;
}
