# 🏛️ ARCHITECTURE RULES & PRINCIPLES

**Version:** 1.0  
**Framework:** Clean Architecture + Hexagonal Architecture + SOLID  
**Target:** Enterprise-Grade Monorepo  

---

## 🎯 CORE PRINCIPLES

### 1. **Separation of Concerns**
Each layer has ONE responsibility:
```
apps/web/     → Presentation & User Interaction
apps/api/     → Business Logic & Data Processing
packages/     → Reusable artifacts (types, components, configs)
testing/      → Quality assurance
```

### 2. **Dependency Inversion**
```
Backend:
  ❌ controllers.py → models.py (WRONG: tight coupling)
  ✅ api.py → domain interfaces ← services (RIGHT: abstractions)

Frontend:
  ❌ components import directly from /services
  ✅ components → custom hooks → api-client (RIGHT: layers)
```

### 3. **Single Responsibility Principle (SRP)**
```python
# ❌ WRONG: Multiple responsibilities
class UserService:
    def create_user(self): pass
    def generate_pdf(self): pass
    def send_email(self): pass

# ✅ RIGHT: One responsibility
class UserService:
    def create_user(self): pass

class PDFGenerator:
    def generate_pdf(self): pass

class EmailService:
    def send_email(self): pass
```

### 4. **Open/Closed Principle (OCP)**
```python
# ❌ WRONG: Modifying when adding new document type
class DocumentGenerator:
    if format == "docx":
        generate_docx()
    elif format == "pdf":
        generate_pdf()
    # Add new type? Modify this file!

# ✅ RIGHT: Extension without modification
class DocumentGenerator(ABC):
    @abstractmethod
    def generate(self): pass

class DocxGenerator(DocumentGenerator):
    def generate(self): pass

class PDFGenerator(DocumentGenerator):
    def generate(self): pass
```

### 5. **Liskov Substitution Principle (LSP)**
All implementations must be substitutable:
```python
generators: list[DocumentGenerator] = [
    DocxGenerator(),
    PDFGenerator(),
    ExcelGenerator()
]

for gen in generators:
    gen.generate()  # All work the same way
```

### 6. **Interface Segregation Principle (ISP)**
```python
# ❌ WRONG: Huge interface
class DocumentService:
    def generate_docx(self): pass
    def generate_pdf(self): pass
    def sync_verify(self): pass
    def validate_data(self): pass

# ✅ RIGHT: Segregated interfaces
class DocumentGenerator(ABC):
    def generate(self): pass

class SyncValidator(ABC):
    def validate(self): pass
```

---

## 📁 ARCHITECTURE LAYERS

### **Presentation Layer** (`apps/web/`)
**Responsibility:** User Interface & Interaction  
**Can depend on:** Components, Hooks, API Client  
**Cannot depend on:** Business logic, Direct service calls  

```typescript
apps/web/src/
├── components/        # Reusable UI components
│   ├── DocumentDownloader.tsx
│   ├── SyncStatus.tsx
│   └── index.ts
├── pages/             # Route handlers
│   ├── Home.tsx
│   └── Portfolio.tsx
├── hooks/             # Custom React hooks (logic extraction)
│   ├── useDocuments.ts
│   └── useSync.ts
├── services/          # API integration (calls api-client)
│   └── documentService.ts
└── types/             # Local types (UI state, props)
```

**Rules:**
- ✅ Import from `@mportafolio/api-client`
- ✅ Import from `@mportafolio/ui`
- ✅ Import from `./hooks`
- ✅ Import from `./services`
- ❌ Direct API calls (use services)
- ❌ Business logic in components
- ❌ Database/file operations

---

### **API Client Layer** (`packages/api-client/`)
**Responsibility:** Type-safe API contracts & HTTP communication  
**Can depend on:** Nothing (pure TS)  
**Cannot depend on:** React, Business logic  

```typescript
packages/api-client/src/
├── types/
│   ├── requests.ts       # Request DTOs
│   ├── responses.ts      # Response DTOs
│   └── index.ts          # Public types
├── client.ts             # HTTP client
└── index.ts              # Public API
```

**Rules:**
- ✅ Define Request/Response types
- ✅ Export HTTP client
- ✅ Document endpoints
- ❌ Business logic
- ❌ React code
- ❌ Database code

**Example:**
```typescript
// api-client/src/types/responses.ts
export interface GenerateDocumentResponse {
  status: 'success' | 'error';
  file_url?: string;
  message: string;
}

export interface SyncVerifyResponse {
  status: 'success' | 'warning' | 'error';
  sync_report: {
    total_certificates: number;
    matched_formats: string[];
    mismatches: string[];
  };
}
```

---

### **Business Logic Layer** (`apps/api/app/domain/`)
**Responsibility:** Business rules & entities  
**Can depend on:** Abstractions (interfaces)  
**Cannot depend on:** HTTP, Database implementations  

```python
apps/api/app/domain/
├── entities/          # Domain models
│   ├── cv_entity.py
│   └── certificate_entity.py
├── repositories/      # Abstract interfaces
│   ├── cv_repository.py
│   └── sync_repository.py
└── use_cases/         # Business workflows
    ├── generate_document.py
    └── verify_sync.py
```

**Rules:**
- ✅ Define domain entities (no Pydantic models here)
- ✅ Define repository interfaces (ABCs)
- ✅ Implement use cases
- ✅ Pure Python (no FastAPI)
- ❌ HTTP/REST logic
- ❌ Database queries
- ❌ FastAPI dependencies

**Example:**
```python
# apps/api/app/domain/use_cases/generate_document.py
from abc import ABC, abstractmethod

class DocumentGenerator(ABC):
    @abstractmethod
    def generate(self, cv_data: dict) -> bytes:
        pass

class DocxDocumentUseCase:
    def __init__(self, generator: DocumentGenerator):
        self.generator = generator
    
    def execute(self, cv_data: dict) -> bytes:
        return self.generator.generate(cv_data)
```

---

### **Application Layer** (`apps/api/app/api/`)
**Responsibility:** HTTP endpoints, request validation, dependency injection  
**Can depend on:** Domain layer, Services  
**Cannot depend on:** Direct business logic from services  

```python
apps/api/app/api/
├── routes/            # Endpoint groups
│   ├── documents.py   # /api/generate/*
│   └── sync.py        # /api/sync/*
├── middlewares/       # Auth, CORS, logging
│   └── auth.py
└── main.py           # FastAPI app setup
```

**Rules:**
- ✅ Define FastAPI routes
- ✅ Request validation (Pydantic)
- ✅ Call use cases from domain
- ✅ Return proper HTTP responses
- ❌ Business logic
- ❌ Direct service calls
- ❌ Database operations

**Example:**
```python
# apps/api/app/api/routes/documents.py
from fastapi import APIRouter
from ...domain.use_cases import DocxDocumentUseCase

router = APIRouter()

@router.post("/generate/docx")
async def generate_docx(cv_data: CVDataModel):
    use_case = DocxDocumentUseCase(DocxGenerator())
    file_bytes = use_case.execute(cv_data.dict())
    return FileResponse(file_bytes, filename="CV.docx")
```

---

### **Infrastructure Layer** (`apps/api/app/services/`)
**Responsibility:** Concrete implementations (DOCX, PDF, Excel, Validators)  
**Can depend on:** Domain interfaces  
**Cannot depend on:** Application layer  

```python
apps/api/app/services/
├── generators/        # Document implementations
│   ├── docx_generator.py
│   ├── pdf_generator.py
│   └── excel_generator.py
└── validators/        # Validation implementations
    └── sync_validator.py
```

**Rules:**
- ✅ Implement domain interfaces
- ✅ Handle technical details (python-docx, reportlab, etc)
- ✅ Pure implementations
- ❌ HTTP logic
- ❌ FastAPI dependency injection
- ❌ Multiple responsibilities

**Example:**
```python
# apps/api/app/services/generators/docx_generator.py
from ...domain.use_cases import DocumentGenerator

class DocxGenerator(DocumentGenerator):
    def generate(self, cv_data: dict) -> bytes:
        # Implementation using python-docx
        return docx_bytes
```

---

### **UI Component Library** (`packages/ui/`)
**Responsibility:** Reusable React components  
**Can depend on:** Nothing (or tailwind, shadcn/ui)  
**Cannot depend on:** Business logic, API calls  

```typescript
packages/ui/src/
├── components/
│   ├── Button.tsx
│   ├── Card.tsx
│   ├── DownloadButton.tsx
│   └── index.ts
└── types/
    └── props.ts
```

**Rules:**
- ✅ Pure presentational components
- ✅ Accept props for customization
- ✅ Emit events/callbacks
- ✅ Storybook documentation
- ❌ API calls
- ❌ useState for business logic
- ❌ Direct imports from apps

---

### **Configuration Package** (`packages/config/`)
**Responsibility:** Shared build & code quality configs  

```
packages/config/
├── eslint-config/
│   └── index.js
├── prettier-config/
│   └── index.js
├── tsconfig/
│   ├── base.json
│   ├── react.json
│   └── node.json
└── package.json
```

---

### **Testing Layer** (`testing/`)
**Responsibility:** Quality assurance  

```
testing/
├── e2e/               # Integration & E2E (Playwright)
│   ├── tests/
│   │   ├── documents.spec.ts
│   │   └── sync.spec.ts
│   └── playwright.config.ts
└── performance/       # Load testing
```

---

## 🔄 DATA FLOW

### ✅ CORRECT Flow
```
User Input (Web)
    ↓
UI Component
    ↓
Custom Hook (useDocuments)
    ↓
DocumentService (apps/web/services)
    ↓
API Client (@mportafolio/api-client)
    ↓
HTTP Request
    ↓
FastAPI Router (apps/api/api/routes)
    ↓
Request Validation (Pydantic)
    ↓
Use Case (apps/api/domain/use_cases)
    ↓
Generator/Service (apps/api/services)
    ↓
Response (HTTP 200 + file)
    ↓
Hook processes response
    ↓
UI updates
```

### ❌ WRONG Flow
```
Component
  ↓
Directly calls apps/api/services  ❌ WRONG: Breaks separation
  ↓ or
Component  
  ↓
Has business logic ❌ WRONG: Violates SRP
  ↓ or
Service imports component ❌ WRONG: Circular dependency
```

---

## 📋 DEPENDENCY RULES

### TypeScript/React Dependencies
```json
{
  "dependencies": {
    "@mportafolio/api-client": "workspace:*",
    "@mportafolio/ui": "workspace:*",
    "react": "19.x",
    "typescript": "7.x"
  }
}
```

### Python Dependencies
```toml
[project]
dependencies = [
    "fastapi>=0.104.0",
    "pydantic>=2.0.0",
    "python-docx>=0.8.11",
    "reportlab>=4.0.0",
    "openpyxl>=3.1.0"
]
```

### Circular Dependency Prevention
```
✅ ALLOWED:
  web → api-client
  api-client ← nothing
  backend → domain → services
  
❌ BLOCKED:
  web → backend
  services → api
  ui → web
  backend → frontend
```

---

## 🚦 CODE QUALITY GATES

### TypeScript Rules
```bash
npm run lint              # ESLint (No warnings allowed)
npm run type-check        # TypeScript (0 errors)
npm run format:check      # Prettier (Code style)
npm run test              # Vitest (100% pass)
npm run build             # Vite (Successful bundle)
```

### Python Rules
```bash
python -m flake8 .        # Code style (8 max)
python -m mypy .          # Type checking (0 errors)
python -m pytest .        # Tests (100% pass)
python -m black --check . # Code format
```

### General Rules
```
✅ Zero TypeScript errors
✅ Zero Python type errors
✅ All tests passing (65+ unit + 30+ E2E)
✅ No circular dependencies
✅ No direct service imports from UI
✅ All imports from correct layer
✅ Documentation complete
```

---

## 📐 IMPORT PATTERNS

### ✅ CORRECT Imports

**Frontend:**
```typescript
// ✅ Import from packages
import { CVDataClient } from '@mportafolio/api-client';
import { Button, Card } from '@mportafolio/ui';

// ✅ Import from hooks
import { useDocuments } from './hooks/useDocuments';

// ✅ Import from services
import { documentService } from './services/documentService';

// ✅ Import from types
import type { DocumentFormat } from '@mportafolio/api-client';
```

**Backend:**
```python
# ✅ API layer imports use cases
from app.domain.use_cases import DocxDocumentUseCase

# ✅ Use cases import repositories
from app.domain.repositories import DocumentGenerator

# ✅ Services implement interfaces
from app.domain.use_cases import DocumentGenerator
class DocxGenerator(DocumentGenerator):
    pass

# ✅ Config from app config
from app.config import get_settings
```

### ❌ WRONG Imports

**Frontend:**
```typescript
// ❌ Direct API calls (use api-client)
import axios from 'axios';
axios.post('/api/generate/docx');

// ❌ Import from backend
import { docxGenerator } from 'apps/backend';

// ❌ Direct service in component
const doc = documentService.generate();

// ❌ Business logic in component
const [certs, setCerts] = useState([]);
useEffect(() => {
    setCerts(data.certificates);
}, []);
```

**Backend:**
```python
# ❌ FastAPI in domain
from fastapi import APIRouter

# ❌ Multiple responsibilities
class UserService:
    def create_user(self): pass
    def generate_pdf(self): pass

# ❌ Direct database in service
result = db.query(User).all()
```

---

## 🎯 MIGRATION QUALITY CHECKLIST

Before considering migration complete:

### Structure ✅
- [ ] All directories created
- [ ] Files moved to correct locations
- [ ] No duplicate code
- [ ] All imports fixed

### Dependencies ✅
- [ ] No circular imports
- [ ] All workspaces configured
- [ ] package.json dependencies correct
- [ ] pyproject.toml configured

### Code Quality ✅
- [ ] TypeScript: 0 errors (`npm run lint`)
- [ ] Python: 0 errors (`python -m mypy`)
- [ ] All tests pass
- [ ] Build succeeds

### Documentation ✅
- [ ] README files updated
- [ ] Architecture clear
- [ ] Contributing guide created
- [ ] API documented

### CI/CD ✅
- [ ] GitHub Actions workflows created
- [ ] All checks pass
- [ ] Architecture enforced via linters
- [ ] Security scanning enabled

---

## 📚 REFERENCES

### Clean Architecture
- [Clean Code by Uncle Bob](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
- [Clean Architecture book](https://www.oreilly.com/library/view/clean-architecture-a/9780134494272/)

### Hexagonal Architecture
- [Hexagonal Architecture Pattern](https://alistair.cockburn.us/hexagonal-architecture/)
- [Ports and Adapters](https://en.wikipedia.org/wiki/Hexagonal_architecture)

### SOLID Principles
- [SOLID Principles (Wikipedia)](https://en.wikipedia.org/wiki/SOLID)
- [Python Design Patterns](https://refactoring.guru/design-patterns/python)

---

## 🚀 NEXT STEPS

1. ✅ Read this document completely
2. ✅ Understand the layer dependencies
3. ✅ Start migration following MIGRATION_PLAN.md
4. ✅ Use this as reference for refactoring
5. ✅ Enforce via linting & CI/CD

**Questions?** Refer to specific layer sections above.

---

```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║         🏛️  CLEAN ARCHITECTURE RULES ESTABLISHED  🏛️         ║
║                                                                ║
║    All code must follow these principles and patterns.         ║
║    Violations will be caught by linters & code review.         ║
║                                                                ║
║              "Architecture is not about tools,                 ║
║               it's about structure and principles"             ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

**Last Updated:** 2026-09-14  
**Maintained By:** Principal Architect  
**Enforced By:** ESLint, mypy, pytest, GitHub Actions  
