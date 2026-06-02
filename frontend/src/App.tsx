// src/App.tsx
import { useState, useEffect } from 'react';
import Header from './components/Header';
import UploadArea from './components/UploadArea';
import StatsCards from './components/StatsCards';
import AlertPieChart from './components/charts/AlertPieChart';
import AlertBarChart from './components/charts/AlertBarChart';
import AlertTable from './components/AlertTable';
import type { Alert, SummaryStats, ChartData } from './types';
import {
  checkSystemHealth,
  processBatchAlertsPython,
  convertBatchAlertsToTableFormat,
  calculateSummaryStats,
  generateChartData,
} from './services/api';

function App() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [stats, setStats] = useState<SummaryStats | null>(null);
  const [charts, setCharts] = useState<ChartData | null>(null);
  const [isDataLoaded, setIsDataLoaded] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [systemHealth, setSystemHealth] = useState({
    javaBackend: false,
    mlService: false,
    overall: false,
  });
  const [error, setError] = useState<string | null>(null);

  // Check system health on mount
  useEffect(() => {
    checkHealth();
  }, []);

  const checkHealth = async () => {
    try {
      const health = await checkSystemHealth();
      setSystemHealth(health);
      
      if (!health.overall) {
        console.warn('System health check: Some services are down');
      }
    } catch (err) {
      console.error('Health check failed:', err);
    }
  };

  const handleUpload = async (file: File) => {
    setIsUploading(true);
    setError(null);

    try {
      console.log('Processing file:', file.name);

      // Call the FastAPI ML service for batch processing.
      const result = await processBatchAlertsPython(file);

      console.log('Batch processing result:', result);

      // Convert batch alerts to table format
      const convertedAlerts = convertBatchAlertsToTableFormat(result.all_alerts);

      // Calculate statistics
      const newStats = calculateSummaryStats(result.all_alerts);

      // Generate chart data
      const newChartData = generateChartData(result.all_alerts);

      // Update state
      setAlerts(convertedAlerts);
      setStats(newStats);
      setCharts(newChartData);
      setIsDataLoaded(true);

      // Show success message
      console.log(`✅ Successfully processed ${result.total_alerts} alerts`);
    } catch (err) {
      console.error('Upload error:', err);
      setError(
        err instanceof Error
          ? err.message
          : 'Failed to process file. Please check if the backend services are running.'
      );

      // Show error alert
      alert(
        'Failed to process file. Please ensure:\n' +
          '1. Java Backend is running on port 8081\n' +
          '2. Python ML Service is running on port 8000\n' +
          '3. CSV file format is correct'
      );
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#080a0c] text-zinc-100 p-4 md:p-6 lg:p-8">
      <div className="mx-auto max-w-[1500px]">
        <Header />

        {/* System Health Status */}
        {!systemHealth.overall && (
          <div className="mb-6 p-4 bg-yellow-900/30 border border-yellow-700 rounded-md">
            <div className="flex items-center">
              <svg
                className="w-5 h-5 text-amber-300 mr-3"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                />
              </svg>
              <div>
                <span className="text-amber-300 font-medium">System Status Warning</span>
                <p className="text-sm text-zinc-300 mt-1">
                  {!systemHealth.javaBackend && '• Java Backend (port 8081) is offline '}
                  {!systemHealth.mlService && '• ML Service (port 8000) is offline'}
                </p>
              </div>
              <button
                onClick={checkHealth}
                className="ml-auto px-4 py-2 bg-yellow-800 hover:bg-yellow-700 text-white rounded-md text-sm transition-colors"
              >
                Retry
              </button>
            </div>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-900/30 border border-red-700 rounded-md">
            <div className="flex items-center">
              <svg
                className="w-5 h-5 text-red-400 mr-3"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
              <div className="flex-1">
                <span className="text-red-400 font-medium">Error</span>
                <p className="text-sm text-zinc-300 mt-1">{error}</p>
              </div>
              <button
                onClick={() => setError(null)}
                className="ml-4 text-zinc-400 hover:text-white"
              >
                ×
              </button>
            </div>
          </div>
        )}

        {/* Upload Area */}
        <div className="mb-8">
          <UploadArea onUpload={handleUpload} />
          {isUploading && (
            <div className="mt-4 p-4 bg-teal-950/30 border border-teal-800 rounded-md">
              <div className="flex items-center">
                <svg
                  className="animate-spin h-5 w-5 text-teal-300 mr-3"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
                <span className="text-teal-300 font-medium">
                  Processing alerts with ML model... This may take a moment.
                </span>
              </div>
            </div>
          )}
        </div>

        {/* Dashboard Content */}
        {isDataLoaded && stats && charts ? (
          <>
            <StatsCards stats={stats} />

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
              <AlertPieChart data={charts.priorityDistribution} />
              <AlertBarChart data={charts.alertTypes} />
            </div>

            <AlertTable alerts={alerts} />
          </>
        ) : (
          <div className="text-center py-12 border border-zinc-800 bg-zinc-950/80 shadow-[0_18px_50px_rgba(0,0,0,0.25)]">
            <svg
              className="w-16 h-16 text-zinc-600 mx-auto mb-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="1.5"
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            <div className="text-zinc-400 text-lg mb-2">No Data Available</div>
            <div className="text-zinc-500 text-sm mb-4">
              Upload a CSV file to see AI-powered alert prioritization
            </div>
            <div className="text-zinc-600 text-xs max-w-md mx-auto">
              Your CSV should contain network traffic features that the ML model will analyze
              to classify attack types and assign priority levels.
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="mt-8 border-t border-zinc-800 pt-5 text-center font-mono text-xs uppercase tracking-normal text-zinc-600">
          SecuIQ SOC Triage / ML-assisted alert prioritization
        </div>
      </div>
    </div>
  );
}

export default App;