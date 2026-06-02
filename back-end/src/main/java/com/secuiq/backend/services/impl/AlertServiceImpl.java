package com.secuiq.backend.services.impl;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.secuiq.backend.domain.Alert;
import com.secuiq.backend.domain.AlertSeverity;
import com.secuiq.backend.dto.alerts.AlertListResponse;
import com.secuiq.backend.dto.alerts.AlertResponse;
import com.secuiq.backend.dto.alerts.upload.AlertUploadRequest;
import com.secuiq.backend.dto.alerts.upload.AlertUploadResponse;
import com.secuiq.backend.repositories.AlertRepository;
import com.secuiq.backend.services.AlertService;
import com.secuiq.backend.services.FeatureExtractionService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional
@SuppressWarnings("java:S1192")
public class AlertServiceImpl implements AlertService {

    private final FeatureExtractionService featureExtractionService;

    private final AlertRepository alertRepository;
    private final ObjectMapper objectMapper;

    @Override
    public AlertUploadResponse uploadAlert(AlertUploadRequest request) {
        List<String> errors = validateRequest(request);
        if (!errors.isEmpty()) {
            return new AlertUploadResponse(null, "FAILED", errors);
        }

        try {
            String rawDataJson = request.getRawData() == null ? "{}"
                    : objectMapper.writeValueAsString(request.getRawData());

            Alert alert = Alert.builder()
                    .source(request.getSource())
                    .timestamp(Instant.parse(request.getTimestamp()))
                    .severity(request.getSeverity())
                    .description(request.getDescription())
                    .srcIp(request.getSrcIp())
                    .destIp(request.getDstIp())
                    .username(request.getUsername())
                    .eventType(request.getEventType())
                    .rawData(rawDataJson)
                    .build();

            Alert saved = alertRepository.save(alert);
            featureExtractionService.extractAndStoreFeatures(saved.getAlertId());
            return new AlertUploadResponse(saved.getAlertId(), "SUCCESS", null);

        } catch (Exception e) {
            return new AlertUploadResponse(null, "FAILED", List.of("Internal error: " + e.getMessage()));
        }
    }

    // BULK upload from file (multipart/form-data)
    @Override
    public AlertUploadResponse uploadFile(MultipartFile file) {
        if (file == null || file.isEmpty()) {
            return new AlertUploadResponse(null, "FAILED", List.of("No file uploaded"));
        }

        // Placeholder – you can implement real CSV/JSON parsing later
        return new AlertUploadResponse(
                null,
                "SUCCESS",
                List.of("File received: " + file.getOriginalFilename() + " (" + file.getSize() + " bytes)"));
    }

    @Override
    @Transactional(readOnly = true)
    public AlertListResponse getAlerts(Pageable pageable, String severity, String source, String eventType) {
        Pageable sorted = PageRequest.of(
                pageable.getPageNumber(),
                pageable.getPageSize(),
                Sort.by("timestamp").descending());

        Page<Alert> page = fetchAlertsPage(sorted, severity, source, eventType);

        List<AlertResponse> items = page.getContent().stream()
                .map(this::toAlertResponse)
                .toList();

        return new AlertListResponse(
                items,
                page.getNumber(),
                page.getSize(),
                page.getTotalElements(),
                page.getTotalPages());
    }

    // ────────────────────── private helpers ──────────────────────

    private Page<Alert> fetchAlertsPage(Pageable pageable, String severity, String source, String eventType) {
        if (isValidSeverity(severity)) {
            return alertRepository.findBySeverity(AlertSeverity.valueOf(severity.toUpperCase()), pageable);
        }
        if (source != null && !source.isBlank()) {
            return alertRepository.findBySource(source, pageable);
        }
        if (eventType != null && !eventType.isBlank()) {
            return alertRepository.findByEventType(eventType, pageable);
        }
        return alertRepository.findAll(pageable);
    }

    private boolean isValidSeverity(String severity) {
        return severity != null && switch (severity.toUpperCase()) {
            case "LOW", "MEDIUM", "HIGH", "CRITICAL" -> true;
            default -> false;
        };
    }

    private AlertResponse toAlertResponse(Alert alert) {
        return new AlertResponse(
                alert.getAlertId(),
                alert.getSource(),
                alert.getTimestamp().toString(),
                alert.getSeverity(),
                alert.getDescription(),
                alert.getSrcIp(),
                alert.getDestIp(),
                alert.getUsername(),
                alert.getEventType(),
                alert.getScore(),
                alert.getModelVersion());
    }

    private List<String> validateRequest(AlertUploadRequest req) {
        List<String> errors = new ArrayList<>();
        if (isBlank(req.getSource()))
            errors.add("source is required");
        if (isBlank(req.getTimestamp())) {
            errors.add("timestamp is required");
        } else {
            try {
                Instant.parse(req.getTimestamp());
            } catch (Exception e) {
                errors.add("timestamp must be valid ISO-8601");
            }
        }
        if (req.getSeverity() == null)
            errors.add("severity is required");
        if (isBlank(req.getDescription()))
            errors.add("description is required");
        if (isBlank(req.getSrcIp()))
            errors.add("srcIp is required");
        if (isBlank(req.getDstIp()))
            errors.add("dstIp is required");
        if (isBlank(req.getEventType()))
            errors.add("eventType is required");
        return errors;
    }

    private static boolean isBlank(String str) {
        return str == null || str.isBlank();
    }
}