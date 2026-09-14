"""DOCX document generator for CV"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

from app.domain.entities.cv_models import CVDataModel


class DocxGenerator:
    """Generate ATS-optimized DOCX CV from CV data"""

    def __init__(self, cv_data: CVDataModel):
        """Initialize generator with CV data"""
        self.cv_data = cv_data
        self.doc = Document()
        self._setup_document()

    def _setup_document(self) -> None:
        """Setup document margins and default styles"""
        sections = self.doc.sections
        for section in sections:
            section.top_margin = Inches(0.75)
            section.bottom_margin = Inches(0.75)
            section.left_margin = Inches(0.75)
            section.right_margin = Inches(0.75)

    def _add_heading_line(self, text: str, level: int = 1) -> None:
        """Add styled heading with line"""
        heading = self.doc.add_heading(text, level=level)
        heading.alignment = WD_ALIGN_PARAGRAPH.LEFT
        
        # Add line under heading
        p = heading.paragraph_format
        p.space_before = Pt(12)
        p.space_after = Pt(6)

    def _add_ruled_paragraph(self) -> None:
        """Add horizontal line"""
        p = self.doc.add_paragraph()
        pPr = p._element.get_or_add_pPr()
        pBdr = OxmlElement('w:pBdr')
        bottom = OxmlElement('w:bottom')
        bottom.set(qn('w:val'), 'single')
        bottom.set(qn('w:sz'), '12')
        bottom.set(qn('w:space'), '1')
        bottom.set(qn('w:color'), '000000')
        pBdr.append(bottom)
        pPr.append(pBdr)

    def generate_header(self) -> None:
        """Generate document header with profile information"""
        profile = self.cv_data.profile

        # Name and title
        name_para = self.doc.add_paragraph()
        name_run = name_para.add_run(profile.name)
        name_run.font.size = Pt(16)
        name_run.font.bold = True
        name_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        title_para = self.doc.add_paragraph(profile.title)
        title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        title_para.paragraph_format.space_after = Pt(6)

        # Contact info
        contact_parts = [
            f"Email: {profile.email}",
            f"Location: {profile.location}",
            f"GitHub: {profile.github}",
            f"LinkedIn: {profile.linkedin}",
        ]
        
        if profile.phone:
            contact_parts.insert(1, f"Phone: {profile.phone}")

        contact_para = self.doc.add_paragraph(" | ".join(contact_parts))
        contact_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        contact_para.paragraph_format.space_after = Pt(12)

        self._add_ruled_paragraph()

    def generate_profile(self) -> None:
        """Generate profile/summary section"""
        self._add_heading_line("PROFESSIONAL SUMMARY")
        
        profile_text = self.cv_data.profile.bio
        self.doc.add_paragraph(profile_text)
        self.doc.add_paragraph()  # Spacing

    def generate_skills(self) -> None:
        """Generate skills section"""
        if not self.cv_data.skills:
            return

        self._add_heading_line("TECHNICAL SKILLS")

        for category in self.cv_data.skills:
            skills_text = ", ".join([s.name for s in category.skills])
            
            p = self.doc.add_paragraph(style='List Bullet')
            p_run = p.add_run(f"{category.category}: ")
            p_run.bold = True
            p.add_run(skills_text)
            p.paragraph_format.space_after = Pt(3)

        self.doc.add_paragraph()  # Spacing

    def generate_experience(self) -> None:
        """Generate experience section"""
        if not self.cv_data.experience:
            return

        self._add_heading_line("PROFESSIONAL EXPERIENCE")

        for exp in self.cv_data.experience:
            # Job title and company
            job_para = self.doc.add_paragraph()
            job_run = job_para.add_run(f"{exp.title} | {exp.company}")
            job_run.bold = True
            job_para.paragraph_format.space_after = Pt(3)

            # Period
            period_para = self.doc.add_paragraph(exp.period)
            period_para.paragraph_format.space_after = Pt(6)
            period_para.runs[0].italic = True

            # Description
            self.doc.add_paragraph(exp.description, style='List Paragraph')

            # Achievements
            if exp.achievements:
                for achievement in exp.achievements:
                    self.doc.add_paragraph(achievement, style='List Bullet')

            # Technologies
            if exp.technologies:
                tech_para = self.doc.add_paragraph()
                tech_run = tech_para.add_run("Technologies: ")
                tech_run.bold = True
                tech_para.add_run(", ".join(exp.technologies))
                tech_para.paragraph_format.space_after = Pt(9)

        self.doc.add_paragraph()  # Spacing

    def generate_education(self) -> None:
        """Generate education section"""
        if not self.cv_data.education:
            return

        self._add_heading_line("EDUCATION")

        for edu in self.cv_data.education:
            edu_para = self.doc.add_paragraph()
            edu_run = edu_para.add_run(f"{edu.degree}")
            edu_run.bold = True
            edu_para.paragraph_format.space_after = Pt(3)

            inst_para = self.doc.add_paragraph(f"{edu.institution} | {edu.graduation}")
            inst_para.paragraph_format.space_after = Pt(6)
            inst_para.runs[0].italic = True

            if edu.description:
                self.doc.add_paragraph(edu.description)
                self.doc.add_paragraph()  # Spacing

    def generate_certificates(self) -> None:
        """Generate certifications section"""
        if not self.cv_data.certificates:
            return

        self._add_heading_line("CERTIFICATIONS & TRAINING")

        for category, certs in self.cv_data.certificates.items():
            if not certs:
                continue

            # Category heading
            cat_para = self.doc.add_paragraph(f"{category}:")
            cat_para.runs[0].bold = True
            cat_para.paragraph_format.space_after = Pt(3)

            # Certificates
            for cert in certs:
                cert_para = self.doc.add_paragraph(style='List Bullet')
                cert_run = cert_para.add_run(f"{cert.name}")
                cert_para.add_run(f" - {cert.issuer}")
                
                if cert.hours:
                    cert_para.add_run(f" ({cert.hours}h)")
                
                cert_para.paragraph_format.space_after = Pt(3)

        self.doc.add_paragraph()  # Spacing

    def generate(self, output_path: Path) -> Path:
        """Generate complete DOCX document"""
        self.generate_header()
        self.generate_profile()
        self.generate_skills()
        self.generate_experience()
        self.generate_education()
        self.generate_certificates()

        self.doc.save(str(output_path))
        return output_path

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'DocxGenerator':
        """Create generator from dictionary (from cv-data.ts)"""
        cv_model = CVDataModel(**data)
        return DocxGenerator(cv_model)

