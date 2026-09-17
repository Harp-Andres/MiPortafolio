/**
 * HTTP API Client
 * 
 * Type-safe wrapper for all API endpoints
 * Handles authentication, error handling, and response parsing
 */

import type {
  ClientConfig,
  RequestOptions,
  ApiResponse,
  GenerateDocumentRequest,
  GenerateDocumentResponse,
  SyncVerifyRequest,
  SyncVerifyResponse,
  HealthCheckResponse,
  DocumentFormat,
  CVData,
  FileBlob,
} from "./types/index";

export class ApiClient {
  private baseURL: string;
  private timeout: number;
  private headers: Record<string, string>;

  constructor(config: ClientConfig) {
    this.baseURL = config.baseURL;
    this.timeout = config.timeout || 30000;
    this.headers = {
      "Content-Type": "application/json",
      ...config.headers,
    };
  }

  /**
   * Make an HTTP request
   */
  private async request<T>(
    method: "GET" | "POST" | "PUT" | "DELETE",
    endpoint: string,
    options?: RequestOptions & { data?: unknown }
  ): Promise<ApiResponse<T>> {
    const url = `${this.baseURL}${endpoint}`;
    const headers = { ...this.headers, ...options?.headers };
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(url, {
        method,
        headers,
        body: options?.data ? JSON.stringify(options.data) : undefined,
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      const contentType = response.headers.get("content-type");
      let data;

      if (contentType?.includes("application/json")) {
        data = await response.json();
      } else if (contentType?.includes("application/octet-stream")) {
        data = await response.blob();
      } else {
        data = await response.text();
      }

      return {
        data,
        status: response.status,
        statusText: response.statusText,
      };
    } catch (error: unknown) {
      clearTimeout(timeoutId);

      const errorMessage =
        error instanceof Error ? error.message : "Unknown error occurred";

      return {
        error: {
          status: "error",
          message: errorMessage,
          timestamp: new Date().toISOString(),
          error_code: "NETWORK_ERROR",
        },
        status: 0,
        statusText: "Network Error",
      };
    }
  }

  // ========================================================================
  // DOCUMENT GENERATION ENDPOINTS
  // ========================================================================

  /**
   * Generate DOCX document
   */
  async generateDocx(cvData: CVData): Promise<ApiResponse<Blob>> {
    return this.request<Blob>("POST", "/api/generate/docx", {
      data: { cv_data: cvData },
    });
  }

  /**
   * Generate PDF document
   */
  async generatePdf(cvData: CVData): Promise<ApiResponse<Blob>> {
    return this.request<Blob>("POST", "/api/generate/pdf", {
      data: { cv_data: cvData },
    });
  }

  /**
   * Generate Excel document
   */
  async generateExcel(cvData: CVData): Promise<ApiResponse<Blob>> {
    return this.request<Blob>("POST", "/api/generate/excel", {
      data: { cv_data: cvData },
    });
  }

  /**
   * Generate all document formats at once
   */
  async generateAll(cvData: CVData): Promise<ApiResponse<Record<string, Blob>>> {
    return this.request<Record<string, Blob>>("POST", "/api/generate/all", {
      data: { cv_data: cvData },
    });
  }

  /**
   * Generate document by format
   */
  async generateDocument(
    format: DocumentFormat,
    cvData: CVData
  ): Promise<ApiResponse<Blob | Record<string, Blob>>> {
    switch (format) {
      case "docx":
        return this.generateDocx(cvData);
      case "pdf":
        return this.generatePdf(cvData);
      case "excel":
        return this.generateExcel(cvData);
      case "all":
        return this.generateAll(cvData);
      default:
        throw new Error(`Unknown document format: ${format}`);
    }
  }

  // ========================================================================
  // SYNCHRONIZATION ENDPOINTS
  // ========================================================================

  /**
   * Verify data synchronization across all formats
   */
  async verifySynchronization(
    cvData: CVData
  ): Promise<ApiResponse<SyncVerifyResponse>> {
    return this.request<SyncVerifyResponse>("POST", "/api/sync/verify", {
      data: { cv_data: cvData },
    });
  }

  // ========================================================================
  // HEALTH CHECK
  // ========================================================================

  /**
   * Check API health status
   */
  async healthCheck(): Promise<ApiResponse<HealthCheckResponse>> {
    return this.request<HealthCheckResponse>("GET", "/health");
  }

  /**
   * Get API information
   */
  async getInfo(): Promise<ApiResponse<unknown>> {
    return this.request("GET", "/");
  }

  // ========================================================================
  // FILE DOWNLOAD HELPERS
  // ========================================================================

  /**
   * Download file as blob
   */
  private downloadFile(blob: Blob, filename: string): void {
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  }

  /**
   * Generate and download DOCX
   */
  async downloadDocx(cvData: CVData, filename = "CV.docx"): Promise<void> {
    const response = await this.generateDocx(cvData);
    if (response.data && response.data instanceof Blob) {
      this.downloadFile(response.data, filename);
    } else if (response.error) {
      throw new Error(response.error.message);
    }
  }

  /**
   * Generate and download PDF
   */
  async downloadPdf(cvData: CVData, filename = "CV.pdf"): Promise<void> {
    const response = await this.generatePdf(cvData);
    if (response.data && response.data instanceof Blob) {
      this.downloadFile(response.data, filename);
    } else if (response.error) {
      throw new Error(response.error.message);
    }
  }

  /**
   * Generate and download Excel
   */
  async downloadExcel(
    cvData: CVData,
    filename = "CV.xlsx"
  ): Promise<void> {
    const response = await this.generateExcel(cvData);
    if (response.data && response.data instanceof Blob) {
      this.downloadFile(response.data, filename);
    } else if (response.error) {
      throw new Error(response.error.message);
    }
  }

  /**
   * Generate and download by format
   */
  async downloadDocument(
    format: DocumentFormat,
    cvData: CVData,
    filename?: string
  ): Promise<void> {
    switch (format) {
      case "docx":
        return this.downloadDocx(cvData, filename);
      case "pdf":
        return this.downloadPdf(cvData, filename);
      case "excel":
        return this.downloadExcel(cvData, filename);
      case "all":
        throw new Error("Use downloadAll() for multiple formats");
      default:
        throw new Error(`Unknown document format: ${format}`);
    }
  }
}

// ============================================================================
// FACTORY FUNCTION
// ============================================================================

/**
 * Create API client instance
 * Usage: const client = createApiClient("http://localhost:8000");
 */
export function createApiClient(baseURL: string, config?: Partial<ClientConfig>): ApiClient {
  return new ApiClient({
    baseURL,
    ...config,
  });
}

// ============================================================================
// SINGLETON INSTANCE
// ============================================================================

let globalClient: ApiClient | null = null;

/**
 * Initialize global API client
 * Call once at application startup
 */
export function initializeApiClient(baseURL: string, config?: Partial<ClientConfig>): ApiClient {
  globalClient = createApiClient(baseURL, config);
  return globalClient;
}

/**
 * Get global API client instance
 */
export function getApiClient(): ApiClient {
  if (!globalClient) {
    throw new Error(
      "API client not initialized. Call initializeApiClient() first."
    );
  }
  return globalClient;
}

// ============================================================================
// EXPORTS
// ============================================================================

export type { ClientConfig, RequestOptions, ApiResponse, FileBlob };
export * from "./types/index";
