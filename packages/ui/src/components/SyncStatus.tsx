import React, { useEffect, useState } from "react";
import type { CVData, SyncVerifyResponse } from "@mportafolio/api-client";
import { getApiClient } from "@mportafolio/api-client";

export interface SyncStatusProps {
  /**
   * CV data to verify
   */
  cvData: CVData;

  /**
   * Poll interval in milliseconds (0 to disable)
   */
  pollInterval?: number;

  /**
   * CSS class name
   */
  className?: string;

  /**
   * Show detailed report
   */
  showDetails?: boolean;

  /**
   * Callback when sync status changes
   */
  onStatusChange?: (status: "success" | "warning" | "error") => void;
}

/**
 * SyncStatus
 *
 * Displays the synchronization status between all document formats
 * Shows which formats have matching data
 *
 * @example
 * ```tsx
 * <SyncStatus
 *   cvData={myCV}
 *   pollInterval={5000}
 *   showDetails={true}
 * />
 * ```
 */
export const SyncStatus: React.FC<SyncStatusProps> = ({
  cvData,
  pollInterval = 0,
  className = "",
  showDetails = false,
  onStatusChange,
}) => {
  const [report, setReport] = useState<SyncVerifyResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const verifySynchronization = async () => {
    try {
      setLoading(true);
      setError(null);

      const client = getApiClient();
      const response = await client.verifySynchronization(cvData);

      if (response.data) {
        setReport(response.data);
        onStatusChange?.(response.data.status);
      } else if (response.error) {
        setError(response.error.message);
        onStatusChange?.("error");
      }
    } catch (err) {
      const message = err instanceof Error ? err.message : "Verification failed";
      setError(message);
      onStatusChange?.("error");
    } finally {
      setLoading(false);
    }
  };

  // Initial verification
  useEffect(() => {
    verifySynchronization();
  }, []);

  // Polling
  useEffect(() => {
    if (pollInterval <= 0) return;

    const interval = setInterval(() => {
      verifySynchronization();
    }, pollInterval);

    return () => clearInterval(interval);
  }, [pollInterval, cvData]);

  if (loading && !report) {
    return (
      <div className={`p-4 bg-gray-100 rounded ${className}`}>
        <p className="text-gray-600">Verifying synchronization...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`p-4 bg-red-50 border border-red-200 rounded ${className}`}>
        <p className="text-red-700 font-semibold">Sync Error</p>
        <p className="text-red-600 text-sm">{error}</p>
      </div>
    );
  }

  if (!report) {
    return null;
  }

  const statusColors = {
    success: "bg-green-50 border-green-200",
    warning: "bg-yellow-50 border-yellow-200",
    error: "bg-red-50 border-red-200",
  };

  const statusTextColors = {
    success: "text-green-700",
    warning: "text-yellow-700",
    error: "text-red-700",
  };

  const statusIcons = {
    success: "✓",
    warning: "⚠",
    error: "✗",
  };

  return (
    <div
      className={`p-4 border rounded ${statusColors[report.status]} ${className}`}
    >
      <div className="flex items-center gap-2 mb-2">
        <span className={`text-xl ${statusTextColors[report.status]}`}>
          {statusIcons[report.status]}
        </span>
        <p className={`font-semibold ${statusTextColors[report.status]}`}>
          {report.status === "success"
            ? "✓ All formats synchronized"
            : report.status === "warning"
              ? "⚠ Partial sync"
              : "✗ Sync error"}
        </p>
      </div>

      {showDetails && report.sync_report && (
        <div className="text-sm text-gray-700 mt-3 space-y-1">
          <p>
            <strong>Certificates:</strong> {report.sync_report.total_certificates}
          </p>
          <p>
            <strong>Skills:</strong> {report.sync_report.total_skills}
          </p>
          <p>
            <strong>Matched Formats:</strong>{" "}
            {report.sync_report.matched_formats.join(", ") || "None"}
          </p>

          {report.sync_report.mismatches.length > 0 && (
            <div className="mt-2 p-2 bg-red-100 rounded">
              <p className="font-semibold text-red-700">Mismatches:</p>
              <ul className="text-red-600">
                {report.sync_report.mismatches.map((mismatch, idx) => (
                  <li key={idx}>• {mismatch.field}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      <p className="text-xs text-gray-500 mt-2">
        {report.message}
      </p>

      {loading && (
        <p className="text-xs text-gray-500 mt-2">Updating...</p>
      )}
    </div>
  );
};
