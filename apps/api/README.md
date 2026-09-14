# @mportafolio/backend

Python backend for generating CV documents (DOCX, PDF, Excel) and synchronization verification.

## 🎯 Features

- 📄 **DOCX Generation** - Professional ATS-optimized Word documents
- 📑 **PDF Generation** - Visually formatted PDF documents
- 📊 **Excel Generation** - Structured workbook with multiple sheets
- ✅ **Sync Validation** - Verify data consistency across all formats
- 🚀 **FastAPI** - Production-ready REST API
- 🧪 **Pytest** - Comprehensive test coverage

## 📦 Installation

```bash
cd packages/backend
pip install -e ".[dev]"
```

### Requirements

- Python 3.10+
- pip or conda

### Dependencies

- `fastapi` - Modern web framework
- `uvicorn` - ASGI server
- `python-docx` - DOCX generation
- `reportlab` - PDF generation
- `openpyxl` - Excel generation
- `pydantic` - Data validation

## 🚀 Quick Start

### Development Server

```bash
# From packages/backend
python -m uvicorn mportafolio_backend.api:app --reload
```

Server runs at: http://localhost:8000

API docs at: http://localhost:8000/docs

### Generate Documents

```python
from mportafolio_backend.generators import DocxGenerator, PDFGenerator, ExcelGenerator
import json

# Load CV data
with open('cv-data.json', 'r') as f:
    cv_data = json.load(f)

# Generate DOCX
docx_gen = DocxGenerator.from_dict(cv_data)
docx_gen.generate('output/CV.docx')

# Generate PDF
pdf_gen = PDFGenerator.from_dict(cv_data)
pdf_gen.generate('output/CV.pdf')

# Generate Excel
excel_gen = ExcelGenerator.from_dict(cv_data)
excel_gen.generate('output/CV.xlsx')
```

## 📡 API Endpoints

### Health Check
```
GET /health
```

### Generate DOCX
```
POST /api/generate/docx
Content-Type: application/json

{
  "data": { /* CV data object */ }
}
```

### Generate PDF
```
POST /api/generate/pdf
Content-Type: application/json

{
  "data": { /* CV data object */ }
}
```

### Generate Excel
```
POST /api/generate/excel
Content-Type: application/json

{
  "data": { /* CV data object */ }
}
```

### Generate All Documents
```
POST /api/generate/all
Content-Type: application/json

{
  "data": { /* CV data object */ }
}

Response:
{
  "status": "success",
  "timestamp": "20260913_120000",
  "files": {
    "docx": "/tmp/mportafolio_generated/CV_20260913_120000.docx",
    "pdf": "/tmp/mportafolio_generated/CV_20260913_120000.pdf",
    "excel": "/tmp/mportafolio_generated/CV_20260913_120000.xlsx"
  }
}
```

### Verify Synchronization
```
POST /api/sync/verify
Content-Type: application/json

{
  "data": { /* CV data object */ }
}

Response:
{
  "timestamp": "2026-09-13T12:00:00.123456",
  "status": "success",
  "web_data_present": true,
  "docx_data_present": true,
  "pdf_data_present": true,
  "excel_data_present": true,
  "all_in_sync": true,
  "mismatches": [],
  "message": "✅ All data in sync!"
}
```

## 📁 Project Structure

```
packages/backend/
├── pyproject.toml                 ← Project configuration
├── README.md                      ← This file
│
└── src/mportafolio_backend/
    ├── __init__.py
    ├── api.py                     ← FastAPI application
    ├── models.py                  ← Pydantic models
    ├── sync_validator.py          ← Sync verification
    │
    └── generators/
        ├── __init__.py
        ├── docx_generator.py      ← DOCX generation
        ├── pdf_generator.py       ← PDF generation
        └── excel_generator.py     ← Excel generation
```

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=mportafolio_backend

# Run specific test
pytest tests/test_generators.py::test_docx_generation
```

## 🔧 Configuration

### Environment Variables

```bash
# API configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true

# Output directory
OUTPUT_DIR=/tmp/mportafolio_generated
```

## 📊 Data Models

### CVDataModel

```python
{
  "profile": {
    "name": "Andrés Rodríguez Pisa",
    "title": "SDET Senior",
    "email": "email@example.com",
    "phone": "(+57) 320 324 5988",
    "location": "Bogotá, Colombia",
    "bio": "Professional summary...",
    "github": "https://github.com/...",
    "linkedin": "https://linkedin.com/...",
    "portfolio": "https://portfolio.com"
  },
  "skills": [
    {
      "category": "Web Automation",
      "skills": [
        {"name": "Selenium", "level": "expert"},
        {"name": "Playwright", "level": "expert"}
      ]
    }
  ],
  "experience": [...],
  "education": [...],
  "certificates": {...},
  "languages": [...]
}
```

## 🚀 Production Deployment

### Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install -e .

COPY src ./src

CMD ["uvicorn", "mportafolio_backend.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Running in Docker

```bash
docker build -t mportafolio-backend .
docker run -p 8000:8000 mportafolio-backend
```

## 📝 Scripts

### Generate CV Documents

```bash
python -c "
from mportafolio_backend.generators import DocxGenerator, PDFGenerator, ExcelGenerator
import json

with open('../core/src/data/cv-data.json') as f:
    data = json.load(f)

DocxGenerator.from_dict(data).generate('output/CV.docx')
PDFGenerator.from_dict(data).generate('output/CV.pdf')
ExcelGenerator.from_dict(data).generate('output/CV.xlsx')
"
```

## 🔗 Integration

### Import from @mportafolio/core

The backend reads CV data from the core package:

```python
# Load from cv-data.ts exported as JSON
import json
with open('../../packages/core/src/data/cv-data.json') as f:
    cv_data = json.load(f)

# Use with generators
from mportafolio_backend.generators import DocxGenerator
gen = DocxGenerator.from_dict(cv_data)
gen.generate('CV.docx')
```

## 📞 Support

For issues or questions, refer to:
- [ARCHITECTURE.md](../../.agent/ARCHITECTURE.md)
- [Backend Implementation Guide](../../docs/BACKEND_IMPLEMENTATION.md)

## 📄 License

ISC

---

**Version:** 2.0.0  
**Status:** ✅ Production Ready  
**Python:** 3.10+  
**Framework:** FastAPI
