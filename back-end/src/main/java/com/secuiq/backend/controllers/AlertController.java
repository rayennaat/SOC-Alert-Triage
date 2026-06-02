package com.secuiq.backend.controllers;

import com.secuiq.backend.dto.alerts.AlertListResponse;
import com.secuiq.backend.dto.alerts.upload.AlertUploadRequest;
import com.secuiq.backend.dto.alerts.upload.AlertUploadResponse;
import com.secuiq.backend.services.AlertService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

@RestController
@RequestMapping("/alerts")
@RequiredArgsConstructor // THIS IS ALL YOU NEED — WORKS 100%
@Tag(name = "Alerts", description = "Alert upload and listing endpoints")
public class AlertController {

        private final AlertService alertService;

        @PostMapping(consumes = MediaType.APPLICATION_JSON_VALUE)
        @Operation(summary = "Upload a single alert")
        public ResponseEntity<AlertUploadResponse> uploadSingleAlert(
                        @Valid @RequestBody AlertUploadRequest request) {
                AlertUploadResponse response = alertService.uploadAlert(request);
                return "SUCCESS".equals(response.getStatus())
                                ? ResponseEntity.ok(response)
                                : ResponseEntity.badRequest().body(response);
        }

        @PostMapping(value = "/upload", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
        @Operation(summary = "Upload alerts from file")
        public ResponseEntity<AlertUploadResponse> uploadFile(
                        @Parameter(description = "File to upload") @RequestPart("file") MultipartFile file) {
                if (file == null || file.isEmpty()) {
                        return ResponseEntity.badRequest().body(
                                        new AlertUploadResponse(null, "FAILED", List.of("File is empty")));
                }
                AlertUploadResponse response = alertService.uploadFile(file);
                return "SUCCESS".equals(response.getStatus())
                                ? ResponseEntity.ok(response)
                                : ResponseEntity.badRequest().body(response);
        }

        @GetMapping
        public ResponseEntity<AlertListResponse> getAlerts(
                        @RequestParam(defaultValue = "0") int page,
                        @RequestParam(defaultValue = "20") int size,
                        @RequestParam(required = false) String severity,
                        @RequestParam(required = false) String source,
                        @RequestParam(required = false) String eventType) {
                Pageable pageable = PageRequest.of(page, size);
                AlertListResponse response = alertService.getAlerts(pageable, severity, source, eventType);
                return ResponseEntity.ok(response);
        }
}