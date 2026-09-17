import React, { useState } from "react";
import type { CVData, DocumentFormat } from "@mportafolio/api-client";
import { getApiClient } from "@mportafolio/api-client";

export interface DocumentDownloadButtonProps {
  /**
   * Document format to generate
   */
  format: DocumentFormat;

  /**
   * CV data to generate from
   */
  cvData: CVData;

  /**
   * Button label/text
   */
  label?: string;

  /**
   * Custom filename for download (without extension)
   */
  filename?: string;

  /**
   * CSS class name
   */
  className?: string;

  /**
   * Callback when download starts
   */
  onStart?: () => void;

  /**
   * Callback when download succeeds
   */
  onSuccess?: (filename: string) => void;

  /**
   * Callback when download fails
   */
  onError?: (error: Error) => void;

  /**
   * Disable button
   */
  disabled?: boolean;

  /**
   * Show loading state
   */
  showLoading?: boolean;
}

const defaultLabels: Record<DocumentFormat, string> = {
  docx: "Download DOCX",
  pdf: "Download PDF",
  excel: "Download Excel",
  all: "Download All",
};

const defaultFilenames: Record<DocumentFormat, string> = {
  docx: "CV",
  pdf: "CV",
  excel: "CV",
  all: "CV-all",
};

const fileExtensions: Record<DocumentFormat, string> = {
  docx: ".docx",
  pdf: ".pdf",
  excel: ".xlsx",
  all: "",
};

/**
 * DocumentDownloadButton
 *
 * Renders a button that downloads a generated document from the backend API
 * Handles loading, error states, and file download
 *
 * @example
 * ```tsx
 * <DocumentDownloadButton
 *   format="docx"
 *   cvData={myCV}
 *   label="Get Word Document"
 *   onSuccess={() => console.log("Downloaded!")}
 * />
 * ```
 */
export const DocumentDownloadButton: React.FC<DocumentDownloadButtonProps> = ({
  format,
  cvData,
  label,
  filename,
  className,
  onStart,
  onSuccess,
  onError,
  disabled = false,
  showLoading = true,
}) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleDownload = async () => {
    try {
      setIsLoading(true);
      setError(null);
      onStart?.();

      const client = getApiClient();
      const finalFilename =
        (filename || defaultFilenames[format]) + fileExtensions[format];

      await client.downloadDocument(format, cvData, finalFilename);

      onSuccess?.(finalFilename);
    } catch (err) {
      const error = err instanceof Error ? err : new Error(String(err));
      setError(error.message);
      onError?.(error);
      console.error(`Failed to download ${format}:`, error);
    } finally {
      setIsLoading(false);
    }
  };

  const buttonLabel = label || defaultLabels[format];
  const isDisabled = disabled || isLoading;

  return (
    <div className={className}>
      <button
        onClick={handleDownload}
        disabled={isDisabled}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {showLoading && isLoading ? "Downloading..." : buttonLabel}
      </button>

      {error && (
        <div className="mt-2 text-red-600 text-sm">
          Error: {error}
        </div>
      )}
    </div>
  );
};
