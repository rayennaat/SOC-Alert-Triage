import type { Alert, SummaryStats, ChartData } from '../types';

export const mockAlerts: Alert[] = [
  {
    id: 1,
    timestamp: "2024-03-15 14:30:22",
    sourceIp: "192.168.1.105",
    destinationIp: "10.0.0.50",
    alertType: "Brute Force",
    description: "Multiple failed login attempts from same IP",
    aiPriority: "CRITICAL",
    confidence: 94,
    count: 23
  },
  {
    id: 2,
    timestamp: "2024-03-15 14:25:10",
    sourceIp: "45.33.32.156",
    destinationIp: "10.0.0.25",
    alertType: "Port Scan",
    description: "TCP SYN scan on multiple ports",
    aiPriority: "HIGH",
    confidence: 88,
    count: 156
  },
  {
    id: 3,
    timestamp: "2024-03-15 14:15:42",
    sourceIp: "172.16.0.12",
    destinationIp: "8.8.8.8",
    alertType: "DNS Anomaly",
    description: "Unusual DNS query patterns",
    aiPriority: "MEDIUM",
    confidence: 76,
    count: 5
  },
  {
    id: 4,
    timestamp: "2024-03-15 14:10:18",
    sourceIp: "10.0.0.100",
    destinationIp: "external-server.com",
    alertType: "Data Exfiltration",
    description: "Large outbound data transfer",
    aiPriority: "CRITICAL",
    confidence: 96,
    count: 1
  },
  {
    id: 5,
    timestamp: "2024-03-15 14:05:33",
    sourceIp: "192.168.1.200",
    destinationIp: "10.0.0.80",
    alertType: "Malware Detection",
    description: "Suspicious process execution",
    aiPriority: "CRITICAL",
    confidence: 98,
    count: 1
  },
  {
    id: 6,
    timestamp: "2024-03-15 13:55:47",
    sourceIp: "203.0.113.5",
    destinationIp: "10.0.0.60",
    alertType: "SQL Injection",
    description: "SQL-like patterns in HTTP requests",
    aiPriority: "HIGH",
    confidence: 85,
    count: 12
  },
  {
    id: 7,
    timestamp: "2024-03-15 13:50:21",
    sourceIp: "192.168.1.150",
    destinationIp: "internal-db.local",
    alertType: "Unauthorized Access",
    description: "Access to restricted database",
    aiPriority: "HIGH",
    confidence: 89,
    count: 3
  },
  {
    id: 8,
    timestamp: "2024-03-15 13:45:09",
    sourceIp: "10.0.0.15",
    destinationIp: "192.168.1.10",
    alertType: "Network Scan",
    description: "ICMP ping sweep across subnet",
    aiPriority: "LOW",
    confidence: 65,
    count: 45
  }
];

export const summaryStats: SummaryStats = {
  totalAlerts: 245,
  critical: 12,
  high: 35,
  medium: 78,
  low: 120,
  topThreatIp: "192.168.1.105",
  topThreatType: "Brute Force"
};

export const chartData: ChartData = {
  priorityDistribution: [
    { name: 'Critical', value: 12, color: '#ef4444' },
    { name: 'High', value: 35, color: '#f97316' },
    { name: 'Medium', value: 78, color: '#eab308' },
    { name: 'Low', value: 120, color: '#3b82f6' }
  ],
  alertTypes: [
    { name: 'Brute Force', count: 45 },
    { name: 'Port Scan', count: 38 },
    { name: 'Malware', count: 12 },
    { name: 'DNS Anomaly', count: 28 },
    { name: 'Data Exfiltration', count: 8 },
    { name: 'SQL Injection', count: 15 }
  ]
};