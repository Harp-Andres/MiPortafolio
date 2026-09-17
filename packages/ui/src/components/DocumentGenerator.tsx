import React, { useState } from "react";
import type { CVData } from "@mportafolio/api-client";
import { DocumentDownloadButton } from "./DocumentDownloadButton";
import { SyncStatus } from "./SyncStatus";

export interface DocumentGeneratorProps {
  /**
   * CV data to generate documents from
   */
  cvData: CVData;

  /**
   * Show sync status panel
   */
  showSyncStatus?: boolean;

  /**
   * Show individual format buttons
   */
  showIndividualButtons?: boolean;

  /**
   * Show "Download All" button
   */
  showDownloadAll?: boolean;

  /**
   * Custom CSS class
   */
  className?: string;

  /**
   * Custom button class
   */
  buttonClassName?: string;

  /**
   * Callback when all downloads complete
   */
  onComplete?: () => void;

  /**
   * Callback on error
   */
  onError?: (error: Error) => void;

  /**
   * Poll interval for sync verification
   */
  syncPollInterval?: number;
}

/**
 * DocumentGenerator
 *
 * Complete component for generating and downloading CV documents
 * Includes sync verification and multiple format options
 *
 * @example
 * ```tsx
 * <DocumentGenerator
 *   cvData={myCV}
 *   showSyncStatus={true}
 *   showIndividualButtons={true}
 * />
 * ```
 */
export const DocumentGenerator: React.FC<DocumentGeneratorProps> = ({
  cvData,
  showSyncStatus = true,
  showIndividualButtons = true,
  showDownloadAll = true,
  className = "",
  buttonClassName = "mb-4",
  onComplete,
  onError,
  syncPollInterval = 0,
}) => {
  const [downloadCount, setDownloadCount] = useState(0);
  const [lastDownload, setLastDownload] = useState<string | null>(null);

  const handleDownloadSuccess = (filename: string) => {
    setDownloadCount((prev) => prev + 1);
    setLastDownload(filename);
    onComplete?.();
  };

  const handleDownloadError = (error: Error) => {
    onError?.(error);
  };

  return (
    <div className={`space-y-6 p-6 bg-gray-50 rounded-lg ${className}`}>
      {/* Header */}
      <div className="border-b pb-4">
        <h2 className="text-2xl font-bold text-gray-800">
          Document Generator
        </h2>
        <p className="text-gray-600 mt-1">
          Generate and download your CV in multiple formats
        </p>
      </div>

      {/* Sync Status Panel */}
      {showSyncStatus && (
        <div className="bg-white p-4 rounded border">
          <h3 className="font-semibold text-gray-800 mb-3">
            Synchronization Status
          </h3>
          <SyncStatus
            cvData={cvData}
            pollInterval={syncPollInterval}
            showDetails={true}
          />
        </div>
      )}

      {/* Download Buttons */}
      {showIndividualButtons && (
        <div className="space-y-3">
          <h3 className="font-semibold text-gray-800">Download Formats</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className={buttonClassName}>
              <DocumentDownloadButton
                format="docx"
                cvData={cvData}
                onSuccess={handleDownloadSuccess}
                onError={handleDownloadError}
                label="📄 Download Word"
              />
            </div>

            <div className={buttonClassName}>
              <DocumentDownloadButton
                format="pdf"
                cvData={cvData}
                onSuccess={handleDownloadSuccess}
                onError={handleDownloadError}
                label="📕 Download PDF"
              />
            </div>

            <div className={buttonClassName}>
              <DocumentDownloadButton
                format="excel"
                cvData={cvData}
                onSuccess={handleDownloadSuccess}
                onError={handleDownloadError}
                label="📊 Download Excel"
              />
            </div>
          </div>
        </div>
      )}

      {/* Download All Button */}
      {showDownloadAll && (
        <div className="bg-blue-50 p-4 rounded border border-blue-200">
          <DocumentDownloadButton
            format="all"
            cvData={cvData}
            onSuccess={handleDownloadSuccess}
            onError={handleDownloadError}
            label="⬇️ Download All Formats"
            className="w-full"
          />
        </div>
      )}

      {/* Stats Footer */}
      <div className="text-center text-sm text-gray-600">
        <p>
          {downloadCount === 0
            ? "No documents downloaded yet"
            : `${downloadCount} document${downloadCount !== 1 ? "s" : ""} downloaded`}
        </p>
        {lastDownload && (
          <p className="text-gray-500 text-xs mt-1">
            Last: {lastDownload}
          </p>
        )}
      </div>
    </div>
  );
};
