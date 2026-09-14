"""Dependency injection setup for the application

This module provides factory functions for creating instances of services
that implement domain interfaces. Used by FastAPI for dependency injection.
"""

from typing import Dict, Any
from functools import lru_cache

from app.domain.use_cases.document_generator import DocumentGenerator
from app.domain.use_cases.sync_validator import SyncValidator

from app.services.generators.docx_generator import DocxGenerator as DocxGeneratorImpl
from app.services.generators.pdf_generator import PDFGenerator as PDFGeneratorImpl
from app.services.generators.excel_generator import ExcelGenerator as ExcelGeneratorImpl
from app.services.validators.sync_validator_impl import SyncValidator as SyncValidatorImpl
from app.domain.entities.cv_models import CVDataModel


@lru_cache(maxsize=1)
def get_docx_generator() -> DocumentGenerator:
    """
    Factory function to get DOCX document generator instance.
    
    Returns:
        DocumentGenerator: DOCX generator implementing DocumentGenerator interface
    """
    return DocxGeneratorImpl


@lru_cache(maxsize=1)
def get_pdf_generator() -> DocumentGenerator:
    """
    Factory function to get PDF document generator instance.
    
    Returns:
        DocumentGenerator: PDF generator implementing DocumentGenerator interface
    """
    return PDFGeneratorImpl


@lru_cache(maxsize=1)
def get_excel_generator() -> DocumentGenerator:
    """
    Factory function to get Excel document generator instance.
    
    Returns:
        DocumentGenerator: Excel generator implementing DocumentGenerator interface
    """
    return ExcelGeneratorImpl


@lru_cache(maxsize=1)
def get_sync_validator() -> SyncValidator:
    """
    Factory function to get sync validator instance.
    
    Returns:
        SyncValidator: Validator implementing SyncValidator interface
    """
    # Return a callable that creates instances when called with CV data
    return SyncValidatorImpl


def create_docx_generator(cv_data: Dict[str, Any]) -> DocxGeneratorImpl:
    """
    Create a DOCX generator instance with CV data.
    
    Args:
        cv_data: Dictionary with CV data
        
    Returns:
        DocxGeneratorImpl: Configured generator instance
    """
    cv_model = CVDataModel(**cv_data)
    return DocxGeneratorImpl(cv_model)


def create_pdf_generator(cv_data: Dict[str, Any]) -> PDFGeneratorImpl:
    """
    Create a PDF generator instance with CV data.
    
    Args:
        cv_data: Dictionary with CV data
        
    Returns:
        PDFGeneratorImpl: Configured generator instance
    """
    cv_model = CVDataModel(**cv_data)
    return PDFGeneratorImpl(cv_model)


def create_excel_generator(cv_data: Dict[str, Any]) -> ExcelGeneratorImpl:
    """
    Create an Excel generator instance with CV data.
    
    Args:
        cv_data: Dictionary with CV data
        
    Returns:
        ExcelGeneratorImpl: Configured generator instance
    """
    cv_model = CVDataModel(**cv_data)
    return ExcelGeneratorImpl(cv_model)


def create_sync_validator(cv_data: Dict[str, Any] = None) -> SyncValidatorImpl:
    """
    Create a sync validator instance.
    
    Args:
        cv_data: Optional dictionary with CV data
        
    Returns:
        SyncValidatorImpl: Configured validator instance
    """
    if cv_data is None:
        cv_data = {}
    
    try:
        cv_model = CVDataModel(**cv_data)
    except Exception:
        # If data is invalid, create with empty model for validation
        cv_model = CVDataModel(
            profile={
                "name": "",
                "title": "",
                "email": "",
                "location": "",
                "bio": "",
                "github": "",
                "linkedin": "",
                "portfolio": ""
            },
            skills=[],
            experience=[],
            education=[],
            certificates={}
        )
    
    return SyncValidatorImpl(cv_model)
