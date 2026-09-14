# Backend Implementation Guide

## Overview

The MiPortafolio Backend is a Python-based service responsible for generating professional CV documents (DOCX, PDF, Excel) from a centralized CV data source and validating data synchronization across all platforms.

## Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Application                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         REST API Routes (/api/generate/*, etc)       │   │
│  └──────────────────────────────────────────────────────┘   │
│            ↓           ↓           ↓           ↓             │
│  ┌──────────────┐ ┌─────────┐ ┌──────────┐ ┌──────────┐    │
│  │DocxGenerator │ │PdfGen   │ │ExcelGen  │ │SyncValid │    │
│  └──────────────┘ └─────────┘ └──────────┘ └──────────┘    │
│            ↓           ↓           ↓           ↓             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │      CVDataModel (Pydantic Validation)              │   │
│  └─────────────────────────────────────────────────────┘   │
│            ↓                                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Input: cv-data.ts from @mportafolio/core           │   │
│  │  (JSON representation of TypeScript data)           │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Core Components

#### 1. **Models** (`models.py`)
Pydantic BaseModels that define and validate CV data structure:
- `ProfileModel` - Personal profile information
- `SkillModel` - Individual skill entry
- `SkillCategoryModel` - Group of skills by category
- `ExperienceModel` - Job experience entry
- `EducationModel` - Education entry
- `CertificateModel` - Certification entry
- `ProjectModel` - Portfolio project
- `CVDataModel` - Root model combining all CV components
- `SyncReportModel` - Synchronization validation report

#### 2. **Generators** (in `generators/` folder)

**DocxGenerator** (`docx_generator.py`)
- Uses `python-docx` library
- Generates professional ATS-optimized Word documents
- Methods:
  - `generate_header()` - Profile + contact information
  - `generate_profile()` - Professional summary
  - `generate_skills()` - Technical skills by category
  - `generate_experience()` - Work experience with achievements
  - `generate_education()` - Education entries
  - `generate_certificates()` - Certifications by category
  - `generate()` - Orchestrator method

**PDFGenerator** (`pdf_generator.py`)
- Uses `reportlab` library
- Generates visually formatted PDF documents
- Features:
  - Custom color scheme (primary: #1a1a1a, secondary: #0066cc)
  - Professional typography with different font styles
  - Structured sections with headers and subheaders
  - Proper spacing and alignment

**ExcelGenerator** (`excel_generator.py`)
- Uses `openpyxl` library
- Generates structured multi-sheet workbooks:
  - Sheet 1: Profile (personal info, summary)
  - Sheet 2: Skills (by category)
  - Sheet 3: Experience (job entries)
  - Sheet 4: Education (degrees)
  - Sheet 5: Certificates (by category)
- Features:
  - Styled headers with colors and fonts
  - Wrapped text for readability
  - Appropriate column widths
  - Border styling

#### 3. **Sync Validator** (`sync_validator.py`)
Validates that CV data is complete and consistent:
- `_validate_profile()` - Checks required profile fields
- `_validate_skills()` - Checks skills structure
- `_validate_experience()` - Checks experience data
- `_validate_education()` - Checks education data
- `_validate_certificates()` - Checks certificates structure
- `_count_data()` - Counts data elements for reporting
- `validate()` - Complete validation returning `SyncReportModel`

Status levels:
- `success` - All validations passed
- `warning` - Validations passed with warnings
- `error` - Validation failures found

#### 4. **FastAPI Application** (`api.py`)

**Endpoints:**

1. **GET /health**
   - Health check endpoint
   - Response: `{"status": "ok", "timestamp": "...", "service": "..."}`

2. **POST /api/generate/docx**
   - Generate DOCX document
   - Input: `CVDataRequest` with CV data
   - Output: DOCX file download

3. **POST /api/generate/pdf**
   - Generate PDF document
   - Input: `CVDataRequest` with CV data
   - Output: PDF file download

4. **POST /api/generate/excel**
   - Generate Excel workbook
   - Input: `CVDataRequest` with CV data
   - Output: Excel file download

5. **POST /api/generate/all**
   - Generate all documents at once
   - Input: `CVDataRequest` with CV data
   - Output: JSON with file paths

6. **POST /api/sync/verify**
   - Verify data synchronization
   - Input: `CVDataRequest` with CV data
   - Output: `SyncReportModel`

7. **GET /**
   - Root endpoint with service information

### Data Flow

```
TypeScript cv-data.ts
    ↓
Export as JSON
    ↓
HTTP Request to Backend API
    ↓
Pydantic Validation (CVDataModel)
    ↓
Generator Selection
    ├→ DocxGenerator
    ├→ PDFGenerator
    └→ ExcelGenerator
    ↓
Document Generation
    ↓
File Saved to OUTPUT_DIR
    ↓
File Returned to Client
```

## Configuration

### Environment Variables

```bash
# API Configuration
API_HOST=0.0.0.0              # Bind host
API_PORT=8000                 # Bind port
API_RELOAD=false              # Auto-reload on file changes (dev only)

# Output Directory
OUTPUT_DIR=/tmp/mportafolio_generated

# Logging
LOGGING_LEVEL=INFO
```

### Project Settings

Configured in `config.py`:
- Document MIME types
- Output directory
- API defaults
- Color schemes for PDF

## Installation & Setup

### Requirements
- Python 3.10+
- pip or conda

### Installation Steps

```bash
# Navigate to backend directory
cd packages/backend

# Install with development dependencies
pip install -e ".[dev]"

# Verify installation
python -c "import mportafolio_backend; print('✅ Backend installed')"
```

### Verify Dependencies

```bash
pip list | grep -E 'fastapi|python-docx|reportlab|openpyxl|pydantic'
```

## Running the Backend

### Development Server

```bash
# From packages/backend
python -m uvicorn mportafolio_backend.api:app --reload --host 0.0.0.0 --port 8000
```

Or use the convenience script:

```bash
python run.py
```

Server will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

### Production Deployment

```bash
# Using gunicorn (more stable)
pip install gunicorn
gunicorn mportafolio_backend.api:app --workers 4 --worker-class uvicorn.workers.UvicornWorker

# Or Docker
docker build -t mportafolio-backend .
docker run -p 8000:8000 mportafolio-backend
```

## Testing

### Unit Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_generators.py::TestDocxGenerator::test_generate_creates_file -v

# Run with coverage
pytest tests/ --cov=mportafolio_backend --cov-report=term-missing
```

### Using Test Script

```bash
python run_tests.py              # Run tests
python run_tests.py --coverage   # Run tests with coverage report
```

### Test Coverage

Current test suite includes:
- `TestDocxGenerator` - DOCX generation tests
- `TestPDFGenerator` - PDF generation tests
- `TestExcelGenerator` - Excel generation tests
- `TestSyncValidator` - Data validation tests
- `TestIntegration` - Integration tests for all generators

## Code Quality

### Formatting

```bash
# Format with Black
black src/ tests/

# Sort imports
isort src/ tests/

# Lint with Flake8
flake8 src/ tests/
```

### Type Checking

```bash
# Run mypy
mypy src/mportafolio_backend
```

## Integration with Frontend

### Getting CV Data from TypeScript

The backend expects CV data in the following format:

```python
import json
from mportafolio_backend.generators import DocxGenerator

# Option 1: Load from JSON file
with open('../core/src/data/cv-data.json') as f:
    cv_data = json.load(f)

# Option 2: Receive from HTTP request
# POST /api/generate/docx with body: {"data": {...}}

# Generate document
generator = DocxGenerator.from_dict(cv_data)
generator.generate('output/CV.docx')
```

### Frontend API Integration

```typescript
// Frontend code calling backend
const generateCV = async (format: 'docx' | 'pdf' | 'excel') => {
  const response = await fetch(`http://localhost:8000/api/generate/${format}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ data: CV_DATA })
  });
  
  const blob = await response.blob();
  // Download blob as file
};
```

## Troubleshooting

### Common Issues

1. **Import Error: "No module named 'mportafolio_backend'"**
   - Solution: Install package in editable mode: `pip install -e .`

2. **ModuleNotFoundError: "No module named 'python_docx'"`
   - Solution: Install dependencies: `pip install -e ".[dev]"`

3. **Port 8000 Already in Use**
   - Solution: Use different port: `API_PORT=8001 python run.py`

4. **Permission Denied on OUTPUT_DIR**
   - Solution: Create directory with write permissions: `mkdir -p /tmp/mportafolio_generated && chmod 755 /tmp/mportafolio_generated`

### Debug Mode

```bash
# Enable verbose logging
LOGGING_LEVEL=DEBUG python run.py

# Test API manually
curl -X POST http://localhost:8000/api/sync/verify \
  -H "Content-Type: application/json" \
  -d '{"data": {...}}'
```

## Performance Considerations

### Document Generation Times
- DOCX: ~100-200ms (python-docx is fast)
- PDF: ~300-500ms (reportlab rendering)
- Excel: ~150-250ms (openpyxl is fast)

### Memory Usage
- Per-request memory: ~5-15MB
- Total process: ~50-100MB (with dependencies)

### Optimization Tips
- Use connection pooling for API clients
- Cache CV data when possible
- Use async endpoints for bulk generation
- Consider background job queue for many requests

## Deployment Checklist

- [ ] Install dependencies: `pip install -e .`
- [ ] Run tests: `pytest tests/`
- [ ] Check type hints: `mypy src/`
- [ ] Format code: `black src/`
- [ ] Set environment variables
- [ ] Create OUTPUT_DIR with proper permissions
- [ ] Start server: `python run.py`
- [ ] Verify health: `curl http://localhost:8000/health`
- [ ] Test endpoint: `curl -X POST http://localhost:8000/api/sync/verify`

## Future Enhancements

1. **Caching**
   - Cache generated documents
   - Redis integration for distributed caching

2. **Database**
   - Store generation history
   - Track user preferences

3. **Advanced Features**
   - Multiple CV templates
   - Customizable styling
   - Batch generation
   - Webhook notifications

4. **Performance**
   - Async/await improvements
   - Streaming large files
   - CDN integration

5. **Monitoring**
   - Prometheus metrics
   - Structured logging
   - Error tracking (Sentry)

---

**Version:** 2.0.0  
**Last Updated:** 2026-09-13  
**Status:** Production Ready ✅
