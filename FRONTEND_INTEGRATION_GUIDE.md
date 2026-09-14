# 🔗 FRONTEND INTEGRATION GUIDE

**Status:** Ready for Implementation  
**Priority:** HIGH - Needed for API communication  
**Time Estimate:** 30-45 minutes  

---

## 📋 WHAT WAS CREATED

### 1. **API Client Package** (`packages/api-client/`)
- ✅ Type-safe API types (Request/Response DTOs)
- ✅ HTTP client with fetch wrapper
- ✅ Document generation endpoints
- ✅ Sync verification endpoint
- ✅ File download helpers
- ✅ Error handling & retry logic

**Usage:**
```typescript
import { initializeApiClient, getApiClient } from "@mportafolio/api-client";

// Initialize once at app startup
initializeApiClient("http://localhost:8000");

// Use in any component
const client = getApiClient();
const response = await client.generateDocx(cvData);
```

### 2. **UI Components Package** (`packages/ui/`)
- ✅ `DocumentDownloadButton` - Download individual formats
- ✅ `SyncStatus` - Show sync verification status
- ✅ `DocumentGenerator` - Complete UI for all operations

**Usage:**
```typescript
import { DocumentGenerator } from "@mportafolio/ui";

<DocumentGenerator
  cvData={myCV}
  showSyncStatus={true}
  showIndividualButtons={true}
/>
```

---

## 🔧 INTEGRATION STEPS

### Step 1: Update Root package.json Workspaces

Edit root `package.json`:

```json
{
  "workspaces": [
    "apps/web",
    "apps/api",
    "packages/api-client",
    "packages/ui",
    "packages/config",
    "testing/e2e"
  ]
}
```

### Step 2: Update pnpm-workspace.yaml

Edit `pnpm-workspace.yaml`:

```yaml
packages:
  - 'apps/**'
  - 'packages/**'
  - 'testing/**'
```

### Step 3: Initialize Frontend Package

In `apps/web/package.json`, add dependencies:

```json
{
  "dependencies": {
    "@mportafolio/api-client": "workspace:*",
    "@mportafolio/ui": "workspace:*"
  }
}
```

Then run:
```bash
pnpm install
pnpm build -r  # Build all packages
```

### Step 4: Create API Service Hook

Create `apps/web/src/hooks/useDocuments.ts`:

```typescript
import { useState, useCallback } from "react";
import { getApiClient } from "@mportafolio/api-client";
import type { CVData, DocumentFormat } from "@mportafolio/api-client";

export function useDocuments(cvData: CVData) {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastDownload, setLastDownload] = useState<string | null>(null);

  const downloadDocument = useCallback(
    async (format: DocumentFormat) => {
      try {
        setIsLoading(true);
        setError(null);
        const client = getApiClient();
        
        const filename = `CV.${format === 'docx' ? 'docx' : format === 'pdf' ? 'pdf' : 'xlsx'}`;
        await client.downloadDocument(format, cvData, filename);
        setLastDownload(filename);
      } catch (err) {
        const message = err instanceof Error ? err.message : "Unknown error";
        setError(message);
        throw err;
      } finally {
        setIsLoading(false);
      }
    },
    [cvData]
  );

  return { downloadDocument, isLoading, error, lastDownload };
}
```

### Step 5: Create Sync Status Hook

Create `apps/web/src/hooks/useSync.ts`:

```typescript
import { useState, useEffect } from "react";
import { getApiClient } from "@mportafolio/api-client";
import type { CVData, SyncVerifyResponse } from "@mportafolio/api-client";

export function useSync(cvData: CVData, pollInterval = 0) {
  const [report, setReport] = useState<SyncVerifyResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const verifySynchronization = async () => {
      try {
        setLoading(true);
        const client = getApiClient();
        const response = await client.verifySynchronization(cvData);
        if (response.data) {
          setReport(response.data);
        } else if (response.error) {
          setError(response.error.message);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : "Verification failed");
      } finally {
        setLoading(false);
      }
    };

    verifySynchronization();

    if (pollInterval <= 0) return;

    const interval = setInterval(verifySynchronization, pollInterval);
    return () => clearInterval(interval);
  }, [cvData, pollInterval]);

  return { report, loading, error };
}
```

### Step 6: Integrate into Pages

Update `apps/web/src/pages/Portfolio.tsx` (or wherever appropriate):

```typescript
import { useEffect } from "react";
import { initializeApiClient } from "@mportafolio/api-client";
import { DocumentGenerator } from "@mportafolio/ui";
import { cvData } from "@mportafolio/core/src/data/cv-data";

function Portfolio() {
  // Initialize API client once
  useEffect(() => {
    const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
    initializeApiClient(apiBaseUrl);
  }, []);

  return (
    <div>
      {/* ... existing portfolio content ... */}
      
      <section className="mt-12">
        <DocumentGenerator
          cvData={cvData}
          showSyncStatus={true}
          showIndividualButtons={true}
          showDownloadAll={true}
        />
      </section>
    </div>
  );
}

export default Portfolio;
```

### Step 7: Configure Environment Variables

Create `.env.local` in `apps/web/`:

```env
# API Configuration
VITE_API_BASE_URL=http://localhost:8000

# Optional: Enable debug logging
VITE_DEBUG=false
```

For production:
```env
VITE_API_BASE_URL=https://api.mportafolio.com
```

### Step 8: Update .gitignore

Add to root `.gitignore`:

```
# Monorepo
pnpm-lock.yaml
node_modules/

# Build outputs
dist/
build/
*.tsbuildinfo

# Environment
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
```

---

## 🧪 TESTING INTEGRATION

### Test 1: API Client Connectivity

Create `apps/web/src/__tests__/api.test.ts`:

```typescript
import { describe, it, expect } from "vitest";
import { initializeApiClient, getApiClient } from "@mportafolio/api-client";

describe("API Client", () => {
  it("should initialize successfully", () => {
    initializeApiClient("http://localhost:8000");
    const client = getApiClient();
    expect(client).toBeDefined();
  });

  it("should have required methods", () => {
    const client = getApiClient();
    expect(client.generateDocx).toBeDefined();
    expect(client.generatePdf).toBeDefined();
    expect(client.generateExcel).toBeDefined();
    expect(client.verifySynchronization).toBeDefined();
  });
});
```

### Test 2: Component Rendering

Create `apps/web/src/__tests__/DocumentGenerator.test.tsx`:

```typescript
import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import { DocumentGenerator } from "@mportafolio/ui";
import { sampleCVData } from "./fixtures/cv-data";

describe("DocumentGenerator Component", () => {
  it("should render successfully", () => {
    render(<DocumentGenerator cvData={sampleCVData} />);
    expect(screen.getByText(/Document Generator/i)).toBeInTheDocument();
  });

  it("should display all download buttons", () => {
    render(
      <DocumentGenerator cvData={sampleCVData} showIndividualButtons={true} />
    );
    expect(screen.getByText(/Word/i)).toBeInTheDocument();
    expect(screen.getByText(/PDF/i)).toBeInTheDocument();
    expect(screen.getByText(/Excel/i)).toBeInTheDocument();
  });
});
```

---

## 🔌 BACKEND COMPATIBILITY

### Expected API Endpoints

The frontend expects these endpoints to exist:

```
POST /api/generate/docx
  Request:  { cv_data: CVData }
  Response: Blob (Word document)

POST /api/generate/pdf
  Request:  { cv_data: CVData }
  Response: Blob (PDF document)

POST /api/generate/excel
  Request:  { cv_data: CVData }
  Response: Blob (Excel workbook)

POST /api/sync/verify
  Request:  { cv_data: CVData }
  Response: SyncVerifyResponse { status, sync_report, message }

GET /health
  Response: { status: "ok", timestamp, service, version }
```

### CORS Setup Required

Backend must enable CORS for frontend:

```python
# apps/api/app/api/main.py
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",      # Dev
        "http://localhost:4173",      # Preview
        "https://Harp-Andres.github.io",  # Production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📊 FEATURE CHECKLIST

### Components Ready ✅
- [x] DocumentDownloadButton
- [x] SyncStatus
- [x] DocumentGenerator

### API Client Ready ✅
- [x] TypeScript types/DTOs
- [x] HTTP client
- [x] Document generation
- [x] Sync verification
- [x] Error handling

### Frontend Integration TODO
- [ ] Add dependencies to apps/web/package.json
- [ ] Create hooks (useDocuments, useSync)
- [ ] Integrate components into pages
- [ ] Configure environment variables
- [ ] Add tests
- [ ] Test end-to-end flow

### Backend Integration TODO
- [ ] Refactor Python to Clean Architecture layers
- [ ] Ensure all endpoints exist
- [ ] Configure CORS
- [ ] Add authentication (if needed)
- [ ] Test all endpoints

---

## 🚀 DEPLOYMENT CHECKLIST

### Development
```bash
# Terminal 1: Frontend
cd apps/web
pnpm install
pnpm dev

# Terminal 2: Backend
cd apps/api
python -m uvicorn app.api.main:app --reload

# Terminal 3: Tests
pnpm test -r
```

### Production
```bash
# Build all packages
pnpm build -r

# Deploy frontend to GitHub Pages
cd apps/web
pnpm run deploy

# Deploy backend to server/cloud
# (Docker, cloud functions, etc.)
```

---

## 🔗 QUICK REFERENCE

### Import Paths (After Integration)

```typescript
// API Client
import { 
  initializeApiClient, 
  getApiClient,
  type CVData,
  type DocumentFormat 
} from "@mportafolio/api-client";

// UI Components
import { 
  DocumentGenerator,
  DocumentDownloadButton,
  SyncStatus 
} from "@mportafolio/ui";

// Hooks
import { useDocuments } from "./hooks/useDocuments";
import { useSync } from "./hooks/useSync";
```

### Component Usage

```typescript
// Option 1: Complete component
<DocumentGenerator cvData={cvData} />

// Option 2: Individual components
<DocumentDownloadButton format="docx" cvData={cvData} />
<SyncStatus cvData={cvData} showDetails={true} />

// Option 3: Custom hook
const { downloadDocument, isLoading } = useDocuments(cvData);
```

---

## ⚠️ COMMON ISSUES & SOLUTIONS

### Issue 1: CORS Error
**Problem:** "Access to XMLHttpRequest blocked by CORS policy"  
**Solution:** Ensure backend has CORS middleware configured

### Issue 2: API Not Found
**Problem:** 404 on `/api/generate/docx`  
**Solution:** Check backend is running and endpoints are implemented

### Issue 3: Type Errors
**Problem:** "Cannot find module '@mportafolio/api-client'"  
**Solution:** Run `pnpm install` and ensure workspaces are configured

### Issue 4: Environment Variable Not Loaded
**Problem:** API calls to undefined URL  
**Solution:** Create `.env.local` with `VITE_API_BASE_URL`

---

## 📞 SUPPORT & DEBUGGING

### Enable Debug Logging

In component:
```typescript
if (import.meta.env.VITE_DEBUG === 'true') {
  console.log('API Response:', response);
}
```

### Test API Directly

```bash
curl -X POST http://localhost:8000/api/generate/docx \
  -H "Content-Type: application/json" \
  -d @cv-data.json \
  -o CV.docx
```

### Check API Health

```typescript
const client = getApiClient();
const health = await client.healthCheck();
console.log(health);
```

---

```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║         ✅ FRONTEND INTEGRATION READY FOR IMPLEMENTATION      ║
║                                                                ║
║  API Client    ✓  React Components  ✓  Documentation ✓        ║
║  All dependencies configured and types defined.                ║
║                                                                ║
║              Ready to integrate into apps/web!                ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

**Next Steps:**
1. Update apps/web/package.json with new dependencies
2. Create hooks in apps/web/src/hooks/
3. Integrate components into portfolio pages
4. Configure environment variables
5. Test end-to-end flow
6. Deploy to production

**Questions?** Refer to ARCHITECTURE_RULES.md and MIGRATION_PLAN.md
