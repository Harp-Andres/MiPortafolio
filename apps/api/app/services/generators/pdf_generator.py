"""PDF document generator for CV"""

from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)

from app.domain.entities.cv_models import CVDataModel


class PDFGenerator:
    """Generate visually formatted PDF CV from CV data"""

    # Color scheme
    PRIMARY_COLOR = HexColor('#1a1a1a')
    SECONDARY_COLOR = HexColor('#0066cc')
    ACCENT_COLOR = HexColor('#ff6b35')
    TEXT_COLOR = HexColor('#333333')
    LIGHT_GRAY = HexColor('#f5f5f5')

    def __init__(self, cv_data: CVDataModel):
        """Initialize generator with CV data"""
        self.cv_data = cv_data
        self.styles = self._create_styles()
        self.story = []

    def _create_styles(self) -> dict:
        """Create or get paragraph styles"""
        styles = getSampleStyleSheet()
        return styles

    def add_header(self) -> None:
        """Add document header"""
        profile = self.cv_data.profile

        # Name
        self.story.append(Paragraph(profile.name, self.styles['Heading1']))

        # Title
        self.story.append(Paragraph(profile.title, self.styles['Normal']))

        # Contact info
        contact_info = f"""
        Email: {profile.email} | Location: {profile.location}<br/>
        GitHub: {profile.github} | LinkedIn: {profile.linkedin}
        """
        self.story.append(Paragraph(contact_info, self.styles['Normal']))
        self.story.append(Spacer(1, 0.15*inch))

    def add_profile(self) -> None:
        """Add profile section"""
        self.story.append(Paragraph("PROFESSIONAL SUMMARY", self.styles['Heading2']))
        self.story.append(Paragraph(
            self.cv_data.profile.bio,
            self.styles['Normal']
        ))
        self.story.append(Spacer(1, 0.1*inch))

    def add_skills(self) -> None:
        """Add skills section"""
        if not self.cv_data.skills:
            return

        self.story.append(Paragraph("TECHNICAL SKILLS", self.styles['Heading2']))

        for category in self.cv_data.skills:
            skills_list = ", ".join([s.name for s in category.skills])
            skill_text = f"<b>{category.category}:</b> {skills_list}"
            self.story.append(Paragraph(skill_text, self.styles['Normal']))

        self.story.append(Spacer(1, 0.1*inch))

    def add_experience(self) -> None:
        """Add experience section"""
        if not self.cv_data.experience:
            return

        self.story.append(Paragraph("PROFESSIONAL EXPERIENCE", self.styles['Heading2']))

        for exp in self.cv_data.experience:
            # Job header
            job_header = f"<b>{exp.title}</b> | {exp.company}"
            self.story.append(Paragraph(job_header, self.styles['Normal']))

            # Period
            self.story.append(Paragraph(f"<i>{exp.period}</i>", self.styles['Normal']))

            # Description
            self.story.append(Paragraph(exp.description, self.styles['Normal']))

            # Achievements
            if exp.achievements:
                for achievement in exp.achievements:
                    self.story.append(Paragraph(
                        f"• {achievement}",
                        self.styles['Normal']
                    ))

            # Technologies
            if exp.technologies:
                tech_text = f"<b>Technologies:</b> {', '.join(exp.technologies)}"
                self.story.append(Paragraph(tech_text, self.styles['Normal']))

            self.story.append(Spacer(1, 0.08*inch))

    def add_education(self) -> None:
        """Add education section"""
        if not self.cv_data.education:
            return

        self.story.append(Paragraph("EDUCATION", self.styles['Heading2']))

        for edu in self.cv_data.education:
            edu_text = f"<b>{edu.degree}</b> | {edu.institution}"
            self.story.append(Paragraph(edu_text, self.styles['Normal']))

            self.story.append(Paragraph(f"<i>Graduated: {edu.graduation}</i>", self.styles['Normal']))

            if edu.description:
                self.story.append(Paragraph(edu.description, self.styles['Normal']))

            self.story.append(Spacer(1, 0.08*inch))

    def add_certificates(self) -> None:
        """Add certifications section"""
        if not self.cv_data.certificates:
            return

        self.story.append(Paragraph("CERTIFICATIONS & TRAINING", self.styles['Heading2']))

        for category, certs in self.cv_data.certificates.items():
            if not certs:
                continue

            self.story.append(Paragraph(f"<b>{category}</b>", self.styles['Normal']))

            for cert in certs:
                cert_text = f"{cert.name} - {cert.issuer}"
                if cert.hours:
                    cert_text += f" ({cert.hours}h)"
                self.story.append(Paragraph(f"• {cert_text}", self.styles['Normal']))

        self.story.append(Spacer(1, 0.1*inch))

    def generate(self, output_path: Path) -> Path:
        """Generate complete PDF document"""
        self.add_header()
        self.add_profile()
        self.add_skills()
        self.add_experience()
        self.add_education()
        self.add_certificates()

        # Create PDF
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch,
        )

        doc.build(self.story)
        return output_path

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'PDFGenerator':
        """Create generator from dictionary (from cv-data.ts)"""
        cv_model = CVDataModel(**data)
        return PDFGenerator(cv_model)

