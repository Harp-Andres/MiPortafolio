"""Data models for CV and portfolio information"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class SkillModel(BaseModel):
    """Skill with proficiency level"""
    name: str
    level: Optional[str] = None  # beginner, intermediate, advanced, expert


class SkillCategoryModel(BaseModel):
    """Category of skills"""
    category: str
    skills: List[SkillModel]


class ExperienceModel(BaseModel):
    """Work experience entry"""
    id: str
    title: str
    company: str
    period: str
    description: str
    technologies: Optional[List[str]] = None
    achievements: Optional[List[str]] = None


class EducationModel(BaseModel):
    """Education entry"""
    id: str
    degree: str
    institution: str
    graduation: str
    description: Optional[str] = None


class CertificateModel(BaseModel):
    """Certificate or certification"""
    id: str
    name: str
    issuer: str
    date: str
    credentialURL: Optional[str] = None
    hours: Optional[int] = None


class ProfileModel(BaseModel):
    """User profile information"""
    name: str
    title: str
    email: str
    phone: Optional[str] = None
    location: str
    bio: str
    github: str
    linkedin: str
    portfolio: str


class ProjectModel(BaseModel):
    """Portfolio project"""
    id: str
    name: str
    description: str
    longDescription: str
    technologies: List[str]
    github: str
    link: Optional[str] = None
    highlights: List[str]
    type: str  # featured, secondary, supporting
    image: Optional[str] = None


class CVDataModel(BaseModel):
    """Complete CV data"""
    profile: ProfileModel
    skills: List[SkillCategoryModel]
    experience: List[ExperienceModel]
    education: List[EducationModel]
    certificates: Dict[str, List[CertificateModel]]
    languages: Optional[List[str]] = None
    projects: Optional[List[ProjectModel]] = None


class GeneratedDocumentModel(BaseModel):
    """Response for generated documents"""
    filename: str
    format: str  # pdf, docx, xlsx
    size_bytes: int
    generated_at: str
    url: Optional[str] = None


class SyncReportModel(BaseModel):
    """Synchronization verification report"""
    timestamp: str
    status: str  # success, warning, error
    web_data_present: bool
    docx_data_present: bool
    pdf_data_present: bool
    excel_data_present: bool
    all_in_sync: bool
    mismatches: List[str] = Field(default_factory=list)
    message: str
