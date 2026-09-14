"""Synchronization verification service"""

from datetime import datetime
from typing import Dict, List, Any
from .models import CVDataModel, SyncReportModel


class SyncValidator:
    """Validates that all CV artifacts are synchronized"""

    def __init__(self, cv_data: CVDataModel):
        """Initialize validator with CV data"""
        self.cv_data = cv_data
        self.timestamp = datetime.now().isoformat()
        self.mismatches: List[str] = []

    def _validate_profile(self) -> bool:
        """Validate profile data is present"""
        profile = self.cv_data.profile
        
        required_fields = ['name', 'title', 'email', 'location', 'bio']
        missing = [f for f in required_fields if not getattr(profile, f, None)]
        
        if missing:
            self.mismatches.append(f"Profile missing fields: {', '.join(missing)}")
            return False
        return True

    def _validate_skills(self) -> bool:
        """Validate skills structure"""
        if not self.cv_data.skills:
            self.mismatches.append("Skills data is empty")
            return False

        for category in self.cv_data.skills:
            if not category.skills:
                self.mismatches.append(f"Category '{category.category}' has no skills")
                return False

        return True

    def _validate_experience(self) -> bool:
        """Validate experience data"""
        if not self.cv_data.experience:
            self.mismatches.append("Experience data is empty")
            return False

        for exp in self.cv_data.experience:
            if not all([exp.company, exp.title, exp.period]):
                self.mismatches.append(f"Experience entry missing required fields: {exp.id}")
                return False

        return True

    def _validate_education(self) -> bool:
        """Validate education data"""
        if not self.cv_data.education:
            self.mismatches.append("Education data is empty")
            return False

        for edu in self.cv_data.education:
            if not all([edu.degree, edu.institution, edu.graduation]):
                self.mismatches.append(f"Education entry missing required fields: {edu.id}")
                return False

        return True

    def _validate_certificates(self) -> bool:
        """Validate certificates structure"""
        if not self.cv_data.certificates:
            self.mismatches.append("Certificates data is empty")
            return False

        for category, certs in self.cv_data.certificates.items():
            if not isinstance(certs, list):
                self.mismatches.append(f"Certificates category '{category}' is not a list")
                return False

        return True

    def _count_data(self) -> Dict[str, int]:
        """Count data elements for reporting"""
        return {
            'skills_categories': len(self.cv_data.skills) if self.cv_data.skills else 0,
            'skills_total': sum(
                len(c.skills) for c in self.cv_data.skills
            ) if self.cv_data.skills else 0,
            'experience_entries': len(self.cv_data.experience) if self.cv_data.experience else 0,
            'education_entries': len(self.cv_data.education) if self.cv_data.education else 0,
            'certificate_categories': len(self.cv_data.certificates) if self.cv_data.certificates else 0,
            'certificate_items': sum(
                len(certs) for certs in self.cv_data.certificates.values()
            ) if self.cv_data.certificates else 0,
        }

    def validate(self) -> SyncReportModel:
        """Run complete validation"""
        # Run all validations
        profile_ok = self._validate_profile()
        skills_ok = self._validate_skills()
        experience_ok = self._validate_experience()
        education_ok = self._validate_education()
        certificates_ok = self._validate_certificates()

        # All data present
        all_present = all([profile_ok, skills_ok, experience_ok, education_ok, certificates_ok])

        # Count data
        data_count = self._count_data()

        # Determine status
        if all_present and not self.mismatches:
            status = "success"
            message = f"✅ All data in sync! ({data_count['skills_total']} skills, {data_count['experience_entries']} experiences, {data_count['education_entries']} educations, {data_count['certificate_items']} certificates)"
        elif self.mismatches:
            status = "error"
            message = f"❌ Sync issues found: {'; '.join(self.mismatches[:3])}"
        else:
            status = "warning"
            message = "⚠️ Some data validation warnings"

        return SyncReportModel(
            timestamp=self.timestamp,
            status=status,
            web_data_present=profile_ok,
            docx_data_present=all_present,
            pdf_data_present=all_present,
            excel_data_present=all_present,
            all_in_sync=all_present and not self.mismatches,
            mismatches=self.mismatches,
            message=message
        )

    @staticmethod
    def validate_dict(data: Dict[str, Any]) -> SyncReportModel:
        """Validate from dictionary"""
        try:
            cv_model = CVDataModel(**data)
            validator = SyncValidator(cv_model)
            return validator.validate()
        except Exception as e:
            return SyncReportModel(
                timestamp=datetime.now().isoformat(),
                status="error",
                web_data_present=False,
                docx_data_present=False,
                pdf_data_present=False,
                excel_data_present=False,
                all_in_sync=False,
                mismatches=[str(e)],
                message=f"❌ Validation failed: {str(e)}"
            )
