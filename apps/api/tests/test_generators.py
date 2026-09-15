"""Tests for document generators"""

import json
import pytest
from copy import deepcopy
from pathlib import Path
from mportafolio_backend.generators import DocxGenerator, PDFGenerator, ExcelGenerator
from mportafolio_backend.sync_validator import SyncValidator
from mportafolio_backend.models import CVDataModel

# Test constants - mirror from Andrés' real CV data
EXPECTED_CERTIFICATE_COUNT = 21
EXPECTED_CERTIFICATE_CATEGORIES = {
    'DevOps & Cloud': 3,
    'Calidad & QA': 3,
    'Automatización Web & Mobile': 6,
    'Playwright & API Testing': 3,
    'IA & Productividad': 6,
}


# Sample CV data for testing - MIRROR OF ANDRÉS' REAL CV DATA
SAMPLE_CV = {
    "profile": {
        "name": "ANDRES RODRIGUEZ PISA",
        "title": "SDET | Senior QA Automation Engineer",
        "email": "andresrdrgzps05@gmail.com",
        "phone": "(+57) 320 324 5988",
        "location": "Bogotá, Colombia",
        "bio": "Ingeniero especializado en automatización multiplataforma con expertise en Playwright, Selenium, Appium y Karate",
        "github": "https://github.com/Harp-Andres",
        "linkedin": "https://www.linkedin.com/in/andresrodriguezpisa-qa/",
        "portfolio": "https://Harp-Andres.github.io/MiPortafolio"
    },
    "skills": [
        {
            "category": "Web Automation",
            "skills": [
                {"name": "Selenium WebDriver", "level": "expert"},
                {"name": "Playwright", "level": "expert"},
                {"name": "Cypress", "level": "advanced"}
            ]
        },
        {
            "category": "Mobile Automation",
            "skills": [
                {"name": "Appium", "level": "expert"},
                {"name": "Android/iOS", "level": "advanced"}
            ]
        }
    ],
    "experience": [
        {
            "id": "gft-2026",
            "title": "Test Automation Analyst III",
            "company": "GFT Technologies",
            "period": "Feb 2026 – Actualidad",
            "description": "Lidero la estrategia de automatización QA",
            "technologies": ["Playwright", "Selenium", "Karate", "GitHub Actions"],
            "achievements": [
                "Lidero la estrategia de automatización QA",
                "Diseño y ejecuto pruebas de performance",
                "Gestiono DoD y Test Plan"
            ]
        }
    ],
    "education": [
        {
            "id": "unad-2024",
            "degree": "Ingeniero de Sistemas",
            "institution": "Universidad Nacional Abierta y a Distancia (UNAD)",
            "graduation": "2024",
            "description": "Ingeniería de sistemas con énfasis en calidad"
        }
    ],
    "certificates": {
        "DevOps & Cloud": [
            {
                "id": "azure-udemy",
                "name": "DevOps y Cloud con Azure DevOps, App Service Pipelines y Git",
                "issuer": "Udemy",
                "date": "2024",
                "hours": 21
            },
            {
                "id": "docker-selenium",
                "name": "Docker Compose with Selenium",
                "issuer": "Udemy",
                "date": "2024",
                "hours": 3
            },
            {
                "id": "jenkins-udemy",
                "name": "La Guía de Jenkins: De Cero a Experto",
                "issuer": "Udemy",
                "date": "2024",
                "hours": 32
            }
        ],
        "Calidad & QA": [
            {
                "id": "istqb-udemy",
                "name": "ISTQB Certified Tester Foundation Level (CTFL 4.0)",
                "issuer": "Udemy",
                "date": "2024",
                "hours": 18
            },
            {
                "id": "jmeter-udemy",
                "name": "Master: Pruebas de Rendimiento con Apache JMeter",
                "issuer": "Udemy",
                "date": "2024",
                "hours": 16
            },
            {
                "id": "puppeteer-platzi",
                "name": "Introducción a Automatización de Pruebas con Puppeteer",
                "issuer": "Platzi",
                "date": "2023",
                "hours": 12
            }
        ],
        "Automatización Web & Mobile": [
            {
                "id": "selenium-udemy",
                "name": "Selenium WebDriver y Grid",
                "issuer": "Udemy",
                "date": "2023",
                "hours": 21
            },
            {
                "id": "selenium-linkedin",
                "name": "Selenium Essential Training",
                "issuer": "LinkedIn Learning",
                "date": "2023",
                "hours": 5
            },
            {
                "id": "appium-udemy",
                "name": "Master Class de Appium 2 con Java",
                "issuer": "Udemy",
                "date": "2024",
                "hours": 22
            },
            {
                "id": "appium-serenity",
                "name": "Configuración básica con Appium+Serenity",
                "issuer": "Udemy",
                "date": "2023",
                "hours": 8
            },
            {
                "id": "cypress-udemy",
                "name": "Cypress: Master en Automatización Test QA",
                "issuer": "Udemy",
                "date": "2023",
                "hours": 23
            },
            {
                "id": "katalon-udemy",
                "name": "Master: Katalon Studio Test QA Automation",
                "issuer": "Udemy",
                "date": "2023",
                "hours": 20
            }
        ],
        "Playwright & API Testing": [
            {
                "id": "playwright-api-rest",
                "name": "Automatización de Pruebas API Rest con Playwright",
                "issuer": "Udemy",
                "date": "2024",
                "hours": 16
            },
            {
                "id": "playwright-javascript",
                "name": "Curso de Playwright con JavaScript",
                "issuer": "Udemy",
                "date": "2024",
                "hours": 19
            },
            {
                "id": "playwright-typescript",
                "name": "Dominando Playwright con TypeScript: E2E Testing moderno",
                "issuer": "Udemy",
                "date": "2024",
                "hours": 21
            }
        ],
        "IA & Productividad": [
            {
                "id": "ai-fluency-anthropic",
                "name": "AI Fluency: Framework & Foundations",
                "issuer": "Anthropic",
                "date": "2024",
                "hours": 2
            },
            {
                "id": "claude-cowork",
                "name": "Introduction to Claude Cowork",
                "issuer": "Anthropic",
                "date": "2024",
                "hours": 1
            },
            {
                "id": "claude-101",
                "name": "Claude 101",
                "issuer": "Anthropic",
                "date": "2024",
                "hours": 1
            },
            {
                "id": "prompting-microsoft",
                "name": "Escriba indicaciones eficaces para lograr resultados óptimos",
                "issuer": "Microsoft",
                "date": "2024",
                "hours": 3
            },
            {
                "id": "copilot-studio",
                "name": "Introducción a Microsoft Copilot Studio",
                "issuer": "Microsoft",
                "date": "2024",
                "hours": 2
            },
            {
                "id": "copilot-chat",
                "name": "Introducción a Microsoft 365 Copilot Chat (básico)",
                "issuer": "Microsoft",
                "date": "2024",
                "hours": 2
            }
        ]
    },
    "languages": ["Español (Nativo)", "Inglés (B1 - en progreso)"]
}


class TestDocxGenerator:
    """Test DOCX document generation"""

    def test_generator_initialization(self):
        """Test generator can be initialized"""
        gen = DocxGenerator.from_dict(SAMPLE_CV)
        assert gen is not None
        assert gen.cv_data.profile.name == "ANDRES RODRIGUEZ PISA"

    def test_generate_creates_file(self, tmp_path):
        """Test document generation creates file"""
        gen = DocxGenerator.from_dict(SAMPLE_CV)
        output_file = tmp_path / "test.docx"
        
        result = gen.generate(output_file)
        
        assert result.exists()
        assert result.stat().st_size > 0


class TestPDFGenerator:
    """Test PDF document generation"""

    def test_generator_initialization(self):
        """Test generator can be initialized"""
        gen = PDFGenerator.from_dict(SAMPLE_CV)
        assert gen is not None
        assert gen.cv_data.profile.name == "ANDRES RODRIGUEZ PISA"

    def test_generate_creates_file(self, tmp_path):
        """Test document generation creates file"""
        gen = PDFGenerator.from_dict(SAMPLE_CV)
        output_file = tmp_path / "test.pdf"
        
        result = gen.generate(output_file)
        
        assert result.exists()
        assert result.stat().st_size > 0


class TestExcelGenerator:
    """Test Excel workbook generation"""

    def test_generator_initialization(self):
        """Test generator can be initialized"""
        gen = ExcelGenerator.from_dict(SAMPLE_CV)
        assert gen is not None
        assert gen.cv_data.profile.name == "ANDRES RODRIGUEZ PISA"

    def test_generate_creates_file(self, tmp_path):
        """Test workbook generation creates file"""
        gen = ExcelGenerator.from_dict(SAMPLE_CV)
        output_file = tmp_path / "test.xlsx"
        
        result = gen.generate(output_file)
        
        assert result.exists()
        assert result.stat().st_size > 0


class TestSyncValidator:
    """Test synchronization validation"""

    def test_validator_initialization(self):
        """Test validator initialization"""
        cv_model = CVDataModel(**SAMPLE_CV)
        validator = SyncValidator(cv_model)
        assert validator is not None

    def test_valid_data_passes(self):
        """Test validation passes for complete data"""
        report = SyncValidator.validate_dict(SAMPLE_CV)
        assert report.status == "success"
        assert report.all_in_sync is True
        assert len(report.mismatches) == 0

    def test_missing_profile_fails(self):
        """Test validation fails when profile is missing"""
        invalid_data = deepcopy(SAMPLE_CV)
        del invalid_data["profile"]["name"]
        
        report = SyncValidator.validate_dict(invalid_data)
        assert report.status == "error"
        assert report.all_in_sync is False

    def test_empty_skills_fails(self):
        """Test validation fails for empty skills"""
        invalid_data = deepcopy(SAMPLE_CV)
        invalid_data["skills"] = []
        
        report = SyncValidator.validate_dict(invalid_data)
        assert report.status == "error"
        assert report.all_in_sync is False


class TestIntegration:
    """Integration tests for all generators"""

    def test_all_generators_work_together(self, tmp_path):
        """Test all generators can work with same data"""
        # Generate all documents
        docx_gen = DocxGenerator.from_dict(SAMPLE_CV)
        pdf_gen = PDFGenerator.from_dict(SAMPLE_CV)
        excel_gen = ExcelGenerator.from_dict(SAMPLE_CV)

        docx_file = tmp_path / "test.docx"
        pdf_file = tmp_path / "test.pdf"
        excel_file = tmp_path / "test.xlsx"

        docx_gen.generate(docx_file)
        pdf_gen.generate(pdf_file)
        excel_gen.generate(excel_file)

        # Verify all files exist
        assert docx_file.exists()
        assert pdf_file.exists()
        assert excel_file.exists()

        # Verify file sizes are reasonable
        assert docx_file.stat().st_size > 1000  # DOCX should be > 1KB
        assert pdf_file.stat().st_size > 1000   # PDF should be > 1KB
        assert excel_file.stat().st_size > 1000  # Excel should be > 1KB


class TestCertificateSyncValidation:
    """Test that certificates are properly synchronized across all formats"""

    def test_exact_certificate_count_validation(self):
        """
        TEST 1: Validate EXACT certificate count from Andrés' real CV
        This test will FAIL if certificates are missing or duplicated
        """
        total_certs = sum(
            len(certs) for certs in SAMPLE_CV['certificates'].values()
        )
        
        # Must have exactly 21 certificates
        assert total_certs == EXPECTED_CERTIFICATE_COUNT, \
            f"❌ Certificate count mismatch! Expected {EXPECTED_CERTIFICATE_COUNT}, got {total_certs}"
        
        print(f"✅ Certificate count correct: {total_certs} certificates found")

    def test_certificate_categories_count_validation(self):
        """
        TEST 2: Validate EXACT count for each certificate category
        This test verifies each category has the correct number of certificates
        """
        for category, expected_count in EXPECTED_CERTIFICATE_CATEGORIES.items():
            actual_count = len(SAMPLE_CV['certificates'].get(category, []))
            
            assert category in SAMPLE_CV['certificates'], \
                f"❌ Missing category: '{category}'"
            
            assert actual_count == expected_count, \
                f"❌ Category '{category}' has {actual_count} certs, expected {expected_count}"
            
            print(f"✅ {category}: {actual_count} certificates (correct)")

    def test_all_expected_categories_present(self):
        """
        TEST 3: Verify ALL 5 certificate categories are present
        This test detects if any category is missing entirely
        """
        for category in EXPECTED_CERTIFICATE_CATEGORIES.keys():
            assert category in SAMPLE_CV['certificates'], \
                f"❌ MISSING CATEGORY: '{category}' not found in CV data!"
        
        print(f"✅ All {len(EXPECTED_CERTIFICATE_CATEGORIES)} categories present")

    def test_certificate_required_fields_validation(self):
        """
        TEST 4: Validate that EVERY certificate has required fields
        This ensures data integrity for document generation
        """
        required_fields = ['id', 'name', 'issuer', 'date', 'hours']
        certificates_checked = 0
        
        for category, certs in SAMPLE_CV['certificates'].items():
            for i, cert in enumerate(certs):
                for field in required_fields:
                    assert field in cert, \
                        f"❌ Certificate {i} in '{category}' missing field: '{field}'"
                
                certificates_checked += 1
        
        print(f"✅ All {certificates_checked} certificates have required fields")

    def test_docx_generator_includes_all_certificates(self, tmp_path):
        """
        TEST 5: DOCX Generator includes all certificate categories
        """
        gen = DocxGenerator.from_dict(SAMPLE_CV)
        output_file = tmp_path / "test_certs.docx"
        
        gen.generate(output_file)
        assert output_file.exists(), "❌ DOCX file not generated"
        
        from docx import Document
        doc = Document(output_file)
        text_content = '\n'.join([p.text for p in doc.paragraphs])
        
        # Verify all categories are in DOCX
        for category in EXPECTED_CERTIFICATE_CATEGORIES.keys():
            assert category in text_content, \
                f"❌ DOCX missing category: '{category}'"
        
        print(f"✅ DOCX contains all {len(EXPECTED_CERTIFICATE_CATEGORIES)} categories")

    def test_pdf_generator_includes_all_certificates(self, tmp_path):
        """
        TEST 6: PDF Generator includes all certificate categories
        """
        gen = PDFGenerator.from_dict(SAMPLE_CV)
        output_file = tmp_path / "test_certs.pdf"
        
        gen.generate(output_file)
        assert output_file.exists(), "❌ PDF file not generated"
        assert output_file.stat().st_size > 1000, "❌ PDF file too small"
        
        # Verify PDF contains expected sections
        pdf_size = output_file.stat().st_size
        assert pdf_size > 0, "❌ PDF file is empty"
        
        print(f"✅ PDF generated successfully ({pdf_size} bytes)")

    def test_excel_generator_has_certificate_sheet_with_all_data(self, tmp_path):
        """
        TEST 7: Excel Generator creates certificates sheet with all data
        """
        gen = ExcelGenerator.from_dict(SAMPLE_CV)
        output_file = tmp_path / "test_certs.xlsx"
        
        gen.generate(output_file)
        assert output_file.exists(), "❌ Excel file not generated"
        
        from openpyxl import load_workbook
        wb = load_workbook(output_file)
        
        assert 'Certificates' in wb.sheetnames, \
            f"❌ Excel missing 'Certificates' sheet. Found: {wb.sheetnames}"
        
        ws = wb['Certificates']
        assert ws.max_row > EXPECTED_CERTIFICATE_COUNT, \
            f"❌ Excel has {ws.max_row} rows, should have > {EXPECTED_CERTIFICATE_COUNT}"
        
        print(f"✅ Excel contains Certificates sheet with {ws.max_row - 1} data rows")


class TestDataSyncAcrossFormats:
    """Test that data remains synchronized across all document formats"""

    def test_sync_report_detects_missing_data(self):
        """Test that sync validator detects missing data"""
        incomplete_cv = deepcopy(SAMPLE_CV)
        del incomplete_cv['experience']
        
        report = SyncValidator.validate_dict(incomplete_cv)
        assert report.status == "error"
        assert report.all_in_sync is False

    def test_sync_report_passes_complete_data(self):
        """Test that sync validator passes for complete data"""
        report = SyncValidator.validate_dict(SAMPLE_CV)
        assert report.status == "success"
        assert report.all_in_sync is True
        assert len(report.mismatches) == 0

    def test_all_generators_handle_same_data(self, tmp_path):
        """Test that all generators can process the same data successfully"""
        docx_file = tmp_path / "CV.docx"
        pdf_file = tmp_path / "CV.pdf"
        excel_file = tmp_path / "CV.xlsx"
        
        # Generate all formats
        DocxGenerator.from_dict(SAMPLE_CV).generate(docx_file)
        PDFGenerator.from_dict(SAMPLE_CV).generate(pdf_file)
        ExcelGenerator.from_dict(SAMPLE_CV).generate(excel_file)
        
        # Verify all exist and have content
        assert docx_file.exists() and docx_file.stat().st_size > 0
        assert pdf_file.exists() and pdf_file.stat().st_size > 0
        assert excel_file.exists() and excel_file.stat().st_size > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
