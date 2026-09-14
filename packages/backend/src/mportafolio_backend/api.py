"""FastAPI application for CV document generation"""

import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, File, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json

from .generators import DocxGenerator, PDFGenerator, ExcelGenerator
from .sync_validator import SyncValidator
from .models import CVDataModel, GeneratedDocumentModel, SyncReportModel

# Create FastAPI app
app = FastAPI(
    title="MiPortafolio Backend API",
    description="Generate DOCX, PDF, and Excel documents from CV data",
    version="2.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create output directory
OUTPUT_DIR = Path("/tmp/mportafolio_generated")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class CVDataRequest(BaseModel):
    """Request model for CV data"""
    data: Dict[str, Any]


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint"""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "service": "MiPortafolio Backend API"
    }


@app.post("/api/generate/docx")
async def generate_docx(request: CVDataRequest) -> FileResponse:
    """Generate DOCX document"""
    try:
        generator = DocxGenerator.from_dict(request.data)
        output_path = OUTPUT_DIR / f"CV_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        generator.generate(output_path)

        return FileResponse(
            output_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=output_path.name
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to generate DOCX: {str(e)}")


@app.post("/api/generate/pdf")
async def generate_pdf(request: CVDataRequest) -> FileResponse:
    """Generate PDF document"""
    try:
        generator = PDFGenerator.from_dict(request.data)
        output_path = OUTPUT_DIR / f"CV_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        generator.generate(output_path)

        return FileResponse(
            output_path,
            media_type="application/pdf",
            filename=output_path.name
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to generate PDF: {str(e)}")


@app.post("/api/generate/excel")
async def generate_excel(request: CVDataRequest) -> FileResponse:
    """Generate Excel workbook"""
    try:
        generator = ExcelGenerator.from_dict(request.data)
        output_path = OUTPUT_DIR / f"CV_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        generator.generate(output_path)

        return FileResponse(
            output_path,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=output_path.name
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to generate Excel: {str(e)}")


@app.post("/api/generate/all")
async def generate_all(request: CVDataRequest) -> Dict[str, str]:
    """Generate all documents (DOCX, PDF, Excel)"""
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results = {}

        # Generate DOCX
        docx_gen = DocxGenerator.from_dict(request.data)
        docx_path = OUTPUT_DIR / f"CV_{timestamp}.docx"
        docx_gen.generate(docx_path)
        results['docx'] = str(docx_path)

        # Generate PDF
        pdf_gen = PDFGenerator.from_dict(request.data)
        pdf_path = OUTPUT_DIR / f"CV_{timestamp}.pdf"
        pdf_gen.generate(pdf_path)
        results['pdf'] = str(pdf_path)

        # Generate Excel
        excel_gen = ExcelGenerator.from_dict(request.data)
        excel_path = OUTPUT_DIR / f"CV_{timestamp}.xlsx"
        excel_gen.generate(excel_path)
        results['excel'] = str(excel_path)

        return {
            "status": "success",
            "timestamp": timestamp,
            "files": results
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to generate documents: {str(e)}")


@app.post("/api/sync/verify")
async def verify_sync(request: CVDataRequest) -> SyncReportModel:
    """Verify synchronization of CV data"""
    try:
        report = SyncValidator.validate_dict(request.data)
        return report
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Sync verification failed: {str(e)}")


@app.get("/api/docs/openapi.json")
async def openapi() -> Dict[str, Any]:
    """OpenAPI schema"""
    return app.openapi()


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint"""
    return {
        "service": "MiPortafolio Backend API",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
