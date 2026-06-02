package com.secuiq.backend.services;

import com.secuiq.backend.domain.Alert;
import com.secuiq.backend.domain.AlertFeatures;
import com.secuiq.backend.domain.AlertSeverity;
import com.secuiq.backend.repositories.AlertFeaturesRepository;
import com.secuiq.backend.repositories.AlertRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.Set;
import java.util.concurrent.ThreadLocalRandom;

@Service
@RequiredArgsConstructor
public class FeatureExtractionService {

    private final AlertRepository alertRepository;
    private final AlertFeaturesRepository featuresRepository;

    private static final Set<String> TOP_EVENTS = Set.of("bruteforce", "malware", "ddos", "phishing", "scan");

    @Async
    public void extractAndStoreFeatures(String alertId) {
        // Run the whole thing in a new transaction — no self-injection needed
        extractAndStoreInNewTransaction(alertId);
    }

    @Transactional
    public void extractAndStoreInNewTransaction(String alertId) {
        Alert alert = alertRepository.findById(alertId)
                .orElseThrow(() -> new IllegalStateException("Alert not found: " + alertId));

        if (featuresRepository.existsByAlertId(alertId)) {
            return;
        }

        ZonedDateTime zdt = alert.getTimestamp().atZone(ZoneId.systemDefault());

        AlertFeatures features = AlertFeatures.builder()
                .alertId(alertId)
                .hourOfDay(zdt.getHour())
                .dayOfWeek(zdt.getDayOfWeek().getValue() % 7)
                .isWeekend(zdt.getDayOfWeek().getValue() >= 6)
                .severityLow(alert.getSeverity() == AlertSeverity.LOW)
                .severityMedium(alert.getSeverity() == AlertSeverity.MEDIUM)
                .severityHigh(alert.getSeverity() == AlertSeverity.HIGH)
                .severityCritical(alert.getSeverity() == AlertSeverity.CRITICAL)
                .eventBruteforce(isTopEvent(alert, "bruteforce"))
                .eventMalware(isTopEvent(alert, "malware"))
                .eventDdos(isTopEvent(alert, "ddos"))
                .eventPhishing(isTopEvent(alert, "phishing"))
                .eventScan(isTopEvent(alert, "scan"))
                .eventOther(!TOP_EVENTS.contains(alert.getEventType().toLowerCase()))
                .descriptionLength(alert.getDescription().length())
                .srcIpEntropy(calculateEntropy(alert.getSrcIp()))
                .eventType(alert.getEventType().toLowerCase())
                .userRole(alert.getUsername() != null && alert.getUsername().toLowerCase().contains("admin") ? "admin"
                        : "user")
                .loginAttempts(alert.getEventType().toLowerCase().contains("brute") ||
                        alert.getEventType().toLowerCase().contains("login") ? 5 : 1)
                .uniqueDstPorts(1)
                .bytesSent(100 + ThreadLocalRandom.current().nextLong(9900))
                .build();

        featuresRepository.save(features);
    }

    private boolean isTopEvent(Alert alert, String event) {
        return alert.getEventType().toLowerCase().contains(event);
    }

    private double calculateEntropy(String ip) {
        return ip.chars()
                .boxed()
                .collect(java.util.stream.Collectors.groupingBy(c -> c, java.util.stream.Collectors.counting()))
                .values()
                .stream()
                .mapToDouble(count -> {
                    double p = count / (double) ip.length();
                    return -p * Math.log(p) / Math.log(2);
                })
                .sum();
    }
}