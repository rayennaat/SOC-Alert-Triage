package com.secuiq.backend.services.impl;

import com.secuiq.backend.domain.AlertFeatures;
import com.secuiq.backend.dto.predict.PredictRequest;
import com.secuiq.backend.dto.predict.PredictResponse;
import com.secuiq.backend.repositories.AlertFeaturesRepository;
import com.secuiq.backend.services.PredictService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.Instant;

@Service
@RequiredArgsConstructor
public class PredictServiceImpl implements PredictService {

    private final AlertFeaturesRepository featuresRepo;

    @Override
    public PredictResponse predict(PredictRequest request) {
        // Find features by alertId from request
        AlertFeatures f = featuresRepo.findByAlertId(request.getAlertId())
                .orElseThrow(() -> new RuntimeException("Features not found for alert: " + request.getAlertId()));

        // Simple but realistic scoring based on your model logic
        double score = 0.1;

        if (f.getEventType() != null) {
            String et = f.getEventType().toLowerCase();
            if (et.contains("malware"))
                score += 0.8;
            else if (et.contains("bruteforce") || et.contains("login"))
                score += 0.6;
            else if (et.contains("scan"))
                score += 0.4;
        }

        if ("admin".equalsIgnoreCase(f.getUserRole()))
            score += 0.3;
        if (f.getLoginAttempts() > 3)
            score += 0.4;
        if (f.getLoginAttempts() > 10)
            score += 0.3;
        if (f.getBytesSent() > 5000)
            score += 0.3;

        score = Math.min(score, 1.0);

        return new PredictResponse(
                request.getAlertId(),
                Math.round(score * 100.0) / 100.0,
                "secuiq-ml-v1.0",
                "Heuristic prediction based on event type, user role, and traffic",
                Instant.now().toString());
    }
}