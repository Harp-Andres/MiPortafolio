# 🏗️ MIGRATION PLAN: SOLID/Clean Architecture Refactor

**Status:** IN PROGRESS  
**Date:** 2026-09-14  
**Complexity:** Senior Level  
**Estimated Time:** 4-6 hours  

---

## 📋 FASE 1: AUDIT & PLANNING

### Estado Actual
```
packages/
├── backend/        (Python FastAPI)
├── core/           (TS data types)
└── web/            (React + Vite)

Root files:
├── monorepo configs (package.json, pnpm-workspace.yaml)
├── Testing (vitest, playwright)
├── CI/CD (basic GitHub Actions)
```

### Estado Objetivo
```
mi-monorepo/
├── apps/
│   ├── web/                          # React frontend
│   │   ├── src/
│   │   │   ├── components/           # UI components
│   │   │   ├── pages/                # Route pages
│   │   │   ├── hooks/                # Custom hooks
│   │   │   ├── services/             # API calls (uses api-client)
│   │   │   └── types/                # Local types
│   │   └── package.json
│   │
│   └── api/                          # Python backend (Hexagonal)
│       ├── app/
│       │   ├── api/                  # HTTP Endpoints (Controllers)
│       │   │   ├── routes/           # FastAPI route groups
│       │   │   └── middlewares/      # Authentication, CORS, etc
│       │   ├── domain/               # Business Logic (Entities, Use Cases)
│       │   │   ├── entities/         # Domain models
│       │   │   ├── repositories/     # Abstract interfaces
│       │   │   └── use_cases/        # Business workflows
│       │   ├── services/             # Infrastructure (Generators, DB, etc)
│       │   │   ├── generators/       # DOCX, PDF, Excel
│       │   │   └── validators/       # Data validation
│       │   ├── config/               # Configuration
│       │   └── dependencies.py       # Dependency injection
│       ├── tests/                    # pytest suite
│       ├── pyproject.toml            # Poetry/UV deps
│       └── README.md
│
├── packages/
│   ├── api-client/                   # TypeScript API interface (from core)
│   │   ├── src/
│   │   │   ├── types/                # API types (request/response)
│   │   │   ├── client.ts             # HTTP client
│   │   │   └── index.ts              # Public API
│   │   ├── package.json
│   │   └── tsconfig.json
│   │
│   ├── ui/                           # Reusable React components
│   │   ├── src/
│   │   │   ├── components/           # Shadcn/UI or custom components
│   │   │   └── index.ts              # Barrel exports
│   │   ├── package.json
│   │   └── tsconfig.json
│   │
│   └── config/                       # Shared configs
│       ├── eslint-config/
│       ├── prettier-config/
│       ├── tsconfig/
│       └── package.json
│
├── testing/
│   ├── e2e/                          # End-to-End tests (Playwright)
│   │   ├── tests/
│   │   │   ├── auth.spec.ts
│   │   │   ├── documents.spec.ts
│   │   │   └── sync.spec.ts
│   │   ├── playwright.config.ts
│   │   └── package.json
│   │
│   └── performance/                  # Load/Stress testing
│       ├── scenarios/
│       └── package.json
│
├── infrastructure/
│   ├── docker/
│   │   ├── Dockerfile.web
│   │   ├── Dockerfile.api
│   │   └── docker-compose.yml
│   ├── kubernetes/                   # (future)
│   └── README.md
│
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                    # Lint, Test, Build
│   │   ├── security.yml              # SAST, Dependency check
│   │   └── deploy.yml                # Deployment pipeline
│   └── copilot-instructions.md       # Architecture rules for AI
│
├── .editorconfig
├── .gitignore
├── turbo.json                        # Task orchestration
├── pnpm-workspace.yaml               # Workspace config
├── package.json                      # Root package
├── tsconfig.base.json                # Shared TS config
└── README.md
```

---

## 🎯 FASE 2: MIGRATION STEPS

### Step 1: Create New Directory Structure (5 min)
- [ ] Create `apps/` directory
- [ ] Create `packages/` subdirectories
- [ ] Create `testing/` with e2e & performance
- [ ] Create `infrastructure/` with docker

### Step 2: Migrate Frontend (15 min)
- [ ] Move `packages/web` → `apps/web`
- [ ] Update `apps/web/package.json` dependencies (remove @mportafolio/core)
- [ ] Remove vite/vitest configs from root
- [ ] Create `apps/web/vitest.config.ts` locally

### Step 3: Migrate Backend (20 min)
- [ ] Move `packages/backend` → `apps/api`
- [ ] Refactor directory structure:
  ```
  app/
  ├── api/routes/          (FROM: root, grouped endpoints)
  ├── domain/              (FROM: models, entities, interfaces)
  ├── services/            (FROM: generators, validators)
  └── config/              (FROM: existing config)
  ```
- [ ] Create `dependencies.py` for DI
- [ ] Update imports everywhere

### Step 4: Create API Client Package (10 min)
- [ ] Create `packages/api-client/` directory
- [ ] Move `packages/core/src/data/` → keep as reference
- [ ] Create TypeScript types for API responses:
  ```typescript
  export interface GenerateDocumentRequest { format: 'docx' | 'pdf' | 'excel' }
  export interface SyncVerifyResponse { status: 'success' | 'error'; message: string }
  ```
- [ ] Create HTTP client wrapper

### Step 5: Create UI Components Package (10 min)
- [ ] Create `packages/ui/` directory
- [ ] Organize existing React components:
  ```
  ui/components/
  ├── DownloadButton.tsx
  ├── DocumentPreview.tsx
  ├── SyncStatus.tsx
  └── index.ts
  ```

### Step 6: Create Shared Config Package (5 min)
- [ ] Create `packages/config/` with:
  - eslint-config
  - tsconfig/base.json (shared)
  - prettier config

### Step 7: Migrate Testing to Central Location (10 min)
- [ ] Create `testing/e2e/` with Playwright tests
- [ ] Move root `tests/` → `testing/e2e/tests/`
- [ ] Create `testing/e2e/playwright.config.ts`
- [ ] Create `testing/performance/` structure

### Step 8: Create Infrastructure (5 min)
- [ ] Create `infrastructure/docker/Dockerfile.web`
- [ ] Create `infrastructure/docker/Dockerfile.api`
- [ ] Create `infrastructure/docker/docker-compose.yml`

### Step 9: Update Monorepo Configs (10 min)
- [ ] Create `turbo.json` for task orchestration
- [ ] Update `pnpm-workspace.yaml` with new paths
- [ ] Create `tsconfig.base.json` in root
- [ ] Update root `package.json` with new workspaces

### Step 10: Create CI/CD & Architecture Docs (10 min)
- [ ] Create `.github/workflows/ci.yml`
- [ ] Create `.github/workflows/security.yml`
- [ ] Create `.github/copilot-instructions.md`
- [ ] Create `ARCHITECTURE.md` at root

### Step 11: Update Imports & Dependencies (20 min)
- [ ] Update all TypeScript imports
- [ ] Update Python imports (backend)
- [ ] Fix circular dependencies
- [ ] Run build & tests

### Step 12: Final Verification (10 min)
- [ ] All tests pass ✅
- [ ] Build succeeds ✅
- [ ] No TypeScript errors ✅
- [ ] Documentation complete ✅

---

## ⏱️ TIMELINE

| Phase | Duration | Tasks |
|-------|----------|-------|
| 1. Create directories | 5 min | Structure setup |
| 2. Migrate frontend | 15 min | Move web to apps/ |
| 3. Migrate backend | 20 min | Refactor Python layers |
| 4. Create api-client | 10 min | Types & HTTP client |
| 5. Create ui package | 10 min | Component library |
| 6. Shared config | 5 min | eslint, prettier, ts |
| 7. Testing structure | 10 min | E2E & performance |
| 8. Infrastructure | 5 min | Docker files |
| 9. Monorepo configs | 10 min | turbo, pnpm, ts |
| 10. CI/CD & docs | 10 min | Workflows & rules |
| 11. Fix imports | 20 min | All dependencies |
| 12. Verify & test | 10 min | Full validation |

**Total: ~130 minutes (~2 hours)**

---

## 🔍 VALIDATION CHECKLIST

After migration:
```
✅ Directory structure matches objective
✅ All imports working (TS + Python)
✅ All tests passing
✅ TypeScript: 0 errors
✅ Python: No linting errors
✅ Build succeeds
✅ Monorepo commands work
✅ CI/CD configured
✅ Documentation complete
```

---

## 📝 NOTES

- **Backwards compatibility:** Need to update all imports
- **Python DI:** Use dependency_injector or manual DI for SOLID
- **API client:** Will be consumed by React apps
- **CI/CD:** Will enforce architecture rules via linters
- **Documentation:** copilot-instructions.md will guide AI to maintain structure

---

**Ready to begin?** → Start with FASE 2, Step 1
