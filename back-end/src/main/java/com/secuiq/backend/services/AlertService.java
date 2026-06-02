package com.secuiq.backend.services;

import org.springframework.data.domain.Pageable;
import org.springframework.web.multipart.MultipartFile;

import com.secuiq.backend.dto.alerts.AlertListResponse;
import com.secuiq.backend.dto.alerts.upload.AlertUploadRequest;
import com.secuiq.backend.dto.alerts.upload.AlertUploadResponse;

// What is the purpose of this file ?
public interface AlertService {
    AlertUploadResponse uploadAlert(AlertUploadRequest request);

    AlertUploadResponse uploadFile(MultipartFile file);

    AlertListResponse getAlerts(Pageable pageable, String severity, String source, String eventType);
}
