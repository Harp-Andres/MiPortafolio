# 🔄 PYTHON BACKEND REFACTORIZATION GUIDE

**Status:** Backend files copied to apps/api. Manual refactorization needed for layer separation.  
**Location:** `e:\UnidadPrincipal\Documentos\Repos\MiPortafolio\apps\api\`  

---

## 📋 REFACTORIZATION CHECKLIST

### Phase 1: Move Files to Layer Directories

Source: `apps/api/src/mportafolio_backend/`  
Target: `apps/api/app/` (organized by layer)

#### Step 1.1: Domain Layer (Entities & Interfaces)
```python
# MOVE: models.py → app/domain/entities/cv_models.py
# Keep ALL classes:
#   - SkillModel
#   - SkillCategoryModel
#   - ExperienceModel
#   - EducationModel
#   - CertificateModel
#   - ProfileModel
#   - CVDataModel
#   - SyncReportModel

# This is the DOMAIN LAYER - pure business models
# No dependencies on FastAPI, HTTP, or specific implementations
```

#### Step 1.2: Infrastructure Layer - Services (Generators)
```python
# MOVE: generators/*.py → app/services/generators/
# Files:
#   - docx_generator.py
#   - pdf_generator.py
#   - excel_generator.py
#
# These are CONCRETE IMPLEMENTATIONS of document generation
# Dependencies on python-docx, reportlab, openpyxl are OK here
```

#### Step 1.3: Infrastructure Layer - Validators
```python
# MOVE: sync_validator.py → app/services/validators/sync_validator.py
#
# This is a CONCRETE IMPLEMENTATION of validation
# Should depend on domain models but not on HTTP
```

#### Step 1.4: Configuration Layer
```python
# MOVE: config.py → app/config/settings.py
#
# Configuration management
# Loading from .env, environment variables, etc
```

#### Step 1.5: HTTP API Layer
```python
# MOVE: api.py → app/api/main.py
#
# FastAPI application setup
# After moving, REFACTOR:
#   - Keep routes and endpoint definitions
#   - Change imports to use new layer paths
#   - Implement dependency injection
```

---

### Phase 2: Create Abstraction Interfaces (Domain)

Create abstract base classes in `app/domain/` to define contracts:

```python
# app/domain/use_cases/document_generator.py
from abc import ABC, abstractmethod

class DocumentGenerator(ABC):
    @abstractmethod
    def generate(self, cv_data: dict) -> bytes:
        """Generate document and return bytes"""
        pass
```

```python
# app/domain/use_cases/sync_validator.py  
from abc import ABC, abstractmethod

class SyncValidator(ABC):
    @abstractmethod
    def validate(self, cv_data: dict) -> dict:
        """Validate data and return report"""
        pass
```

---

### Phase 3: Create Use Cases Layer (Domain)

```python
# app/domain/use_cases/generate_docx_use_case.py
from .document_generator import DocumentGenerator

class GenerateDocxUseCase:
    def __init__(self, generator: DocumentGenerator):
        self.generator = generator
    
    def execute(self, cv_data: dict) -> bytes:
        return self.generator.generate(cv_data)
```

---

### Phase 4: Create Dependency Injection Layer

```python
# app/dependencies.py
from app.services.generators.docx_generator import DocxGenerator
from app.services.generators.pdf_generator import PDFGenerator
from app.services.generators.excel_generator import ExcelGenerator
from app.services.validators.sync_validator import SyncValidator
from app.domain.use_cases.document_generator import DocumentGenerator

def get_docx_generator() -> DocumentGenerator:
    return DocxGenerator()

def get_pdf_generator() -> DocumentGenerator:
    return PDFGenerator()

def get_excel_generator() -> DocumentGenerator:
    return ExcelGenerator()

def get_sync_validator() -> SyncValidator:
    return SyncValidator()
```

---

### Phase 5: Update API Routes

Refactor `app/api/main.py` to use dependency injection:

```python
# BEFORE (Current - wrong)
from mportafolio_backend.generators import DocxGenerator
gen = DocxGenerator()

# AFTER (Correct - using DI)
from fastapi import Depends
from app.dependencies import get_docx_generator

@router.post("/generate/docx")
async def generate_docx(
    cv_data: CVDataModel,
    generator = Depends(get_docx_generator)
):
    file_bytes = generator.generate(cv_data.dict())
    return FileResponse(file_bytes, filename="CV.docx")
```

---

### Phase 6: Update Import Paths

**After moving files, update all imports:**

```python
# OLD import paths (WRONG)
from mportafolio_backend.models import CVDataModel
from mportafolio_backend.generators import DocxGenerator
from mportafolio_backend.sync_validator import SyncValidator

# NEW import paths (CORRECT - by layer)
from app.domain.entities.cv_models import CVDataModel
from app.services.generators.docx_generator import DocxGenerator  
from app.services.validators.sync_validator import SyncValidator
```

---

### Phase 7: Tests Organization

```
apps/api/tests/
├── unit/
│   ├── domain/          # Domain logic tests
│   ├── services/        # Service tests
│   └── api/             # Route tests
└── conftest.py          # Shared fixtures
```

---

## 🎯 ORDER OF EXECUTION

1. **First:** Create interfaces in `app/domain/use_cases/` (abstract classes)
2. **Second:** Move/copy concrete implementations to `app/services/`
3. **Third:** Move domain models to `app/domain/entities/`
4. **Fourth:** Create `app/dependencies.py` with DI setup
5. **Fifth:** Update `app/api/main.py` to use DI
6. **Sixth:** Update all import paths throughout codebase
7. **Seventh:** Run tests: `pytest tests/ -v`
8. **Eighth:** Verify: `python -m mypy app/` (0 errors)

---

## ⚡ QUICK REFERENCE

### File Locations After Refactor

```
apps/api/app/
├── __init__.py
├── config/
│   └── settings.py              (from config.py)
├── domain/
│   ├── entities/
│   │   └── cv_models.py          (from models.py)
│   ├── repositories/             (interfaces)
│   └── use_cases/                (business workflows)
│       ├── document_generator.py (ABC interface)
│       └── sync_validator.py     (ABC interface)
├── services/
│   ├── generators/
│   │   ├── docx_generator.py     (from generators/docx_generator.py)
│   │   ├── pdf_generator.py      (from generators/pdf_generator.py)
│   │   └── excel_generator.py    (from generators/excel_generator.py)
│   └── validators/
│       └── sync_validator.py     (from sync_validator.py)
├── api/
│   └── main.py                   (from api.py - REFACTORED)
├── dependencies.py               (NEW - Dependency Injection)
└── tests/
    ├── unit/
    │   ├── domain/
    │   ├── services/
    │   └── api/
    └── conftest.py
```

---

## ✅ VALIDATION AFTER REFACTOR

```bash
# Type checking
python -m mypy apps/api/ --strict

# Run tests
pytest apps/api/tests/ -v --cov=apps/api

# Lint
python -m pylint apps/api/

# Build/import check
python -c "from app.api.main import app; print('✓ Import successful')"
```

---

## 🔗 REFERENCES

- [Clean Architecture (Uncle Bob)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Dependency Injection in Python](https://en.wikipedia.org/wiki/Dependency_injection)
- [FastAPI Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/)

---

**Status:** READY FOR MANUAL EXECUTION  
**Next:** Proceed to create API Client TypeScript & React Components  
**Complexity:** Moderate - Systematic refactoring with clear structure
