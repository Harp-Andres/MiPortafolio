/**
 * Mi Portafolio API Types
 * 
 * Type-safe interfaces for frontend-backend communication
 * Following OpenAPI/REST conventions
 */

// ============================================================================
// DOMAIN TYPES
// ============================================================================

export interface Skill {
  name: string;
  level?: "beginner" | "intermediate" | "advanced" | "expert";
}

export interface SkillCategory {
  category: string;
  skills: Skill[];
}

export interface Experience {
  id: string;
  title: string;
  company: string;
  period: string;
  description: string;
  technologies?: string[];
  achievements?: string[];
}

export interface Education {
  id: string;
  degree: string;
  institution: string;
  graduation: string;
  description?: string;
}

export interface Certificate {
  id: string;
  name: string;
  issuer: string;
  date: string;
  credentialURL?: string;
  hours?: number;
}

export interface Profile {
  name: string;
  title: string;
  email: string;
  phone: string;
  location: string;
  birthDate?: string;
  bio: string;
  github: string;
  linkedin: string;
  portfolio: string;
}

export interface CVData {
  profile: Profile;
  skills: SkillCategory[];
  experience: Experience[];
  education: Education[];
  certificates: Record<string, Certificate[]>;
}

// ============================================================================
// API REQUEST TYPES
// ============================================================================

export type DocumentFormat = "docx" | "pdf" | "excel" | "all";

export interface GenerateDocumentRequest {
  format: DocumentFormat;
  cv_data: CVData;
}

export interface SyncVerifyRequest {
  cv_data: CVData;
}

// ============================================================================
// API RESPONSE TYPES
// ============================================================================

export type ResponseStatus = "success" | "warning" | "error";

export interface GenerateDocumentResponse {
  status: ResponseStatus;
  format?: DocumentFormat;
  file_url?: string;
  file_name?: string;
  message: string;
  timestamp: string;
}

export interface SyncMismatch {
  field: string;
  web_value: unknown;
  document_value: unknown;
}

export interface SyncPresenceFlags {
  web_has_data: boolean;
  docx_has_data: boolean;
  pdf_has_data: boolean;
  excel_has_data: boolean;
}

export interface SyncVerifyResponse {
  status: ResponseStatus;
  timestamp: string;
  sync_report: {
    total_certificates: number;
    total_skills: number;
    total_experience: number;
    total_education: number;
    matched_formats: string[];
    mismatches: SyncMismatch[];
    presence_flags: SyncPresenceFlags;
  };
  message: string;
}

export interface HealthCheckResponse {
  status: "ok" | "error";
  timestamp: string;
  service: string;
  version: string;
}

export interface ApiErrorResponse {
  status: "error";
  message: string;
  timestamp: string;
  error_code?: string;
  details?: Record<string, unknown>;
}

// ============================================================================
// HTTP CLIENT TYPES
// ============================================================================

export interface ClientConfig {
  baseURL: string;
  timeout?: number;
  headers?: Record<string, string>;
}

export interface RequestOptions {
  headers?: Record<string, string>;
  timeout?: number;
  params?: Record<string, unknown>;
}

export interface ApiResponse<T> {
  data?: T;
  error?: ApiErrorResponse;
  status: number;
  statusText: string;
}

// ============================================================================
// UTILITY TYPES
// ============================================================================

export type AsyncResult<T> = Promise<T>;

export interface FileBlob {
  data: Blob;
  filename: string;
  mimeType: string;
}
