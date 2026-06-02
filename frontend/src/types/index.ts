// src/types/index.ts

// Alert Types - Only Real Backend Data
export interface Alert {
  id: number;
  alertId?: string;
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
}

// Stats Types - Simplified
export interface SummaryStats {
  totalAlerts: number;
  critical: number;
  high: number;
  medium: number;
  low: number;
  topThreatIp: string;
  topThreatType: string;
}

// Chart Data Types
export interface ChartDataItem {
  name: string;
  value: number;
  color: string;
}

export interface AlertTypeData {
  name: string;
  count: number;
}

export interface ChartData {
  priorityDistribution: ChartDataItem[];
  alertTypes: AlertTypeData[];
}

// Props Types
export interface UploadAreaProps {
  onUpload?: (file: File) => void | Promise<void>;
}

export interface StatsCardsProps {
  stats: SummaryStats;
}

export interface AlertTableProps {
  alerts: Alert[];
}

export interface PriorityBadgeProps {
  priority: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
}

export interface AlertPieChartProps {
  data: ChartDataItem[];
}

export interface AlertBarChartProps {
  data: AlertTypeData[];
}