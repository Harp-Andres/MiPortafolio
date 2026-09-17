/**
 * @mportafolio/api-client
 * 
 * Type-safe API client for Mi Portafolio backend
 * Re-exports all types and client functionality
 */

// Types
export type {
  Skill,
  SkillCategory,
  Experience,
  Education,
  Certificate,
  Profile,
  CVData,
  DocumentFormat,
  GenerateDocumentRequest,
  SyncVerifyRequest,
  GenerateDocumentResponse,
  SyncMismatch,
  SyncPresenceFlags,
  SyncVerifyResponse,
  HealthCheckResponse,
  ApiErrorResponse,
  ClientConfig,
  RequestOptions,
  ApiResponse,
  FileBlob,
  AsyncResult,
} from "./types/index";

// Client
export { ApiClient, createApiClient, initializeApiClient, getApiClient } from "./client";

// Version
export const version = "1.0.0";
