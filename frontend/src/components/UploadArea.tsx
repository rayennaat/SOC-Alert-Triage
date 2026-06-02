import React, { useState, type DragEvent, type ChangeEvent } from 'react';
import type { UploadAreaProps } from '../types';

const REQUIRED_COLUMNS = [
  'alert_id',
  'source_ip',
  'dest_ip',
  'timestamp',
  'Flow Duration',
  'Total Fwd Packets',
  'Total Backward Packets',
  'Flow Bytes/s',
  'Flow Packets/s',
  'Total Length of Fwd Packets',
  'Total Length of Bwd Packets',
  'Fwd Packet Length Mean',
  'Bwd Packet Length Mean',
  'Packet Length Std',
  'Flow IAT Mean',
  'Fwd IAT Mean',
  'Bwd IAT Mean',
  'PSH Flag Count',
  'SYN Flag Count',
  'FIN Flag Count',
  'Destination Port',
  'Down/Up Ratio',
];

type CsvPreview = {
  rowCount: number;
  columns: string[];
  missingColumns: string[];
  status: 'valid' | 'invalid';
};

const UploadArea: React.FC<UploadAreaProps> = ({ onUpload }) => {
  const [isDragging, setIsDragging] = useState<boolean>(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [csvPreview, setCsvPreview] = useState<CsvPreview | null>(null);
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [isLoadingDemo, setIsLoadingDemo] = useState<boolean>(false);

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      void handleFile(files[0]);
    }
  };

  const handleFileInput = (e: ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      void handleFile(files[0]);
    }
  };

  const inspectCsv = async (file: File): Promise<CsvPreview> => {
    const text = await file.text();
    const lines = text.replace(/\r/g, '').split('\n').filter((line) => line.trim().length > 0);
    const columns = lines[0]
      ? lines[0].split(',').map((column) => column.trim().replace(/^"|"$/g, ''))
      : [];
    const missingColumns = REQUIRED_COLUMNS.filter((column) => !columns.includes(column));

    return {
      rowCount: Math.max(lines.length - 1, 0),
      columns,
      missingColumns,
      status: missingColumns.length === 0 && lines.length > 1 ? 'valid' : 'invalid',
    };
  };

  const handleFile = async (file: File) => {
    if (file.type !== 'text/csv' && !file.name.endsWith('.csv')) {
      alert('Please upload a CSV file');
      return;
    }

    try {
      const preview = await inspectCsv(file);
      setSelectedFile(file);
      setCsvPreview(preview);
    } catch (error) {
      console.error('CSV preview failed:', error);
      setSelectedFile(file);
      setCsvPreview({ rowCount: 0, columns: [], missingColumns: REQUIRED_COLUMNS, status: 'invalid' });
    }
  };

  const clearSelection = () => {
    setSelectedFile(null);
    setCsvPreview(null);
  };

  const analyzeSelectedFile = async () => {
    if (!selectedFile) {
      alert('Please select a CSV file first');
      return;
    }

    if (csvPreview?.status === 'invalid') {
      alert('This CSV is missing required columns. Please choose a valid alert dataset.');
      return;
    }

    if (onUpload) {
      setIsUploading(true);
      try {
        await onUpload(selectedFile);
      } finally {
        setIsUploading(false);
      }
    }
  };

  const useDemoDataset = async () => {
    setIsLoadingDemo(true);
    try {
      const response = await fetch('/sample-alerts.csv');
      if (!response.ok) {
        throw new Error('Demo dataset could not be loaded');
      }
      const blob = await response.blob();
      const file = new File([blob], 'sample-alerts.csv', { type: 'text/csv' });
      await handleFile(file);
    } catch (error) {
      console.error('Demo dataset load failed:', error);
      alert('Demo dataset could not be loaded. Make sure the frontend dev server was restarted after adding public/sample-alerts.csv.');
    } finally {
      setIsLoadingDemo(false);
    }
  };

  return (
    <div className="border border-dashed border-zinc-700 bg-zinc-950/90 p-8 text-center transition-all duration-300 hover:border-teal-500">
      <div className="flex flex-col items-center justify-center space-y-4">
        <div className="w-16 h-16 bg-teal-950/30 rounded-sm flex items-center justify-center">
          <svg className="w-8 h-8 text-teal-300" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
          </svg>
        </div>

        <div className="text-center">
          <h3 className="text-lg font-semibold text-white mb-2">Upload Alert Data</h3>
          <p className="text-zinc-400 text-sm mb-4">
            Drag & drop your CSV file with security alerts, or click to browse
          </p>
        </div>

        <div
          className={`w-full max-w-2xl border-2 ${isDragging ? 'border-teal-500 bg-teal-950/30' : 'border-zinc-700'} rounded-md p-6 transition-all duration-300 ${!selectedFile ? 'cursor-pointer' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => !selectedFile && document.getElementById('fileInput')?.click()}
        >
          {selectedFile ? (
            <div className="space-y-4 text-left">
              <div className="flex items-center justify-between bg-zinc-900 p-3 rounded">
                <div className="flex min-w-0 items-center">
                  <svg className="w-5 h-5 text-emerald-300 mr-2 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <span className="truncate text-white font-medium">{selectedFile.name}</span>
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    clearSelection();
                  }}
                  className="text-zinc-400 hover:text-white"
                >
                  x
                </button>
              </div>

              {csvPreview && (
                <div className="grid gap-3 rounded-md border border-zinc-800 bg-black/30 p-4 text-sm md:grid-cols-3">
                  <div>
                    <div className="text-xs uppercase tracking-normal text-zinc-500">Rows</div>
                    <div className="mt-1 font-semibold text-white">{csvPreview.rowCount.toLocaleString()}</div>
                  </div>
                  <div>
                    <div className="text-xs uppercase tracking-normal text-zinc-500">Columns</div>
                    <div className="mt-1 font-semibold text-white">{csvPreview.columns.length}</div>
                  </div>
                  <div>
                    <div className="text-xs uppercase tracking-normal text-zinc-500">Status</div>
                    <div className={`mt-1 font-semibold ${csvPreview.status === 'valid' ? 'text-emerald-300' : 'text-red-400'}`}>
                      {csvPreview.status === 'valid' ? 'Ready to analyze' : 'Invalid file'}
                    </div>
                  </div>
                  {csvPreview.missingColumns.length > 0 && (
                    <div className="md:col-span-3">
                      <div className="text-xs uppercase tracking-normal text-red-300">Missing required columns</div>
                      <div className="mt-2 flex flex-wrap gap-2">
                        {csvPreview.missingColumns.map((column) => (
                          <span key={column} className="rounded-sm bg-red-950/70 px-2 py-1 text-xs text-red-200">
                            {column}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                  {csvPreview.status === 'valid' && (
                    <div className="md:col-span-3 text-xs text-zinc-500">
                      Detected alert metadata and all model feature columns.
                    </div>
                  )}
                </div>
              )}
            </div>
          ) : (
            <div className="text-center py-4">
              <svg className="w-12 h-12 text-zinc-500 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
              <p className="text-zinc-400">CSV files only</p>
              <p className="text-sm text-zinc-500 mt-1">Max file size: 10MB</p>
            </div>
          )}

          <input
            id="fileInput"
            type="file"
            accept=".csv"
            className="hidden"
            onChange={handleFileInput}
          />
        </div>

        <div className="flex flex-wrap justify-center gap-3">
          <button
            onClick={() => document.getElementById('fileInput')?.click()}
            className="px-6 py-2.5 bg-zinc-900 hover:bg-zinc-800 text-white rounded-md font-medium transition-colors"
          >
            Browse Files
          </button>

          <button
            onClick={useDemoDataset}
            disabled={isLoadingDemo || isUploading}
            className="px-6 py-2.5 bg-stone-700 hover:bg-stone-600 disabled:bg-stone-900/60 disabled:cursor-not-allowed text-white rounded-md font-medium transition-colors"
          >
            {isLoadingDemo ? 'Loading Demo...' : 'Use Demo Dataset'}
          </button>

          <button
            onClick={analyzeSelectedFile}
            disabled={isUploading || !selectedFile || csvPreview?.status === 'invalid'}
            className={`px-6 py-2.5 rounded-md font-medium transition-colors ${isUploading || !selectedFile || csvPreview?.status === 'invalid' ? 'bg-zinc-800 cursor-not-allowed' : 'bg-teal-700 hover:bg-teal-600'} text-white flex items-center`}
          >
            {isUploading ? (
              <>
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Processing...
              </>
            ) : (
              'Upload & Analyze'
            )}
          </button>
        </div>

        <div className="text-xs text-zinc-500">
          <p>Required: alert_id, source_ip, dest_ip, timestamp, and the 18 network-flow feature columns</p>
        </div>
      </div>
    </div>
  );
};

export default UploadArea;
