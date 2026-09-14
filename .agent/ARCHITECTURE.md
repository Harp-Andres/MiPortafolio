```
 __  __          ____            _            __     _       
|  \/  |  ___   |  _ \   ___   __| |  ___  _ __|  \   / | ___ 
| |\/| | / _ \  | |_) | / _ \ / _` | / _ \| '__| |\/ /| |/ _ \
| |  | || (_) | |  _ < | (_) | (_| || (_) | |  | |  / |  __/
|_|  |_| \___/  |_| \_\ \___/ \__,_| \___/|_|  |_|\/  |_|\___|
                                                               
MODERN AI-DRIVEN ARCHITECTURE FOR PORTFOLIO MANAGEMENT
Senior Developer Level | React 19 + TypeScript 7 + Vite 8

=============================================================
```

# 🏗️ MODERN AI ARCHITECTURE SPECIFICATION

**Version:** 2.0 (Enterprise-Grade)  
**Date:** 2026-09-13  
**Framework:** React 19.3.1 + TypeScript 7.0.2 + Vite 8.3.0  
**Architecture Pattern:** Clean Architecture + SOLID Principles  

---

## 📊 ARCHITECTURE OVERVIEW

```mermaid
graph TB
    subgraph "AI Orchestration Layer"
        MasterAgent["🎯 Master Orchestrator<br/>(coordinator)"]
    end
    
    subgraph "Specialized Agent Layer"
        CVAgent["📝 CV & Skills Agent<br/>(cv-update)"]
        DocAgent["📄 Document Sync Agent<br/>(doc-sync)"]
        TestAgent["✅ Testing Agent<br/>(test-orchestrator)"]
        DeployAgent["🚀 Deployment Agent<br/>(deploy)"]
    end
    
    subgraph "Integration Layer"
        CVData["💾 CV Data Repository<br/>(src/utils/cv-data.ts)"]
        Projects["🎯 Projects Repository<br/>(src/types/projects.ts)"]
    end
    
    subgraph "Execution Layer"
        Web["🌐 Web/React<br/>(src/)")
        PDF["📋 PDF CV<br/>(Hoja De Vida/)"]
        Word["📝 Word CV<br/>(DOCX)"]
    end
    
    MasterAgent -->|Orchestrate| CVAgent
    MasterAgent -->|Orchestrate| DocAgent
    MasterAgent -->|Orchestrate| TestAgent
    MasterAgent -->|Orchestrate| DeployAgent
    
    CVAgent -->|Update| CVData
    CVAgent -->|Validate| TestAgent
    DocAgent -->|Sync| Web
    DocAgent -->|Sync| PDF
    DocAgent -->|Sync| Word
    CVData -->|Feed| Web
    Projects -->|Feed| Web
    
    style MasterAgent fill:#ff6b6b,stroke:#c92a2a,color:#fff
    style CVAgent fill:#4c6ef5,stroke:#1971c2,color:#fff
    style DocAgent fill:#15aabf,stroke:#0d8087,color:#fff
    style TestAgent fill:#51cf66,stroke:#2b8a3e,color:#fff
    style DeployAgent fill:#ffd43b,stroke:#e9a000,color:#000
```

---

## 🎯 MASTER ORCHESTRATOR AGENT

**Role:** Central coordinator that manages all specialized agents  
**Responsibility:** Ensure workflow compliance, synchronization, and quality gates

### Core Responsibilities

1. **Workflow Orchestration**
   - Parse user requests
   - Route to appropriate specialized agents
   - Coordinate multi-step operations
   - Handle rollback on failures

2. **Synchronization Enforcement**
   - Guarantee Web = PDF = Word at all times
   - Verify all updates before commit
   - Prevent partial deployments
   - Track sync status in git commits

3. **Quality Gates**
   - Enforce TypeScript zero-errors rule
   - Verify all tests pass (65+ unit, 30+ E2E)
   - Validate build success
   - Check responsive design coverage

4. **Execution Coordination**
   - Sequence operations correctly
   - Wait for completion signals
   - Handle errors and retries
   - Report comprehensive status

---

## 👥 SPECIALIZED AGENT ECOSYSTEM

### 1️⃣ CV & Skills Update Agent

**File:** `.agent/cv-update-specialist.md`  
**Trigger:** `@cv-update` or `@skills`  
**Scope:** Manage CV data, skills, certificates, education, experience

**Capabilities:**
- Add/update skills in categories
- Create new skill categories
- Manage certificates with hours
- Update education entries
- Add/update work experience
- Create learning paths

**Files Modified:**
- `src/utils/cv-data.ts` (primary)
- `src/types/projects.ts` (secondary)

**Output:** Modified TypeScript files + validation report

---

### 2️⃣ Document Synchronization Agent

**File:** `.agent/doc-sync-specialist.md`  
**Trigger:** `@doc-sync` or `@sync`  
**Scope:** Maintain Web = PDF = Word synchronization

**Capabilities:**
- Verify Web content updates
- Regenerate DOCX from cv-data.ts
- Convert DOCX to PDF
- Compare and validate sync
- Generate sync reports
- Detect and reconcile differences

**Files Modified:**
- `scripts/hv/generate-cv-sdet.mjs`
- `Hoja De Vida/*.docx`
- `Hoja De Vida/*.pdf`

**Quality Checks:**
- Content parity verification
- Formatting consistency check
- Link validation
- PDF accessibility check

---

### 3️⃣ Automated Testing Agent

**File:** `.agent/test-orchestrator-specialist.md`  
**Trigger:** `@test` or `@qa`  
**Scope:** Manage all testing operations

**Capabilities:**
- Run unit tests (Vitest 65+ tests)
- Run E2E tests (Playwright 30+ tests)
- Generate coverage reports
- Auto-generate E2E tests for new components
- Visual regression testing
- Performance monitoring

**Test Categories:**
- **Unit Tests** (65+ passing)
  - Components: Skills, Education, About, Navigation, Hero, Certificates
  - Hooks: useAge, useScrollPosition
  - Utils: cv-data validation
  - Download: CV download logic

- **E2E Tests** (30+ passing)
  - Navigation flow
  - Responsive design (360px → 1920px)
  - CV download functionality
  - Mobile menu toggle
  - Portfolio page navigation

**Output:** Test reports + coverage metrics + recommendations

---

### 4️⃣ Deployment Agent

**File:** `.agent/deploy-specialist.md`  
**Trigger:** `@deploy` or `@release`  
**Scope:** Manage GitHub Pages deployment pipeline

**Capabilities:**
- Pre-flight validation checks
- Automated lint verification
- Build compilation
- Test execution verification
- Git commit with proper sync messages
- GitHub Pages deployment
- Rollback on failure

**Deployment Checklist:**
- ✅ `npm run lint` (0 errors)
- ✅ `npm run build` (success)
- ✅ `npm test` (all pass)
- ✅ `npm run test:e2e` (all pass)
- ✅ Web = PDF = Word verified
- ✅ Git commit message format
- ✅ `git push` → auto-deploy
- ✅ GitHub Pages live URL validation

---

## 📁 MODERN PROJECT STRUCTURE

### Recommended Folder Hierarchy

```
MiPortafolio/
│
├── .agent/                              # AI Agent Definitions
│   ├── master-orchestrator.md           # 🎯 Master agent (NEW)
│   ├── cv-update-specialist.md          # 📝 CV updates
│   ├── doc-sync-specialist.md           # 📄 Document sync (NEW)
│   ├── test-orchestrator-specialist.md  # ✅ Testing (NEW)
│   ├── deploy-specialist.md             # 🚀 Deployment
│   └── ARCHITECTURE.md                  # This file
│
├── src/                                 # React + TypeScript Source
│   │
│   ├── components/                      # Reusable UI Components
│   │   ├── common/                      # Shared components
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Modal.tsx
│   │   │   └── __tests__/
│   │   │       └── common.test.tsx
│   │   │
│   │   ├── layout/                      # Layout Components
│   │   │   ├── Header.tsx
│   │   │   ├── Navigation.tsx
│   │   │   ├── Footer.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── __tests__/
│   │   │       └── layout.test.tsx
│   │   │
│   │   ├── sections/                    # Page Sections
│   │   │   ├── Hero.tsx
│   │   │   ├── About.tsx
│   │   │   ├── Skills.tsx
│   │   │   ├── Experience.tsx
│   │   │   ├── Education.tsx
│   │   │   ├── Certificates.tsx
│   │   │   ├── CVDownloads.tsx
│   │   │   └── __tests__/
│   │   │       └── sections.test.tsx
│   │   │
│   │   └── portfolio/                   # Portfolio Components
│   │       ├── ProjectCard.tsx
│   │       ├── ProjectGrid.tsx
│   │       └── __tests__/
│   │           └── portfolio.test.tsx
│   │
│   ├── pages/                           # Page Components (React Router)
│   │   ├── Home.tsx                     # Main CV page
│   │   ├── Portfolio.tsx                # Portfolio showcase
│   │   ├── NotFound.tsx                 # 404 page
│   │   └── __tests__/
│   │       └── pages.test.tsx
│   │
│   ├── hooks/                           # Custom React Hooks
│   │   ├── useAge.ts
│   │   ├── useScrollPosition.ts
│   │   ├── useCopyClean.ts
│   │   ├── useResponsive.ts             # NEW: Responsive detection
│   │   ├── useDocumentSync.ts           # NEW: Sync verification
│   │   └── __tests__/
│   │       └── hooks.test.ts
│   │
│   ├── utils/                           # Utility Functions
│   │   ├── cv-data.ts                   # ⭐ CV Data Repository
│   │   ├── projects-data.ts             # NEW: Projects Data
│   │   ├── download-cv.ts               # CV Download Logic
│   │   ├── sync-validator.ts            # NEW: Verify sync
│   │   ├── constants.ts                 # Application constants
│   │   ├── helpers.ts                   # Helper functions
│   │   └── __tests__/
│   │       ├── cv-data.test.ts
│   │       ├── sync-validator.test.ts   # NEW
│   │       └── utils.test.ts
│   │
│   ├── types/                           # TypeScript Interfaces
│   │   ├── cv.ts                        # CV-related types
│   │   ├── projects.ts                  # Project types
│   │   ├── ui.ts                        # UI component types
│   │   └── index.ts                     # Type exports
│   │
│   ├── styles/                          # Centralized Styles
│   │   ├── index.css                    # Tailwind imports
│   │   ├── tailwind.config.ts           # (moved from root)
│   │   └── theme.ts                     # Theme configuration
│   │
│   ├── App.tsx                          # Root component
│   ├── main.tsx                         # Entry point
│   └── vite-env.d.ts                    # Vite type declarations
│
├── scripts/                             # Automation Scripts
│   ├── hv/
│   │   ├── generate-cv-sdet.mjs         # DOCX generation
│   │   ├── verify-sync.mjs              # NEW: Sync verification
│   │   └── generate-pdf.mjs             # NEW: PDF generation
│   │
│   ├── setup/
│   │   ├── init-project.mjs             # Project initialization
│   │   └── validate-env.mjs             # Environment validation
│   │
│   └── ci/
│       ├── pre-commit.mjs               # Git pre-commit hook
│       └── validate-pr.mjs              # PR validation
│
├── tests/                               # E2E Test Suite
│   ├── e2e/
│   │   ├── portfolio.spec.ts            # Navigation & portfolio
│   │   ├── cv.spec.ts                   # CV download & sync
│   │   ├── responsive.spec.ts           # Responsive design
│   │   └── performance.spec.ts          # Performance tests
│   │
│   ├── fixtures/
│   │   ├── test-data.ts
│   │   └── mock-responses.ts
│   │
│   └── helpers/
│       ├── page-helpers.ts
│       └── assertion-helpers.ts
│
├── .github/
│   └── workflows/
│       ├── deploy.yml                   # Main CI/CD pipeline
│       ├── test.yml                     # Test workflow
│       └── validate-sync.yml            # NEW: Sync validation
│
├── docs/                                # Project Documentation
│   ├── ARCHITECTURE.md                  # Architecture guide (this)
│   ├── DEVELOPMENT.md                   # Development guide
│   ├── TESTING.md                       # Testing strategy
│   ├── DEPLOYMENT.md                    # Deployment guide
│   └── AGENTS.md                        # Agent system docs
│
├── .vscode/                             # VS Code Configuration
│   ├── settings.json                    # Editor settings
│   ├── extensions.json                  # Recommended extensions
│   └── launch.json                      # Debug configuration
│
├── Hoja De Vida/                        # Generated CV Documents
│   ├── HV_2026_ATS_AndesRodriguez.docx  # DOCX (ATS-optimized)
│   ├── HV_2026_Visual_AndesRodriguez.pdf # PDF (visual)
│   └── latest-sync-report.json          # Sync verification log
│
├── public/                              # Static Assets
│   ├── 404.html                         # GitHub Pages 404 redirect
│   ├── favicon.svg
│   ├── certificados/                    # Certificate files
│   └── images/                          # Images & logos
│
├── Configuration Files
│   ├── vite.config.mjs                  # Vite build config
│   ├── vitest.config.ts                 # Unit test config
│   ├── playwright.config.ts             # E2E test config
│   ├── tailwind.config.ts               # Tailwind customization
│   ├── postcss.config.js                # PostCSS config
│   ├── tsconfig.json                    # TypeScript config
│   └── package.json                     # Dependencies & scripts
│
├── Documentation & Guidelines
│   ├── README.md                        # Project overview
│   ├── AGENT_USAGE.md                   # How to use agents
│   ├── ARCHITECTURE.md                  # This file
│   ├── CONTRIBUTING.md                  # Contribution guide
│   └── CHANGELOG.md                     # Version history
│
└── Configuración de Git
    ├── .gitignore
    ├── .gitattributes
    └── .pre-commit-config.yaml          # Pre-commit hooks
```

---

## 🔄 WORKFLOW ORCHESTRATION

### Example: Update CV Skill + Sync All Artifacts

```
User Request:
"Agrega Python y FastAPI a 'Programación & Desarrollo'"
         ↓
┌─────────────────────────────────────────────────────────────┐
│  MASTER ORCHESTRATOR (coordinator)                          │
│  - Parse request                                            │
│  - Validate user authorization                              │
│  - Plan workflow steps                                      │
└─────────────────────────────────────────────────────────────┘
         ↓
    DELEGATE TO SPECIALIST AGENTS
         ↓
┌─────────────────────────────────────────────────────────────┐
│  1️⃣ CV UPDATE SPECIALIST                                     │
│  - Read: src/utils/cv-data.ts                               │
│  - Modify: Add Python, FastAPI to 'Programación & Desarrollo'│
│  - Validate: TypeScript structure OK                        │
│  - Output: Modified cv-data.ts                              │
└─────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────┐
│  2️⃣ DOCUMENT SYNC SPECIALIST                                 │
│  Step A: Verify Web Content                                │
│    - `npm run lint` (✅ 0 errors)                           │
│    - `npm run build` (✅ success)                           │
│    - Check: Web reflects new skills                         │
│                                                             │
│  Step B: Regenerate DOCX                                   │
│    - `node scripts/hv/generate-cv-sdet.mjs`               │
│    - Output: Updated DOCX file                             │
│                                                             │
│  Step C: Convert DOCX to PDF                               │
│    - `node scripts/hv/generate-pdf.mjs`                    │
│    - Output: Updated PDF file                              │
│                                                             │
│  Step D: Verify Sync                                       │
│    - Compare: Web === DOCX === PDF                         │
│    - Run: `node scripts/hv/verify-sync.mjs`               │
│    - Generate: sync-report.json                            │
└─────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────┐
│  3️⃣ TESTING SPECIALIST                                      │
│  - `npm run lint` (✅ TypeScript check)                     │
│  - `npm test` (✅ 65+ unit tests)                           │
│  - `npm run test:e2e` (✅ 30+ E2E tests)                   │
│  - Verify: All tests passing                               │
└─────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────┐
│  4️⃣ DEPLOYMENT SPECIALIST                                   │
│  - Create git commit:                                       │
│    "feat: Agregar Python y FastAPI"                        │
│                                                             │
│    SYNC UPDATE:                                            │
│    - ✅ Web/Portafolio actualizado                         │
│    - ✅ DOCX (ATS) actualizado                             │
│    - ✅ PDF (Visual) actualizado                           │
│                                                             │
│    Changes:                                                │
│    - Added Python to 'Programación & Desarrollo'           │
│    - Added FastAPI to 'Programación & Desarrollo'          │
│                                                             │
│  - `git push` → GitHub Actions auto-deploys               │
│  - Verify: GitHub Pages live update                        │
└─────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────┐
│  MASTER ORCHESTRATOR (final verification)                   │
│  - Collect all agent outputs                               │
│  - Verify: All steps completed successfully                │
│  - Generate comprehensive report                           │
│  - Notify user of completion                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧪 TESTING STRATEGY

### Three-Tier Testing Pyramid

```
        /\
       /  \
      / E2E \          30+ Tests
     /Tests \         Playwright
    /________\      (Browser-based)
     /      \
    /  Unit  \       65+ Tests
   /  Tests   \      Vitest
  /____________\   (Component + Utils)
  / Integration \   20+ Tests
 /  Smoke Tests  \  Quick validation
/________________\
```

### Test Categories

**Unit Tests (65+ passing):**
- Component rendering tests (Skills, Education, About, etc.)
- Hook logic tests (useAge, useScrollPosition)
- Utility function tests (cv-data validation)
- Download functionality tests

**E2E Tests (30+ passing):**
- Navigation and routing
- CV download workflows
- Responsive design verification (360px - 1920px)
- Mobile menu interactions
- Portfolio page display

**Integration Tests (NEW):**
- Web = PDF = Word sync verification
- Data consistency across components
- API/external service mocking

---

## 🚀 DEPLOYMENT PIPELINE

### GitHub Actions Workflow

```
Code Push
   ↓
[Install Dependencies]
   ↓
[Lint - TypeScript Check]
   ↓
[Unit Tests - Vitest]
   ↓
[E2E Tests - Playwright]
   ↓
[Build - Vite Compilation]
   ↓
[Verify Sync - Web=PDF=Word]
   ↓
[Deploy to GitHub Pages]
   ↓
[Notify - Deployment Success]
   ↓
Live URL: https://Harp-Andres.github.io/MiPortafolio
```

---

## 📊 KEY METRICS & MONITORING

### Build Metrics
- **Build Time:** < 30 seconds
- **Bundle Size:** < 500KB (gzipped)
- **TypeScript Errors:** 0 (strict mode)
- **Lint Warnings:** 0

### Test Metrics
- **Unit Test Coverage:** > 80%
- **E2E Test Coverage:** All user flows
- **Test Pass Rate:** 100%
- **Test Execution Time:** < 2 minutes

### Performance Metrics
- **Lighthouse Score:** > 90
- **Core Web Vitals:** All green
- **Mobile First Index:** Optimized
- **Accessibility Score:** > 95

---

## 🔐 QUALITY GATES

### Pre-Commit Checks
- [ ] TypeScript compiles (0 errors)
- [ ] Prettier formatting
- [ ] ESLint validation
- [ ] Unit tests pass

### Pre-Push Checks
- [ ] All unit tests pass (65+)
- [ ] All E2E tests pass (30+)
- [ ] Build succeeds
- [ ] Web = PDF = Word sync verified

### Pre-Deployment Checks
- [ ] GitHub Actions pipeline success
- [ ] Code review approval
- [ ] All tests passing
- [ ] Sync validation report generated

---

## 🎓 AGENT INTERACTION EXAMPLES

### Example 1: Add New Skill

```
User: @cv-update Agrega React 19 y Next.js a 'Programación & Desarrollo'

Master Orchestrator:
  → Routes to: CV Update Specialist
  → CV Specialist: Updates cv-data.ts
  → Routes to: Document Sync Specialist
  → Sync Specialist: Regenerates DOCX + PDF
  → Routes to: Testing Specialist
  → Test Specialist: Runs all tests
  → Routes to: Deployment Specialist
  → Deploy Specialist: Commits + pushes
  → Master confirms: ✅ Complete
```

### Example 2: Update Portfolio Project

```
User: @portfolio Agrega nuevo proyecto: TaskFlow, GitHub: https://..., Tech: React, TS

Master Orchestrator:
  → CV Specialist: Updates projects-data.ts
  → Test Specialist: Generates E2E tests
  → Testing passes ✅
  → Deploy Specialist: Commits + pushes
  → Verification: Portfolio page updated ✅
```

### Example 3: Full CV Refresh

```
User: @cv-refresh Actualiza todo el CV con mis nuevas certificaciones

Master Orchestrator:
  → Coordinates multi-step process
  → CV Specialist: Updates all fields
  → Sync Specialist: Verifies all artifacts
  → Test Specialist: Validates everything
  → Deploy Specialist: Release version
  → Master: Generates comprehensive report
```

---

## 📚 IMPLEMENTATION ROADMAP

### Phase 1: Immediate (Week 1)
- ✅ Create master orchestrator agent
- ✅ Reorganize folder structure
- ✅ Document architecture
- ✅ Create agent definitions

### Phase 2: Enhancement (Week 2)
- 📦 Implement sync verification automation
- 📦 Add document generation agents
- 📦 Enhance testing automation
- 📦 Create integration tests

### Phase 3: Optimization (Week 3)
- 🎯 Performance monitoring
- 🎯 Visual regression testing
- 🎯 Bundle size analysis
- 🎯 Lighthouse integration

### Phase 4: Advanced (Week 4+)
- 🚀 Multi-language support (i18n)
- 🚀 Portfolio recommendations ML
- 🚀 Automated screenshot generation
- 🚀 AI-powered content suggestions

---

## ✅ SUMMARY

This modern AI-driven architecture provides:

1. **Scalability:** Clear separation of concerns, modular design
2. **Maintainability:** Well-organized folder structure, clear responsibilities
3. **Quality:** Comprehensive testing, multiple quality gates
4. **Automation:** Master orchestrator coordinating specialized agents
5. **Reliability:** Guaranteed sync verification, rollback capabilities
6. **Developer Experience:** Clear guidelines, comprehensive documentation

**Result:** Enterprise-grade portfolio management system with AI-powered automation and quality assurance.

---

**Created by:** AI Architecture Team  
**Version:** 2.0 (Professional)  
**Last Updated:** 2026-09-13
