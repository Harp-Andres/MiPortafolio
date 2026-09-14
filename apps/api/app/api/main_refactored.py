"""FastAPI application for CV document generation with hexagonal architecture

This module implements the HTTP/REST API layer of the application,
using dependency injection to interact with domain services.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.dependencies import (
    create_docx_generator,
    create_pdf_generator,
    create_excel_generator,
    create_sync_validator,
)
from app.domain.entities.cv_models import (
    CVDataModel,
    GeneratedDocumentModel,
    SyncReportModel,
)

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
        "service": "MiPortafolio Backend API",
        "version": "2.0.0"
    }


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint"""
    return {
        "service": "MiPortafolio Backend API",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.post("/api/generate/docx")
async def generate_docx(request: CVDataRequest) -> FileResponse:
    """
    Generate DOCX document from CV data.
    
    Args:
        request: CVDataRequest containing CV data dictionary
        
    Returns:
        FileResponse: Generated DOCX file
        
    Raises:
        HTTPException: If generation fails
    """
    try:
        # Use dependency injection to create generator
        generator = create_docx_generator(request.data)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = OUTPUT_DIR / f"CV_{timestamp}.docx"
        
        # Generate document
        generator.generate(output_path)

        return FileResponse(
            output_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=f"CV_{timestamp}.docx"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid CV data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate DOCX: {str(e)}")


@app.post("/api/generate/pdf")
async def generate_pdf(request: CVDataRequest) -> FileResponse:
    """
    Generate PDF document from CV data.
    
    Args:
        request: CVDataRequest containing CV data dictionary
        
    Returns:
        FileResponse: Generated PDF file
        
    Raises:
        HTTPException: If generation fails
    """
    try:
        # Use dependency injection to create generator
        generator = create_pdf_generator(request.data)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = OUTPUT_DIR / f"CV_{timestamp}.pdf"
        
        # Generate document
        generator.generate(output_path)

        return FileResponse(
            output_path,
            media_type="application/pdf",
            filename=f"CV_{timestamp}.pdf"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid CV data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")


@app.post("/api/generate/excel")
async def generate_excel(request: CVDataRequest) -> FileResponse:
    """
    Generate Excel workbook from CV data.
    
    Args:
        request: CVDataRequest containing CV data dictionary
        
    Returns:
        FileResponse: Generated Excel file
        
    Raises:
        HTTPException: If generation fails
    """
    try:
        # Use dependency injection to create generator
        generator = create_excel_generator(request.data)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = OUTPUT_DIR / f"CV_{timestamp}.xlsx"
        
        # Generate document
        generator.generate(output_path)

        return FileResponse(
            output_path,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=f"CV_{timestamp}.xlsx"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid CV data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate Excel: {str(e)}")


@app.post("/api/generate/all")
async def generate_all(request: CVDataRequest) -> Dict[str, Any]:
    """
    Generate all documents (DOCX, PDF, Excel) in one request.
    
    Args:
        request: CVDataRequest containing CV data dictionary
        
    Returns:
        Dictionary with status and file paths
        
    Raises:
        HTTPException: If any generation fails
    """
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results = {}

        # Generate DOCX
        docx_gen = create_docx_generator(request.data)
        docx_path = OUTPUT_DIR / f"CV_{timestamp}.docx"
        docx_gen.generate(docx_path)
        results['docx'] = str(docx_path)

        # Generate PDF
        pdf_gen = create_pdf_generator(request.data)
        pdf_path = OUTPUT_DIR / f"CV_{timestamp}.pdf"
        pdf_gen.generate(pdf_path)
        results['pdf'] = str(pdf_path)

        # Generate Excel
        excel_gen = create_excel_generator(request.data)
        excel_path = OUTPUT_DIR / f"CV_{timestamp}.xlsx"
        excel_gen.generate(excel_path)
        results['excel'] = str(excel_path)

        return {
            "status": "success",
            "timestamp": timestamp,
            "files": results
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid CV data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate documents: {str(e)}")


@app.post("/api/sync/verify")
async def verify_sync(request: CVDataRequest) -> SyncReportModel:
    """
    Verify synchronization of CV data across all formats.
    
    Args:
        request: CVDataRequest containing CV data dictionary
        
    Returns:
        SyncReportModel: Validation report
        
    Raises:
        HTTPException: If verification fails
    """
    try:
        # Use dependency injection to create validator
        validator = create_sync_validator(request.data)
        
        # Run validation
        report = validator.validate(request.data)
        return report
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid CV data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sync verification failed: {str(e)}")


@app.get("/api/docs/openapi.json")
async def openapi() -> Dict[str, Any]:
    """OpenAPI schema"""
    return app.openapi()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
