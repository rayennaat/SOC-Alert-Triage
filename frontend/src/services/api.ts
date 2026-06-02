// src/services/api.ts

// Backend Configuration
const JAVA_BACKEND_URL = import.meta.env.VITE_JAVA_BACKEND_URL || "http://localhost:8080";
const PYTHON_ML_URL = import.meta.env.VITE_PYTHON_ML_URL || "http://localhost:8000";

// ============================================================================
// TYPE DEFINITIONS
// ============================================================================

export interface NetworkAlertRequest {
  alertId: string;
  sourceIp: string;
  destIp: string;
  timestamp: string;
  assetCriticality: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  flowDuration: number;
  totalFwdPackets: number;
  totalBackwardPackets: number;
  flowBytesPerS: number;
  flowPacketsPerS: number;
  totalLengthOfFwdPackets: number;
  totalLengthOfBwdPackets: number;
  fwdPacketLengthMean: number;
  bwdPacketLengthMean: number;
  packetLengthStd: number;
  flowIATMean: number;
  fwdIATMean: number;
  bwdIATMean: number;
  pshFlagCount: number;
  synFlagCount: number;
  finFlagCount: number;
  destinationPort: number;
  downUpRatio: number;
}

export interface ClassificationResult {
  primaryAttackType: string;
  confidence: number;
  alternativeClassifications?: Array<{
    attackType: string;
    probability: number;
  }>;
}

export interface PrioritizationResult {
  priorityLevel: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  priorityScore: number;
  confidence: number;
}

export interface ClassifyResponse {
  classification: ClassificationResult;
  prioritization: PrioritizationResult;
  recommendations: string[];
}

export interface BatchAlert {
  rank: number;
  alert_id: string;
  source_ip: string;
  dest_ip: string;
  attack_type: string;
  timestamp: string;
  attack_confidence: number;
  priority_level: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  priority_score: number;
  priority_confidence?: number;
}

export interface BatchProcessResponse {
  total_alerts: number;
  prioritization_summary: {
    CRITICAL?: number;
    HIGH?: number;
    MEDIUM?: number;
    LOW?: number;
  };
  all_alerts: BatchAlert[];
}

export interface HealthCheckResponse {
  status: string;
  service: string;
  timestamp?: string;
  model_loaded?: boolean;
  model_accuracy?: number;
}

// ============================================================================
// API FUNCTIONS
// ============================================================================

/**
 * Check health status of Java Backend
 */
export async function checkJavaBackendHealth(): Promise<HealthCheckResponse> {
  try {
    const response = await fetch(`${JAVA_BACKEND_URL}/actuator/health`, {
      method: 'GET',
    });

    if (!response.ok) {
      throw new Error(`Health check failed: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Java Backend health check error:', error);
    throw error;
  }
}

/**
 * Check health status of Python ML Service
 */
export async function checkMLServiceHealth(): Promise<HealthCheckResponse> {
  try {
    const response = await fetch(`${PYTHON_ML_URL}/health`, {
      method: 'GET',
    });

    if (!response.ok) {
      throw new Error(`Health check failed: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('ML Service health check error:', error);
    throw error;
  }
}

/**
 * Classify a single network alert
 */
export async function classifySingleAlert(
  alertData: NetworkAlertRequest
): Promise<ClassifyResponse> {
  try {
    const response = await fetch(`${JAVA_BACKEND_URL}/network-alerts/classify`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(alertData),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Classification failed: ${response.status} - ${errorText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Single alert classification error:', error);
    throw error;
  }
}

/**
 * Process batch of alerts from CSV file via Java Backend
 */
export async function processBatchAlertsJava(file: File): Promise<BatchProcessResponse> {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${JAVA_BACKEND_URL}/network-alerts/batch`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Batch processing failed: ${response.status} - ${errorText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Batch processing error (Java):', error);
    throw error;
  }
}

/**
 * Process batch of alerts from CSV file via Python ML Service
 */
export async function processBatchAlertsPython(file: File): Promise<BatchProcessResponse> {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${PYTHON_ML_URL}/prioritize/csv`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Batch processing failed: ${response.status} - ${errorText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Batch processing error (Python):', error);
    throw error;
  }
}

/**
 * Check overall system health
 */
export async function checkSystemHealth(): Promise<{
  javaBackend: boolean;
  mlService: boolean;
  overall: boolean;
}> {
  const results = {
    javaBackend: false,
    mlService: false,
    overall: false,
  };

  try {
    await checkJavaBackendHealth();
    results.javaBackend = true;
  } catch (error) {
    console.error('Java backend is down:', error);
  }

  try {
    await checkMLServiceHealth();
    results.mlService = true;
  } catch (error) {
    console.error('ML service is down:', error);
  }

  results.overall = results.javaBackend && results.mlService;

  return results;
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Convert backend batch alerts to frontend display format
 * Only uses real data from the ML model - no fake/mock data
 */
export function convertBatchAlertsToTableFormat(
  batchAlerts: BatchAlert[]
): Array<{
  id: number;
  timestamp: string;
  sourceIp: string;
  destinationIp: string;
  alertType: string;
  description: string;
  aiPriority: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  confidence: number;
  priorityScore?: number;
  priorityConfidence?: number;
  count: number;
}> {
  return batchAlerts.map((alert, index) => ({
    id: alert.rank || (index + 1), // Use rank from backend if available
    alertId: alert.alert_id,
    timestamp: alert.timestamp || new Date().toISOString().replace('T', ' ').split('.')[0],
    sourceIp: alert.source_ip,
    destinationIp: alert.dest_ip,
    alertType: alert.attack_type,
    description: `${alert.attack_type} attack detected from ${alert.source_ip}`,
    aiPriority: alert.priority_level,
    confidence: Math.round(alert.attack_confidence * 100),
    priorityScore: alert.priority_score,
    priorityConfidence: alert.priority_confidence !== undefined
      ? Math.round(alert.priority_confidence * 100)
      : undefined,
    count: 1,
  }));
}

/**
 * Calculate summary statistics from batch alerts
 * Only real data from ML model
 */
export function calculateSummaryStats(batchAlerts: BatchAlert[]): {
  totalAlerts: number;
  critical: number;
  high: number;
  medium: number;
  low: number;
  topThreatIp: string;
  topThreatType: string;
} {
  const priorityCounts = {
    CRITICAL: 0,
    HIGH: 0,
    MEDIUM: 0,
    LOW: 0,
  };

  const ipFrequency: Record<string, number> = {};
  const typeFrequency: Record<string, number> = {};

  batchAlerts.forEach((alert) => {
    priorityCounts[alert.priority_level]++;

    ipFrequency[alert.source_ip] = (ipFrequency[alert.source_ip] || 0) + 1;
    typeFrequency[alert.attack_type] = (typeFrequency[alert.attack_type] || 0) + 1;
  });

  const topThreatIp = Object.entries(ipFrequency).sort((a, b) => b[1] - a[1])[0]?.[0] || 'N/A';
  const topThreatType = Object.entries(typeFrequency).sort((a, b) => b[1] - a[1])[0]?.[0] || 'N/A';

  return {
    totalAlerts: batchAlerts.length,
    critical: priorityCounts.CRITICAL,
    high: priorityCounts.HIGH,
    medium: priorityCounts.MEDIUM,
    low: priorityCounts.LOW,
    topThreatIp,
    topThreatType,
  };
}

/**
 * Generate chart data from batch alerts
 */
export function generateChartData(batchAlerts: BatchAlert[]): {
  priorityDistribution: Array<{ name: string; value: number; color: string }>;
  alertTypes: Array<{ name: string; count: number }>;
} {
  const priorityCounts = {
    CRITICAL: 0,
    HIGH: 0,
    MEDIUM: 0,
    LOW: 0,
  };

  const typeFrequency: Record<string, number> = {};

  batchAlerts.forEach((alert) => {
    priorityCounts[alert.priority_level]++;
    typeFrequency[alert.attack_type] = (typeFrequency[alert.attack_type] || 0) + 1;
  });

  const priorityDistribution = [
    { name: 'Critical', value: priorityCounts.CRITICAL, color: '#ef4444' },
    { name: 'High', value: priorityCounts.HIGH, color: '#f97316' },
    { name: 'Medium', value: priorityCounts.MEDIUM, color: '#eab308' },
    { name: 'Low', value: priorityCounts.LOW, color: '#3b82f6' },
  ];

  const alertTypes = Object.entries(typeFrequency)
    .map(([name, count]) => ({ name, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 6); // Top 6 alert types

  return {
    priorityDistribution,
    alertTypes,
  };
}

export default {
  checkJavaBackendHealth,
  checkMLServiceHealth,
  classifySingleAlert,
  processBatchAlertsJava,
  processBatchAlertsPython,
  checkSystemHealth,
  convertBatchAlertsToTableFormat,
  calculateSummaryStats,
  generateChartData,
};