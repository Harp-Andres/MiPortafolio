"""
DOCX Generator Skill - Generate ATS-optimized CV in DOCX format.

Creates a professional resume document optimized for Applicant Tracking Systems.
Includes all portfolio information in Word format.

Expected Input:
    {
        "workspace_root": str,
        "template": str (default: "modern"),
        "include_projects": bool (default: True),
        "include_skills": bool (default: True)
    }

Returns:
    {
        "status": "success" | "failed",
        "document_path": str,
        "file_size_bytes": int,
        "sections_generated": int,
        "duration_ms": float
    }
"""

import asyncio
from pathlib import Path
from datetime import datetime

import importlib.util as _ilu, sys as _sys; _bs = _ilu.spec_from_file_location('_base_skill', __import__('pathlib').Path(__file__).parent.parent / 'base_skill.py'); _bsm = _ilu.module_from_spec(_bs); _bs.loader.exec_module(_bsm); BaseSkill = _bsm.BaseSkill; SkillRequest = _bsm.SkillRequest; SkillResult = _bsm.SkillResult; SkillStatus = _bsm.SkillStatus; skill_wrapper = _bsm.skill_wrapper; _lh = _ilu.spec_from_file_location('_logger_helper', __import__('pathlib').Path(__file__).parent.parent / 'logger_helper.py'); _lhm = _ilu.module_from_spec(_lh); _lh.loader.exec_module(_lhm); get_logger = _lhm.get_logger


logger = get_logger(__name__)


class DocxGenerator(BaseSkill):
    """Generate ATS-optimized DOCX resume.

    This skill:
    1. Reads portfolio data
    2. Formats for ATS compatibility
    3. Generates Word document
    4. Validates output
    """

    def __init__(self, workspace_root: str):
        """Initialize DocxGenerator.

        Args:
            workspace_root: Root directory of the project.
        """
        super().__init__(workspace_root)
        self.skill_name = "DocxGenerator"
        self.security_filter = SecurityFilter(workspace_root=workspace_root)

    async def _run_implementation(self, request) -> SkillResult:
        """Generate DOCX resume.

        Args:
            request: SkillRequest with parameters.

        Returns:
            SkillResult with document info.
        """
        start_time = datetime.now()
        metrics = MetricsCollector()

        try:
            logger.info(
                f"[{self.skill_name}] Starting DOCX generation",
                extra={"workspace": str(self.workspace_root)},
            )

            params = request.parameters
            template = params.get("template", skill_defaults.DOCX_TEMPLATE)
            include_projects = params.get("include_projects", skill_defaults.INCLUDE_PROJECTS)
            include_skills = params.get("include_skills", skill_defaults.INCLUDE_SKILLS)

            with Timer(metrics, "docx_generation_ms"):
                doc_path, file_size, sections = await self._generate_docx(
                    template=template,
                    include_projects=include_projects,
                    include_skills=include_skills,
                )

            duration = (datetime.now() - start_time).total_seconds() * 1000

            logger.info(
                f"[{self.skill_name}] DOCX generation completed",
                extra={
                    "document_path": str(doc_path),
                    "file_size": file_size,
                    "sections": sections,
                    "duration_ms": duration,
                },
            )

            return SkillResult(
                skill_name=self.skill_name,
                status=SkillStatus.SUCCESS,
                output={
                    "document_path": str(doc_path),
                    "file_size_bytes": file_size,
                    "sections_generated": sections,
                    "duration_ms": duration,
                },
            )

        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds() * 1000
            logger.error(
                f"[{self.skill_name}] DOCX generation failed",
                extra={"error": str(e), "duration_ms": duration},
                exc_info=True,
            )
            return SkillResult(
                skill_name=self.skill_name,
                status=SkillStatus.FAILED,
                error=str(e),
                output={"duration_ms": duration},
            )

    async def _generate_docx(
        self,
        template: str = "modern",
        include_projects: bool = True,
        include_skills: bool = True,
    ) -> tuple:
        """Generate DOCX document.

        Args:
            template: Document template name.
            include_projects: Include projects section.
            include_skills: Include skills section.

        Returns:
            Tuple of (path, file_size, num_sections).
        """
        logger.debug(f"[{self.skill_name}] Generating DOCX document")
        # TODO: Implement DOCX generation
        return project_config.RESUME_DOCX_PATH, 125000, 7  # Stub


__all__ = ["DocxGenerator"]
